import io
from os.path import join 
from google.cloud import storage

bucket_name = 'proyecto-dsc'
path_to_private_key = './dsc-proyecto-b6565f206c96.json'


#Cargar un archivo en cloud storage
#Recibe file (en formato bytes) y la ruta/nombre donde debe almacenarse
def upload_file_bucket(file, blob_name, id_user, new_format):
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)
    bucket = storage.Bucket(client, bucket_name)
    blob = bucket.blob(blob_name)

    metadata = {'id_user':id_user, 'new_format':new_format}
    blob.metadata = metadata

    blob.upload_from_file(file, content_type=file.content_type)


#Descargar un archivo de cloud storage, devuelve el archivo en formato Bytes
#Recibe la ruta/nombre donde se encuentra
def download_file_bucket(blob_name):
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)
    bucket = storage.Bucket(client, bucket_name)
    blob = bucket.blob(blob_name)

    file = io.BytesIO()
    blob.download_to_file(file)
    file.seek(0)
    return file


#Eliminar un archivo de cloud storage
#Recibe la ruta/nombre donde se encuentra
def delete_file_bucket(blob_name):
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)
    bucket = storage.Bucket(client, bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()


#Verificar si un archivo existe en cloud storage
#Recibe la ruta/nombre donde se hará la verificación
def exists_file_bucket(blob_name):
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)
    bucket = storage.Bucket(client, bucket_name)
    blob = bucket.blob(blob_name)

    return blob.exists()
