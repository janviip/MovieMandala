from pathlib import Path

# Path to artifacts folder (will be created when ML teammate trains the model)
ARTIFACTS_PATH = Path(__file__).parent.parent.parent / "artifacts"

recommender = None

def load_recommender():
    global recommender
    try:
        from app.services.ml.tfidf_recommender import MovieRecommender
        recommender = MovieRecommender.load(ARTIFACTS_PATH)
        print("✅ ML recommender loaded successfully!")
    except Exception as e:
        print(f"⚠️ ML recommender not available yet: {e}")
        recommender = None

def get_recommendations(tmdb_id: int, k: int = 10):
    if recommender is None:
        return []
    try:
        return recommender.recommend_by_tmdb_id(tmdb_id, k=k)
    except Exception as e:
        print(f"Recommendation error: {e}")
        return []