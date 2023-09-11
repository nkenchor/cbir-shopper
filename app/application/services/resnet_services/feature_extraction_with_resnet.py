import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from app.application.services.resnet_services.resnet_loader import RESNET_50_MODEL,load_resnet_50_model
import numpy as np
from scipy.spatial import distance


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(img_path):
    """Extracts features from image using ResNet."""
    RESNET_50_MODEL = load_resnet_50_model()
    with torch.no_grad():
        image = Image.open(img_path)
        image = transform(image).unsqueeze(0)  # Removed .cuda() here
        features = RESNET_50_MODEL(image)
        features = features.squeeze().cpu().numpy()
    return features


def euclidean_distance(query_features, reference_features):
    """Compute the Euclidean distance between two feature vectors."""
    return np.linalg.norm(query_features - reference_features)



def cosine_similarity(query_features, reference_features):
    dot_product = np.dot(query_features, reference_features)
    norm_query = np.linalg.norm(query_features)
    norm_ref = np.linalg.norm(reference_features)
    return dot_product / (norm_query * norm_ref)

def manhattan_distance(query_features, reference_features):
    return np.sum(np.abs(query_features - reference_features))

def minkowski_distance(query_features, reference_features, p=2):
    return np.sum(np.abs(query_features - reference_features) ** p) ** (1/p)

def mahalanobis_distance(query_features, reference_features, inv_cov_matrix):
    return distance.mahalanobis(query_features, reference_features, inv_cov_matrix)

def hamming_distance(query_features, reference_features):
    return np.sum(query_features != reference_features)

def chi_square_distance(query_features, reference_features):
    return 0.5 * np.sum(((query_features - reference_features) ** 2) / (query_features + reference_features + 1e-6))

def histogram_intersection(query_histogram, reference_histogram):
    return np.sum(np.minimum(query_histogram, reference_histogram))
