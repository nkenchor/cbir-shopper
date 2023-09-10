from app.infrastructure.utilities.service_utils import ModelDownloader
import os
import gensim

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NLP_MODEL = None

NLP_NAME = 'GoogleNews-vectors-negative300.bin'
GOOGLENEWS_VECTORS_URL = "http://vectors.nlpl.eu/repository/11/1.zip"
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'pretrained')

def download_googlenews_vector(base_directory=BASE_DIR):
    global NLP_MODEL
    
    # Initialize the ModelDownloader with the 'model/pretrained' folder path
    downloader = ModelDownloader(base_dir=base_directory, model_folder=MODEL_PATH)
    downloader.download(NLP_NAME, GOOGLENEWS_VECTORS_URL)
    NLP_MODEL = load_model(f"{MODEL_PATH}/{NLP_NAME}")

def load_model(model_path):
    try:
        return gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def get_model():
    global NLP_MODEL
    if NLP_MODEL is None:
        NLP_MODEL = load_model(f"{MODEL_PATH}/{NLP_NAME}")
    return NLP_MODEL
