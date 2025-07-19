from flask import Flask, request, jsonify
from openai import OpenAI
import os
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with error handling
try:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    print("✓ OpenAI client initialized successfully")
except Exception as e:
    print(f"✗ Error initializing OpenAI client: {e}")
    client = None

@app.route("/")
def index():
    return "GPT-4 Chatbot Backend is Running"

@app.route("/chat", methods=["POST"])
def chat():
    # Check if OpenAI client is available
    if not client:
        return jsonify({"error": "OpenAI client not initialized. Check your API key."}), 500
    
    data = request.get_json()
    user_message = data.get("message")
    
    print(f"Received message: {user_message}")  # Debug log

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        print("Sending request to OpenAI...")  # Debug log
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Sunny Side Café in Daytona Beach, FL. You can help customers with information about hours, menu items, location, and general café questions. Be friendly and helpful!"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,  # Limit response length
            temperature=0.7
        )
        
        reply = response.choices[0].message.content
        print(f"OpenAI response: {reply}")  # Debug log
        return jsonify({"reply": reply})
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # Debug log
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5001, debug=True)