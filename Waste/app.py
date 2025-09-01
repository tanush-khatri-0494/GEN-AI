from flask import Flask, request, jsonify, send_from_directory
import requests, os
from dotenv import load_dotenv

# Load API key
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

app = Flask(__name__, static_folder='.')

# Serve index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve CSS/JS files
@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('.', filename)

# Generate guide using Perplexity AI
@app.route('/generate', methods=['POST'])
def generate_guide():
    data = request.get_json()
    item = data.get('item', '')
    category = data.get('category', 'general')
    context = data.get('context', '')

    # Prepare the prompt for AI
    prompt = (
        f"Provide an eco-friendly disposal guide for the following item. "
        f"The instructions should be in plain text only, without any numbers, bullets, hashtags, or symbols. "
        f"Use clear, easy-to-follow sentences.\n\n"
        f"Item: {item}\n"
        f"Category: {category}\n"
        f"Context: {context}"
    )


    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=12  # seconds
        )

        if response.status_code == 200:
            result = response.json()
            guide_text = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            if not guide_text:
                guide_text = f"AI did not return a guide for {item}."
        else:
            guide_text = f"Failed to fetch from Perplexity API. Status code: {response.status_code}"

    except Exception as e:
        guide_text = f"Error connecting to Perplexity API: {e}"

    return jsonify({"guide": guide_text})

if __name__ == '__main__':
    app.run(debug=True)