import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from llm_client import LLMClient

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize LLM client
api_key = os.getenv("NOVITA_API_KEY")
if not api_key:
    raise ValueError("❌ Missing API key. Please set the 'NOVITA_API_KEY' environment variable.")

llm = LLMClient(api_key)

@app.route('/')
def guide():
    return render_template('guide.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    response = None
    prompt = None
    error = None

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if not prompt:
            error = "No prompt provided"
        else:
            try:
                response = llm.query(prompt)
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template('index.html', prompt=prompt, response=response, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)