from flask import Flask, request, jsonify
from PIL import Image
import torch
import clip
import torchvision.transforms as transforms
import os

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Chemin vers les modèles enregistrés (à adapter si tu as plusieurs)
MODEL_IMAGES = {
    "model1": "reference/model1.jpg",  # Exemple d’image de référence
}

# Préparer les images de référence une fois au début
def load_reference_features():
    features = {}
    for model_name, path in MODEL_IMAGES.items():
        image = preprocess(Image.open(path)).unsqueeze(0).to(device)
        features[model_name] = model.encode_image(image).detach()
    return features

reference_features = load_reference_features()

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "no image"}), 400

    image = Image.open(request.files["file"])
    image_input = preprocess(image).unsqueeze(0).to(device)
    image_features = model.encode_image(image_input)

    results = {}
    for model_name, ref_feat in reference_features.items():
        similarity = torch.cosine_similarity(image_features, ref_feat).item()
        results[model_name] = round(similarity, 3)

    best_match = max(results, key=results.get)
    return jsonify({"match": best_match, "scores": results})

@app.route("/")
def home():
    return "Bot IA Vinted OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
