import os
import pickle
import numpy as np

# Folder to store face embeddings
FACES_DIR = "data/faces"
os.makedirs(FACES_DIR, exist_ok=True)


# 🔹 Save embedding (dummy for now)
def register_face(roll_no: str, image: np.ndarray) -> dict:
    """Register a student's face (stores dummy embedding for deployment)"""
    try:
        # Dummy embedding (since no DeepFace)
        embedding = np.random.rand(128)

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


# 🔹 Demo face recognition (NO DeepFace)
def recognize_face(image, threshold=0.72):
    """Simple demo face recognition (for deployment)"""
    try:
        all_embeddings = load_all_embeddings()

        # No students registered
        if not all_embeddings:
            return {"recognized": False, "confidence": 0}

        # Pick first student (demo)
        best_match = list(all_embeddings.keys())[0]

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
