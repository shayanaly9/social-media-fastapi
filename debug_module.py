import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from imagekitio.models import UploadFileRequestOptions

print(f"Type of UploadFileRequestOptions: {type(UploadFileRequestOptions)}")
print(f"Dir of UploadFileRequestOptions: {dir(UploadFileRequestOptions)}")
