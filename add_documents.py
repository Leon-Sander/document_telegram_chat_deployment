from utils import load_documents, load_db, load_embeddings
from langchain_core.documents.base import Document
from utils import get_pdf_texts, get_document_chunks

def add_documents(documents: list[Document]):
    db = load_db(embeddings=load_embeddings())
    db.add_documents(documents)
    print("Documents Added")

def add_documents_from_pdf_bytes(pdf_bytes_list: list[bytes]):
    texts = get_pdf_texts(pdf_bytes_list)
    documents = get_document_chunks(texts)
    add_documents(documents)

def main():
    add_documents(load_documents("new_document/"))

if __name__ == "__main__":
    main()