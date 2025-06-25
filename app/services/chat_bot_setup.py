from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


# Load environment variables (like your OpenAI API key)
load_dotenv()

# Load all PDFs from the data folder
loader = DirectoryLoader(
    "data/sports_docs_chatbot",
    glob="**/*.pdf",  # Recursively finds all PDFs
    loader_cls=PyPDFLoader
)
documents = loader.load()

# Split documents into chunks
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)
print(f"📄 Loaded {len(documents)} raw documents")
print(f"✂️  Split into {len(docs)} chunks")

# Embed in batches and save to ChromaDB
embedding = OpenAIEmbeddings()
batch_size = 100

# Create the initial vector store with the first batch
db = Chroma.from_documents(
    docs[:batch_size],
    embedding,
    persist_directory="chroma_db"
)

# Add the remaining documents in batches
for i in range(batch_size, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    db.add_documents(batch)

db.persist()
print("✅ PDF documents embedded and ChromaDB saved to chroma_db/")
