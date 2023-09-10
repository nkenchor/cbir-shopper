import os
import tensorflow as tf
import torch
import torchvision.models as models
from app.infrastructure.utilities.service_utils import ModelDownloader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESNETMODEL_101_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', 'resnet101_weights_tf_dim_ordering_tf_kernels.h5')
RESNETMODEL_50_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', 'resnet50-0676ba61.pth')

RESNET_101_MODEL = None  # Initialize the global model variable
RESNET_50_MODEL = None  # This model is not used in other parts of your provided code. Should it be globally accessible?

MODELS = {
    'resnet101_weights_tf_dim_ordering_tf_kernels.h5': 'https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet101_weights_tf_dim_ordering_tf_kernels.h5',
    'resnet50-0676ba61.pth': 'https://download.pytorch.org/models/resnet50-0676ba61.pth'
}

def download_resnet_models(base_directory=BASE_DIR):
    downloader = ModelDownloader(base_dir=base_directory, model_folder='model/pretrained')
    for model_name, url in MODELS.items():
        downloader.download(model_name, url)
    load_resnet_50_model()
    global RESNET_101_MODEL
    RESNET_101_MODEL = tf.keras.applications.ResNet101(weights=None)
    RESNET_101_MODEL.load_weights(RESNETMODEL_101_PATH)
    

def load_resnet_50_model():
    global RESNET_50_MODEL
    RESNET_50_MODEL = models.resnet50(pretrained=False)
    RESNET_50_MODEL.load_state_dict(torch.load(RESNETMODEL_50_PATH, map_location=torch.device('cpu')))
    RESNET_50_MODEL = RESNET_50_MODEL.eval()
    modules = list(RESNET_50_MODEL.children())[:-1]
    RESNET_50_MODEL = torch.nn.Sequential(*modules)
    return RESNET_50_MODEL

def load_resnet_101_model():
    if RESNET_101_MODEL is None:
        raise ValueError("Model has not been initialized. Download and load the model first.")
    return RESNET_101_MODEL