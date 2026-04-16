from flask import Flask, request, jsonify,render_template
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

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

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "GET":
        return "Use POST request to interact with chatbot"
     
    user_input = request.json["message"]

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})

    return jsonify({"response": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))