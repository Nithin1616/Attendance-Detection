import os
import numpy as np
import pickle
from deepface import DeepFace

FACES_DIR = "data/faces"
os.makedirs(FACES_DIR, exist_ok=True)

MODEL_NAME = "Facenet512"
DETECTOR = "opencv"


def register_face(roll_no: str, image: np.ndarray) -> dict:
    """Register a student face and save embedding."""
    try:
        embedding_obj = DeepFace.represent(
            img_path=image,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR,
            enforce_detection=True
        )
        embedding = embedding_obj[0]["embedding"]
        path = os.path.join(FACES_DIR, f"{roll_no}.pkl")
        with open(path, "wb") as f:
            pickle.dump(embedding, f)
        return {"success": True, "path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_all_embeddings() -> dict:
    """Load all registered face embeddings from disk."""
    embeddings = {}
    for fname in os.listdir(FACES_DIR):
        if fname.endswith(".pkl"):
            roll_no = fname.replace(".pkl", "")
            with open(os.path.join(FACES_DIR, fname), "rb") as f:
                embeddings[roll_no] = pickle.load(f)
    return embeddings


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recognize_face(image: np.ndarray, threshold: float = 0.72) -> dict:
    """Recognize a face from image against all registered embeddings."""
    try:
        embedding_obj = DeepFace.represent(
            img_path=image,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR,
            enforce_detection=True
        )
        query_embedding = embedding_obj[0]["embedding"]
        all_embeddings = load_all_embeddings()

        best_match = None
        best_score = -1

        for roll_no, stored_emb in all_embeddings.items():
            score = cosine_similarity(query_embedding, stored_emb)
            if score > best_score:
                best_score = score
                best_match = roll_no

        if best_score >= threshold:
            return {
                "recognized": True,
                "roll_no": best_match,
                "confidence": round(float(best_score), 4)
            }
        else:
            return {"recognized": False, "confidence": round(float(best_score), 4)}

    except Exception as e:
        return {"recognized": False, "error": str(e)}


def delete_face(roll_no: str) -> dict:
    """Delete a student's face embedding."""
    path = os.path.join(FACES_DIR, f"{roll_no}.pkl")
    if os.path.exists(path):
        os.remove(path)
        return {"success": True}
    return {"success": False, "error": "Embedding not found"}


def face_registered(roll_no: str) -> bool:
    """Check if a face embedding exists for a student."""
    path = os.path.join(FACES_DIR, f"{roll_no}.pkl")
    return os.path.exists(path)