from celery import Celery
import zipfile
import tarfile
import py7zr
import os
from os.path import basename



#app = Celery( 'tasks' , broker = 'redis://localhost:6379/0')
app = Celery( 'tasks' , broker = 'redis://localhost:6360/0')


@app.task(name="sumar")
def sumar():
    print('Se sumaron los números')
    print("3")

    return 1 + 2

# Función asíncrona de compresión
@app.task(name="compressfile")
def compressfile(file_to_compress, ROOT_DIR, compression_type):
    source_file = os.path.join(ROOT_DIR, str(file_to_compress))
    
    if(compression_type == "ZIP"):
        try:
            out_file = os.path.join(ROOT_DIR, str(file_to_compress) + ".zip")
            with zipfile.ZipFile(out_file, mode="w") as archive:
                archive.write(source_file, basename(source_file), compress_type=zipfile.ZIP_DEFLATED)
        except zipfile.BadZipFile as error:
            print(error)
    
    elif (compression_type == "SEVENZIP"):
        try:
            out_file = os.path.join(ROOT_DIR, str(file_to_compress) + ".7z")
            with py7zr.SevenZipFile(out_file, "w") as archive:
                archive.writeall(source_file, basename(source_file))
        except py7zr.Bad7zFile as error:
            print(error)
    
    elif (compression_type == "TARBZ2"):
        try:
            out_file = os.path.join(ROOT_DIR, str(file_to_compress) + ".tar.bz2")
            with tarfile.open(out_file, "w:bz2") as archive:
                archive.add(source_file, basename(source_file))
        except tarfile.TarError as error:
            print(error)
    
    else:
        print("Compression Type Unavailable")

    