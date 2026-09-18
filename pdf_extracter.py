import pdfplumber

def pdf_extracter(pdf:str):
    with pdfplumber.open(pdf) as pdffile:
        full_text = ""
        for page in pdffile.pages:
            full_text += (page.extract_text() or "") + "\n"
    
    return full_text    
