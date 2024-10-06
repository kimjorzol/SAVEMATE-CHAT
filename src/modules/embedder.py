import os
import tempfile
from langchain_upstage import UpstageEmbeddings
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import getpass

class Embedder:

    def __init__(self, input_folder="pdf_folder", output_folder="embeddings"):#(self, input_folder="/Users/sohi/Downloads/trial1_1/pdf_folder", output_folder="/Users/sohi/Downloads/trial1_1/embeddings"): #"/Users/summer/Downloads/Robby-chat/trial1/embeddings"):
        #self.input_folder = input_folder
        #self.PATH = output_folder
        
        # 아래와 같이 상대 경로로 변경
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.input_folder = os.path.join(base_path, input_folder)
        self.PATH = os.path.join(base_path, output_folder)

        # Load environment variables from .env file
        load_dotenv()
        
        # Get the API key from the environment variable
        UPSTAGE_API_KEY = 'up_sE1q34hltAbAjZoAj0rfCmVIHh6Ws' #os.getenv("UPSTAGE_API_KEY")
        
        # Print the API key to debug
        print(f"Using Upstage API Key: {UPSTAGE_API_KEY}")
        
        if UPSTAGE_API_KEY is None:
            raise ValueError("UPSTAGE_API_KEY environment variable not found.")
        
        # Try using `api_key` parameter for UpstageEmbeddings
        try:
            self.embeddings = UpstageEmbeddings(model="solar-embedding-1-large", 
                                                api_key=UPSTAGE_API_KEY)
        except TypeError:
            # If `api_key` is not the correct parameter, fall back to `upstage_api_key`
            self.embeddings = UpstageEmbeddings(model="solar-embedding-1-large", 
                                                upstage_api_key=UPSTAGE_API_KEY)

    def create_embeddings_dir(self):
        """Creates a directory to store the Chroma DB files."""
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)

    def store_doc_embeds(self, file, original_filename):
        """Stores document embeddings using Solar Pro and Chroma DB."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        def get_file_extension(uploaded_file):
            return os.path.splitext(uploaded_file)[1].lower()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
        )

        file_extension = get_file_extension(original_filename)

        # Load the file based on its extension
        if file_extension == ".csv":
            loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ','})
            data = loader.load()
        elif file_extension == ".pdf":
            loader = PyPDFLoader(file_path=tmp_file_path)
            data = loader.load_and_split(text_splitter)
        elif file_extension == ".txt":
            loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
            data = loader.load_and_split(text_splitter)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        # Print the contents of the loaded data for debugging
        print(f"Loaded data for {original_filename}:")
        for doc in data[:3]:  # Print first 3 chunks as a sample
            print(doc.page_content[:200])  # Print first 200 characters of each chunk

        # Remove the temporary file
        os.remove(tmp_file_path)

        # Store embeddings using Chroma DB
        #chroma_collection_path = os.path.join(self.PATH, original_filename)
        vector_store = Chroma.from_documents(
            documents=data,
            ids=[doc.page_content for doc in data],
            embedding=self.embeddings,
            persist_directory=self.PATH  # 기존 코드에서 chroma_collection_path를 self.PATH로 변경
        )
        vector_store.persist()


    def store_embeddings_from_folder(self):
        """Stores embeddings for all PDF files in the input folder."""
        for filename in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, filename)

            # Check if the file is a PDF (you can add other file types as needed)
            if filename.lower().endswith(".pdf"):
                with open(file_path, "rb") as file:
                    file_content = file.read()
                    #print(f"Storing embeddings for: {filename}")
                    self.store_doc_embeds(file_content, filename)

    def get_retriever(self):
        """Returns a retriever based on document embeddings."""
        # Retrieve or store the vector store as needed
        #vector_store = self.get_doc_embeds(file, original_filename)
        vector_store = Chroma(
            persist_directory= self.PATH,
            embedding_function= self.get_embedding_function()
        )      
        
        # Convert the vector store into a retriever

        retriever = vector_store.as_retriever()
        print('retriever:,',retriever)
        return retriever

    def get_embedding_function(self):
        return self.embeddings

    def list_embeddings(self):
        """List all stored embeddings for debugging."""
        print("Listing stored embeddings:")
        for root, dirs, files in os.walk(self.PATH):
            for file in files:
                print(f"File: {file}, Path: {os.path.join(root, file)}")


# 해당 파일이 직접 실행될 때만 사용되는 코드
## 디렉토리 이동 후 python3 embedder.py
if __name__ == "__main__":
    # Define the folders for input PDFs and output embeddings
    #input_folder = input_folder #"/Users/sohi/Downloads/trial1_1/pdf_folder"
    #output_folder = "/Users/sohi/Downloads/trial1_1/embeddings"

    # initializer와 연계되게 쓰는 것이 좋다.
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(base_path, "pdf_folder")
    output_folder = os.path.join(base_path, "embeddings")

    embedder = Embedder(input_folder=input_folder, output_folder=output_folder)

    # Store embeddings for all PDFs in the input folder
    embedder.store_embeddings_from_folder()

    # List all stored embeddings for verification
    embedder.list_embeddings()
