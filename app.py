import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
# Using the free Llama 3.3 model from Together AI
TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-api', methods=['GET'])
def test_api():
    """Test route to verify API key and connection to Together AI"""
    if not TOGETHER_API_KEY:
        return jsonify({"status": "error", "message": "API key not configured"}), 500
    
    try:
        # Make a simple request to the models endpoint to verify API key
        response = requests.get(
            "https://api.together.xyz/v1/models",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            timeout=10
        )
        
        print(f"Test API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "API key is valid and connection to Together AI is working"}), 200
        elif response.status_code == 401:
            return jsonify({"status": "error", "message": "Authentication error: Your API key is invalid or expired"}), 401
        else:
            return jsonify({"status": "error", "message": f"Unexpected status code: {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error testing API: {str(e)}"}), 500

@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    data = request.get_json()
    text = data.get('text', '')
    academic_level = data.get('academic_level', 'university')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    if not TOGETHER_API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    try:
        # Prepare the prompt for Together AI with improved instructions
        prompt = f"""Paraphrase the following academic text to maintain the same meaning but with different wording. 
        
        Guidelines:
        - Make it sound natural and appropriate for {academic_level} level academic writing
        - Avoid overly formal or verbose language
        - Keep the paraphrased text concise and clear
        - Don't add unnecessary explanations or notes
        - Don't include placeholders like "(Author's Last Name, Year)" unless they're in the original text
        - Focus on rewording while preserving the original meaning and tone
        - Paraphrase only the texts that is being entered by the user.
        - Do not produce additional notes and explanations.
        - Just produce the paraphrased text paragraphs.
        
        Original text: {text}
        
        Paraphrased text:"""
        
        # Call Together AI API
        response = requests.post(
            TOGETHER_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {TOGETHER_API_KEY}"
            },
            json={
                "model": TOGETHER_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an academic writing assistant that specializes in paraphrasing text while maintaining academic integrity. Just produce only the paraphrased text, no other text or notes."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60  # Adding a timeout to prevent hanging requests
        )
        
        # Print response for debugging
        print(f"API Response Status: {response.status_code}")
        print(f"API Response Headers: {response.headers}")
        
        # Handle authentication errors specifically
        if response.status_code == 401:
            error_message = "Authentication error: Your API key is invalid or expired. Please get a new API key from Together AI."
            print(error_message)
            try:
                error_details = response.json()
                print(f"Error details: {error_details}")
            except:
                pass
            return jsonify({"error": error_message}), 401
        
        # Check if response is successful
        response.raise_for_status()
        
        response_data = response.json()
        print(f"API Response Data: {response_data}")
        
        if 'choices' in response_data and len(response_data['choices']) > 0:
            # Extract the content from the message
            paraphrased_text = response_data['choices'][0]['message']['content'].strip()
            
            # Clean up any extra notes or explanations that might be added
            if "Note:" in paraphrased_text:
                paraphrased_text = paraphrased_text.split("Note:")[0].strip()
            if "Alternatively:" in paraphrased_text:
                paraphrased_text = paraphrased_text.split("Alternatively:")[0].strip()
                
            return jsonify({"paraphrased_text": paraphrased_text})
        else:
            error_msg = "Failed to get proper response from API"
            if 'error' in response_data:
                error_msg += f": {response_data['error'].get('message', '')}"
            return jsonify({"error": error_msg}), 500
            
    except requests.exceptions.RequestException as e:
        error_message = f"API request error: {str(e)}"
        print(error_message)
        return jsonify({"error": error_message}), 500
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
