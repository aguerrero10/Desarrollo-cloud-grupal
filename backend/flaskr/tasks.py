from celery import Celery
import zipfile
import tarfile
import py7zr
import os
from os.path import basename

from flask_mail import Mail, Message
import psycopg2

# Mail
mail = Mail()

app = Celery( 'tasks' , broker = 'redis://localhost:6379/0')
# app = Celery( 'tasks' , broker = 'redis://localhost:6360/0')

# Funciones
def enviarcorreo(correo_destino):
    print('Enviando correo')
    msg = Message(subject='Prueba 2!',
                    recipients=[correo_destino],
                    body = 'Se ha comprimido su archivo!'
                    )
    mail.send(msg)

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


def compresion_correo():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(ROOT_DIR)
    # Conexion a la base de datos
    try:
        connection = psycopg2.connect(
            host='proyecto.ckh1hljhxmxq.us-east-1.rds.amazonaws.com',
            user='postgres',
            password='postgres',
            database='tareas'
        )
        print("Conexion exitosa")
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT "fileName", "newFormat", status, "pathOriginal", "pathConverted", "user"
                        FROM public.task
                        WHERE status = 'UPLOADED';
                    """)
        rows = cursor.fetchall()
        # print(rows[0])
        for row in rows:
            compressfile(file_to_compress = row[0],ROOT_DIR= ROOT_DIR, compression_type = row[1])
            cursor.execute("""
                        UPDATE public.task SET status='PROCESSED'
                        WHERE "fileName"=%s;
                        """, [row[0]])
            connection.commit()
            
            # Correo del usuario:
            cursor.execute("""
                           SELECT email
                           FROM public."user"
                           WHERE id = %s;
                           """, [row[5]])
            correo = cursor.fetchall()
            correo_destino = correo[0][0]
            enviarcorreo(correo_destino=correo_destino)            
            print('Correo enviado!')
            
    except Exception as ex:
        print(ex)

    finally:
        connection.close()
        print("Conexión finalizada")
    

@app.task(name="sumar")
def sumar():
    print('Se sumaron los números')
    print("3")

    return 1 + 2




    
    