import re

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_documents(documents):
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    return documents
    
if __name__ == "__main__":
    sample = "Courses\nlike\nCircuit\nTheory\nand\nDevices,\nDigital\nCircuits"
    print(clean_text(sample))