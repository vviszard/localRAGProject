import ollama
import os

BRAIN_DIR = "./brainSpace"
MODEL = "qwen2.5:0.5b"

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
                local_text += f"\n\n[DOCUMENT: {filename}]\n{content}\n[END {filename}]\n"
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            
    return local_text
                
def ask_ai(question, context):
    system_prompt = (
        "You are a Local Document Assistant. Use ONLY the provided context to answer."
        "If the answer is not in the context, say 'I don't have that info in my local files.'"
    )
    
    trimmed_context = context[:8000]
    
    prompt_with_context = f"CONTEXT: \n{trimmed_context}\n\nQUESTION: {question}"
    
    print("\nAI is analyzing the documents...")
    
    stream = ollama.generate(
        model = MODEL,
        prompt = prompt_with_context,
        system = system_prompt,
        stream = True,
        options = {"temperature": 0.1})
       
    print("\nGPT: ", end="")
    for chunk in stream:
        print(chunk['response'], end="", flush=True)
    print("\n")

if __name__ == "__main__":
    print("...local docments reader...")
    knowledge = local_aggregator()

    if not knowledge:
        print("No data found. Add files in the folder")
    else:
        print(f"data loaded: {len(knowledge)} characters.")

    while True:
        q = input("Ask a question or type 'quit' to exit: ")
        
        if q.lower() == 'quit':
            break
        
        if q.strip():
            ask_ai(q, knowledge)
