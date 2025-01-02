from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

def summarizer(user_input):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer HUGGING_FACE_HF_CODE_HERE"}  
    payload = {"inputs": user_input}

    try:
       
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # If the request fails, it will raise an error
        return response.json()[0]["summary_text"]
    except Exception as e:
        print(f"Error: {e}")
        return "Error summarizing text. Please try again later."

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form

@app.route('/process', methods=['POST'])
def process_text():
    user_input = request.form.get('user_input')  # Get input text from the form
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    summarized_text = summarizer(user_input)
    return jsonify({"summary": summarized_text})

if __name__ == "__main__":
    app.run(debug=True)
