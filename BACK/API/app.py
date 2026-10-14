import os

from flask          import Flask, app, render_template, request, jsonify
from BACK.LLM.agent import llm



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "FRONT"), static_folder=os.path.join(BASE_DIR, "FRONT"), static_url_path="/static")

@app.route("/")
def index():
    return render_template("index.html",)



@app.route("/perguntar", methods = ["POST"])
def question():
    
    'arrumar o formulário'
    data     = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    
    'manda pra llm'
    resposta = llm(question)
    

    return jsonify({"answer": resposta})