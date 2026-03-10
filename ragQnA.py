import requests
from bs4 import BeautifulSoup
import ollama
import os

def web_scraper(url, file_path="scraped.txt"):
    # Identity headers must be defined here!
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'
    }
    
    if os.path.exists(file_path):
        print(f"...loading context information from {file_path}...")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    try:
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')       
        
        # Look for the article body
        content = soup.find(id="mw-content-text")
        
        if content:
            paragraphs = content.find_all('p')
            text = " ".join([p.get_text() for p in paragraphs]).strip()
        else:
            # Fallback: Just grab all paragraph text if ID is missing
            text = " ".join([p.get_text() for p in soup.find_all('p')]).strip()

        # Final check: Did we actually get content?
        if len(text) < 100:
            return "Error: Wikipedia blocked the content or page is empty."

        text = text[:10000] # Cap it for your 4GB RAM
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Information Saved Successfully.")
        return text
    
    except Exception as e:
        return f"Error: {e}"

def ask_gpt(question, context):
    print("\nAI is analyzing the document...")
    
    messages = [
        {"role": "system", "content": "You are a literal document reader. Use the provided context only. If the answer isn't there, say 'Information not found.'"},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}"}
    ]
    
    stream = ollama.chat(
        model='qwen2.5:0.5b',
        messages=messages,
        stream=True,
        options={"temperature": 0}
    )
    
    print("\nGPT: ", end="")
    for chunk in stream:
        print(chunk['message']['content'], end="", flush=True)
    print("\n")

if __name__ == "__main__":
    # IMPORTANT: Delete 'scraped.txt' before running this so it re-scrapes correctly!
    if os.path.exists("scraped.txt"):
        os.remove("scraped.txt")
        
    url = input("please enter the url of the webpage: ")
    knowledge = web_scraper(url)
    
    print(f"📊 Context loaded: {len(knowledge)} characters.")
    
    while True:
        q = input("Ask a question or type 'quit' to exit: ")
        if q.lower() == 'quit':
            break
        if len(knowledge) > 100:
            ask_gpt(q, knowledge)
        else:
            print("❌ Cannot ask question: Context is too short. Check your internet/headers.")