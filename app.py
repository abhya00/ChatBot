from flask import Flask, request, jsonify,render_template
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__)

# store chat history
messages = []
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Invalid request"}), 400

        user_input = data["message"]

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )

        reply = response.choices[0].message.content

        messages.append({"role": "assistant", "content": reply})

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))