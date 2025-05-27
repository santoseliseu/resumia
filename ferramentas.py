import PyPDF2

def ler_texto_pdf(curriculo_pdf):
    conteudo_pdf = PyPDF2.PdfReader(curriculo_pdf)

    texto_pdf = ''

    for page in conteudo_pdf.pages:
        texto_pdf += page.extract_text()
    
    print(texto_pdf)
    return texto_pdf