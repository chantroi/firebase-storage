from firebase_admin import credentials, initialize_app, storage
import os

cred = credentials.Certificate("collection-e0cec-3581ea27bf62.json")
initialize_app(cred, {'storageBucket': 'collection-e0cec.appspot.com'})
bucket = storage.bucket()

def list_files():
    blobs = bucket.list_blobs()
    files = [file.name for file in blobs]
    return files

def upload_name(file_name):
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
    blob.make_public()
    os.remove(file_name)
    return blob.public_url

def upload_file(file_path, file_name):
    blob = bucket.blob(file_name)
    blob.upload_from_file(file_path)
    blob.make_public()
    return blob.public_url

def upload_bytes(file_data, file_name, content_type):
    blob = bucket.blob(file_name)
    blob.upload_from_string(file_data, content_type=content_type)
    blob.make_public()
    return blob.public_url

def open_file(file_name):
    return bucket.blob(file_name)

def get_file(file_name):
    blob = bucket.blob(file_name)
    blob.make_public()
    return blob.public_url

def download_bytes(file_name):
    blob = bucket.blob(file_name)
    return blob.download_as_bytes()

def delete_file(file_name):
    blob = bucket.blob(file_name)
    blob.delete()

    