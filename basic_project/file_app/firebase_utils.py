import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings
import uuid

cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'storageBucket': settings.FIREBASE_STORAGE_BUCKET,
    })

bucket = storage.bucket()

def upload_file_to_firebase(file):
    blob = bucket.blob(f"uploads/{uuid.uuid4()}_{file.name}")
    blob.upload_from_file(file, content_type=file.content_type)
    blob.make_public()
    return blob.public_url
