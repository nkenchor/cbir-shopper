import os
import sys

class ModelDownloader:
    def __init__(self, base_dir, model_folder='model'):
        self.base_dir = base_dir
        self.model_folder = os.path.join(base_dir, model_folder)
        
        # Ensure the model folder exists
        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

    def download(self, model_name, download_url):
        model_path = os.path.join(self.model_folder, model_name)

        if not os.path.exists(model_path):
            print(f"Downloading {model_name}...")

            if sys.platform == 'win32':
                # Windows
                cmd = f'powershell -c "Invoke-WebRequest -Uri {download_url} -OutFile {model_path}"'
            elif sys.platform in ['darwin', 'linux']:
                # MacOS and Linux
                cmd = f'wget -O {model_path} {download_url}'
            else:
                raise ValueError("Unsupported OS")

            exit_code = os.system(cmd)
            if exit_code == 0:
                print(f"{model_name} downloaded successfully.")
            else:
                print(f"Failed to download {model_name}. Exit code: {exit_code}")
        else:
            print(f"{model_name} already exists.")
