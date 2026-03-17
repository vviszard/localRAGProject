import ollama
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BRAIN_DIR = "./brainSpace"
MODEL = "qwen2.5:1.5b"

def chunk_text(text, size= 800, overlap= 150):
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
    

def local_aggregator():
    # Reads the files in the folder and return structured context
    local_text = ""
    
    if not os.path.exists(BRAIN_DIR):
        os.makedirs(BRAIN_DIR)
        print(f"'{BRAIN_DIR}' Directory created. Please add your files here.")
        return ""
    # get all the '.txt' and '.md' files
    
    files = [f for f in os.listdir(BRAIN_DIR) if f.endswith(('.txt','.md'))]
    
    if not files:
        print("The Folder is empty.")
        return ""
    
    for filename in files:
        file_path = os.path.join(BRAIN_DIR, filename)
        try:
            with open(file_path,"r", encoding= "utf-8") as f:
                content = f.read()
                if len(content) > 1000:
                    chunk_content = chunk_text(content)
                    for i, text_piece in enumerate(chunk_content):
                        local_text += f"\n[DOCUMENT: {filename} | PART: {i+1}]\n{text_piece}\n"
                else:
                    local_text += f"\n\n[DOCUMENT: {filename}]\n{content}\n[END {filename}]\n"
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            
    return local_text

class BrainSentry(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.txt','.md')):
            global knowledge
            print(f"\nChange detected in {os.path.basename(event.src_path)}... refreshing context data")
            knowledge = local_aggregator()
            print("\nGPT: ", end="")
            
def ask_ai(question, context, history):
    
    messages = [{"role":"system",
                 "content": (
                     "You are a Local Document Assistant. Use ONLY the provided context to answer."
                     "Always start with 'Source: [Filename]'. Link info across multiple docs.")},
                *history,
                {"role":"user","content": f"CONTEXT: \n{context[:10000]}\n\nQUESTION: {question}"}]
    print("\nAI is analyzing...")
    
    response = ollama.chat(model= MODEL, messages= messages, stream = True)
    
    full_response= ""
    print("\nGPT: ", end= "")
    for chunk in response:
        content = chunk['message']['content']
        print(content, end="", flush= True)
        full_response += content
    print("\n")
    
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": full_response})
    
    if len(history) > 8:
        history.pop(0)
        history.pop(0)
        

if __name__ == "__main__":
    print("...local docments reader...")
    knowledge = local_aggregator()
    
    event_handler = BrainSentry()
    observer = Observer()
    observer.schedule(event_handler, BRAIN_DIR, recursive= False)
    observer.start()

    if not knowledge:
        print("No data found. Add files in the folder")
    else:
        print(f"data loaded: {len(knowledge)} characters.")
    
    chat_history = []
        
    try:
        
        while True:
            q = input("Ask a question or type 'quit' to exit: ")
            
            if q.lower() == 'quit':
                break
            
            if q.strip():
                ask_ai(q, knowledge, chat_history)
    finally:
        observer.stop()
        observer.join()
