import pdfplumber

with pdfplumber.open("Cover_Letter.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"
        
print(full_text[:1000])