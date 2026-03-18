import os
import pypdf
import docx

def text_chunker(text, size= 800, overlap= 150):
    '''
    chunk_size = character per piece.
    overlap = How many character to repeat from previous piece.
    '''
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def text_extractor(filepath):
    xtnsion = os.path.splitext(filepath)[1].lower()
    text = ""
    
    try:
        if xtnsion in ('.txt', '.md'):
            with open(filepath, "r", encoding = "utf-8") as f:
                text = f.read()
        
        elif xtnsion == '.pdf':
            reader = pypdf.PdfReader(filepath)
            for page in reader.pages:
                extract = page.extract_text()
                if extract:
                    text += extract + "\n"
        elif xtnsion == '.docx':
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            
    except Exception as e:
        print(f"error parsing {filepath}: {e}")
        
    return text