import fitz  
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rag.cache import ResponseCache
from rag.utils import generate_cache_key

# Function to load PDF content by sections
def load_pdf_by_sections(file_path):
    """
    Load and extract text from a PDF file, splitting it into sections based on the table of contents.

    """
    doc = fitz.open(file_path)
    toc = doc.get_toc(simple=True)  # Get the table of contents in a simple format
    sections = []

    if toc:
        for i, entry in enumerate(toc):
            level, title, page_num = entry
            start_page = page_num - 1  
            end_page = toc[i + 1][2] - 1 if i + 1 < len(toc) else doc.page_count
            text = ""
            for page in doc[start_page:end_page]:
                text += page.get_text()
            sections.append(Document(page_content=text, metadata={"source": title}))
    else:
        # If no TOC is found, treat the entire document as a single section
        text = ""
        for page in doc:
            text += page.get_text()
        sections.append(Document(page_content=text, metadata={"source": "Document"}))

    return sections

def setup_retriever(documents):
    """
    Setup the FAISS retriever with the provided documents.

    """
    # For text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      
        chunk_overlap=100,   
        separators=["\n\n", "\n", " ", ""]  # Prioritize splitting by paragraphs
    )
    
    text_chunks = text_splitter.split_documents(documents)
    
    # Load the HuggingFace Embeddings model with a model name
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") 
    
    # Vector embedding for text chunks using FAISS
    knowledge_base = FAISS.from_documents(text_chunks, embeddings)
    
    # Create a retriever from the FAISS knowledge base
    retriever = knowledge_base.as_retriever(search_kwargs={"k": 1})  # Retrieve top 1 most similar passage
    
    return retriever, knowledge_base
