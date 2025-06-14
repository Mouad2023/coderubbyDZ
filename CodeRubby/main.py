import os
from dotenv import load_dotenv
from llm_client import LLMClient

# Load environment variables
load_dotenv()

def main():
    # Load API key from environment
    api_key = os.getenv("NOVITA_API_KEY")
    print(f"Debug: Loaded API key: {api_key}")  # Debug print
    if not api_key:
        print("❌ Missing API key. Please set the 'NOVITA_API_KEY' environment variable.")
        return

    # Initialize LLM Client
    llm = LLMClient(api_key)
    
    # Test prompt
    print("\n🤖 Testing DeepSeek with Novita AI:")
    prompt = "Create a Python function to validate an email address."
    response = llm.query(prompt)
    print("\n🤖 Response from DeepSeek:")
    print(response)

if __name__ == "__main__":
    main()