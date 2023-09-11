import os
import tensorflow as tf
import torch
import torchvision.models as models
from app.infrastructure.utilities.service_utils import ModelDownloader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESNETMODEL_101_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', 'resnet101_weights_tf_dim_ordering_tf_kernels.h5')
RESNETMODEL_50_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', 'resnet50-0676ba61.pth')

RESNET_101_MODEL = None
RESNET_50_MODEL = None

MODELS = {
    'resnet101_weights_tf_dim_ordering_tf_kernels.h5': 'https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet101_weights_tf_dim_ordering_tf_kernels.h5',
    'resnet50-0676ba61.pth': 'https://download.pytorch.org/models/resnet50-0676ba61.pth'
}

def model_exists(model_path):
    return os.path.isfile(model_path)

def download_resnet_models(base_directory=BASE_DIR):
    downloader = ModelDownloader(base_dir=base_directory, model_folder='model/pretrained')
    for model_name, url in MODELS.items():
        if not model_exists(os.path.join(BASE_DIR, 'model', 'pretrained', model_name)):
            downloader.download(model_name, url)

def load_resnet_50_model():
    global RESNET_50_MODEL
    if RESNET_50_MODEL is None:
        RESNET_50_MODEL = models.resnet50(pretrained=False)
        RESNET_50_MODEL.load_state_dict(torch.load(RESNETMODEL_50_PATH, map_location=torch.device('cpu')))
        RESNET_50_MODEL = RESNET_50_MODEL.eval()
        modules = list(RESNET_50_MODEL.children())[:-1]
        RESNET_50_MODEL = torch.nn.Sequential(*modules)
    return RESNET_50_MODEL

def load_resnet_101_model():
    global RESNET_101_MODEL
    if RESNET_101_MODEL is None:
        RESNET_101_MODEL = tf.keras.applications.ResNet101(weights=None)
        RESNET_101_MODEL.load_weights(RESNETMODEL_101_PATH)
    return RESNET_101_MODEL

def get_or_load_resnet_models():
    download_resnet_models()
    model_50 = load_resnet_50_model()
    model_101 = load_resnet_101_model()
    return model_50, model_101

if __name__ == "__main__":
    model_50, model_101 = get_or_load_resnet_models()
    print("ResNet models loaded successfully!")
