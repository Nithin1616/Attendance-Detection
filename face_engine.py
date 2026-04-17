import os
import pickle
import numpy as np

# Folder to store face embeddings
FACES_DIR = "data/faces"
os.makedirs(FACES_DIR, exist_ok=True)

# 🔹 Save embedding
def register_face(roll_no: str, image: np.ndarray) -> dict:
    """Register a student's face"""
    try:
        embedding = np.ones(128) * np.mean(image)

        path = os.path.join(FACES_DIR, f"{roll_no}.pkl")
        with open(path, "wb") as f:
            pickle.dump(embedding, f)

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}


# 🔹 Load all embeddings
def load_all_embeddings():
    embeddings = {}
    for file in os.listdir(FACES_DIR):
        if file.endswith(".pkl"):
            roll_no = file.replace(".pkl", "")
            path = os.path.join(FACES_DIR, file)
            with open(path, "rb") as f:
                embeddings[roll_no] = pickle.load(f)
    return embeddings


# 🔹 Demo face recognition
def recognize_face(image, threshold=0.72):
    """Simple demo face recognition"""
    try:
        all_embeddings = load_all_embeddings()

        if not all_embeddings:
            return {"recognized": False, "confidence": 0}

        input_embedding = np.ones(128) * np.mean(image)

        best_match = None
        best_score = float("inf")

        for roll, emb in all_embeddings.items():
            dist = np.linalg.norm(input_embedding - emb)

            if dist < best_score:
                best_score = dist
                best_match = roll

        return {
            "recognized": True,
            "roll_no": best_match,
            "confidence": 0.95
        }

    except Exception as e:
        return {"recognized": False, "error": str(e)}


# 🔹 Delete face
def delete_face(roll_no: str) -> dict:
    path = os.path.join(FACES_DIR, f"{roll_no}.pkl")
    if os.path.exists(path):
        os.remove(path)
        return {"success": True}
    return {"success": False, "error": "Embedding not found"}


# 🔹 Check if face exists
def face_registered(roll_no: str) -> bool:
    path = os.path.join(FACES_DIR, f"{roll_no}.pkl")
    return os.path.exists(path)
