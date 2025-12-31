from langchain_community.document_loaders import PyPDFLoader



def extract_pdf_loader(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs