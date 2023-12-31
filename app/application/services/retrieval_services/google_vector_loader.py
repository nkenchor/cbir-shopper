from app.infrastructure.utilities.service_utils import ModelDownloader
import os
import gensim

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOADED_MODEL = None

NLP_NAME = 'GoogleNews-vectors-negative300.bin'
GOOGLENEWS_VECTORS_URL = "https://storage.googleapis.com/cbir-server-01/GoogleNews-vectors-negative300.bin"
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', NLP_NAME)

def model_exists():
    return os.path.isfile(MODEL_PATH)

def download_googlenews_vector(base_directory=BASE_DIR):
    global LOADED_MODEL
    
    # Initialize the ModelDownloader with the 'model/pretrained' folder path
    downloader = ModelDownloader(base_dir=base_directory, model_folder=os.path.join(BASE_DIR, 'model', 'pretrained'))
    downloader.download(NLP_NAME, GOOGLENEWS_VECTORS_URL)
    LOADED_MODEL = load_google_model()

def load_google_model():
    if LOADED_MODEL is not None:
        return LOADED_MODEL
    try:
        return gensim.models.KeyedVectors.load_word2vec_format(MODEL_PATH, binary=True)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_or_load_nlp_model():
    global LOADED_MODEL
    if not model_exists():
        download_googlenews_vector()
    if LOADED_MODEL is None:
        LOADED_MODEL = load_google_model()
    return LOADED_MODEL

if __name__ == "__main__":
    model = get_or_load_nlp_model()
    print("Google News Vectors loaded successfully!")
