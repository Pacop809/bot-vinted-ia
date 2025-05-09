from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot IA Vinted OK"

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({"match": "model1", "scores": {"model1": 0.95}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
