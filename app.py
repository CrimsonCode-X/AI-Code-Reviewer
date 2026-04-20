import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini Client
try:
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Failed to initialize Gemini Client: {e}")
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    if not client:
        return jsonify({"error": "Gemini API key not configured. Please set GEMINI_API_KEY."}), 500

    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'javascript')

    if not code:
        return jsonify({"error": "No code provided"}), 400

    prompt = f"""
You are an expert AI Code Reviewer. Analyze the following {language} code.
Provide your response strictly in the following JSON format:
{{
  "bugs": "Markdown formatted explanation of any logical errors, security vulnerabilities, or syntax errors.",
  "optimizations": "Markdown formatted explanation of performance inefficiencies, memory leaks, or algorithmic improvements.",
  "quality": "Markdown formatted explanation of code readability, best practices, maintainability, and style enhancements."
}}

If there are no issues in a category, mention that the code looks good in that regard.

Code to analyze:
```{language}
{code}
```
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        response_text = response.text
        
        # Strip potential markdown block syntax if the model wraps the json
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result = json.loads(response_text.strip())
        return jsonify(result)
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from AI response: {e}")
        print("Raw response:", response.text)
        return jsonify({"error": "AI response was not in expected JSON format."}), 500
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
