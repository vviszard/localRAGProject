import ollama
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ragTools import text_chunker, text_extractor

BRAIN_DIR = "./brainSpace"
MODEL = "qwen2.5:1.5b"
SUPPORTED_EXT = ('.txt','.md','.pdf','docx')

def local_aggregator():
    # Reads the files in the folder and return structured context
    local_text = ""
    
    if not os.path.exists(BRAIN_DIR):
        os.makedirs(BRAIN_DIR)
        print(f"'{BRAIN_DIR}' Directory created. Please add your files here.")
        return ""
    # get all the '.txt' and '.md' files
    
    files = [f for f in os.listdir(BRAIN_DIR) if f.lower().endswith(SUPPORTED_EXT)]
    
    if not files:
        print("The Folder is empty.")
        return ""
    
    for filename in files:
        file_path = os.path.join(BRAIN_DIR, filename)
            
        content = text_extractor(file_path)
        
        if not content.strip():
            continue
            
        if len(content) > 1000:
            chunk_content = text_chunker(content)
            for i, text_piece in enumerate(chunk_content):
                local_text += f"\n[DOCUMENT: {filename} | PART: {i+1}]\n{text_piece}\n"
        else:
            local_text += f"\n\n[DOCUMENT: {filename}]\n{content}\n[END {filename}]\n"
            
    return local_text

class BrainSentry(FileSystemEventHandler):
    
    def handle_change(self, event):
        if not event.is_directory and event.src_path.endswith(('.txt','.md')):
            global knowledge
            filename = os.path.basename(event.src_path)
            event_type = event.event_type.upper()
            print(f"\n[BrainSpace]: {event_type} {filename} | Context Updated -> {len(knowledge)} Characters.")
            knowledge = local_aggregator()            
            print("\n[BrainSpace]: ", end="")
    def on_modified(self, event):
        self.handle_change(event)
    def on_created(self, event):
        self.handle_change(event)
    def on_deleted(self, event):
        self.handle_change(event)
    def on_moved(self, event):
        self.handle_change(event)
        
            
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
    print("\n[BrainSpace]: ", end= "")
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
