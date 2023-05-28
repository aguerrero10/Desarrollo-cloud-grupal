from flask import Flask, request
from google.cloud.sql.connector import Connector, IPTypes
from google.cloud import storage
import base64
import json
import os
import tempfile
import ssl
import smtplib
from email.message import EmailMessage
# Compressing libraries
import zipfile
import tarfile
import py7zr
# Database libraries
import sqlalchemy
import pg8000

app = Flask(__name__)

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    instance_connection_name = 'project:region:instance'
    db_user = 'user'
    db_pass = 'password'
    db_name = 'dbname'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # Cloud SQL Python Connector 
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool

@app.route("/", methods=["POST"])
def index():

    # Variables creation
    jsondata = {}
    id_user = ""
    compression_type = ""
    user_email = ""

    envelope = request.get_json()
    
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope: 
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400
    
    # Decode the Pub/Sub message.
    pubsub_message = envelope["message"]

    pubsub_data = base64.b64decode(pubsub_message["data"]).decode("utf-8")

    # Convert event string to object
    jsondata = json.loads(pubsub_data)

    #print("file path: ", jsondata['name'])

    # Extracting the required data from the event message
    file_path = jsondata['name'] 
    bucket_name = jsondata['bucket'] 

    try:
        id_user = jsondata["metadata"].get("id_user")
        #print("The user id is: ", id_user)
    except Exception as e:
        print("Something went wrong retrieving the user id: ", e)

    try:
        compression_type = jsondata["metadata"].get("new_format")
        #print("The compression format is: ", compression_type)
    except Exception as e:
        print("Something went wrong retrieving the compression format: ", e)

    # /Start/ --------------- Database connection --------------
    
    pool = connect_with_connector()

    # connect to connection pool
    with pool.connect() as db_conn:
        data = { 'x' : id_user }
        # query and fetch ratings table
        results = db_conn.execute(sqlalchemy.text("SELECT email FROM public.user WHERE id = :x"), data).fetchall()
        #print(results)
        try:
            #print("User email is: ", str(results[0][0]))
            user_email = str(results[0][0])
        except Exception as e:
            print("Wrong: ", e)
        db_conn.close()

    # /End/ --------------- Database connection --------------

    # Extracting the file names
    file_name_ext = file_path.rsplit('/')[-1]
    #print("Filename with extension: ", file_name_ext)
    file_name = file_name_ext.rsplit('.')[0]
    #print("Filename: ", file_name)

    # Temporal downloaded file
    tmpdir = tempfile.gettempdir()
    temp_downloaded = os.path.join(tmpdir, str(file_name_ext))
    #print("Temp path to download the file: ", temp_downloaded)

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    file_blob = storage.Blob(file_path, bucket)

    # Download the file to the temporal folder
    file_blob.download_to_filename(temp_downloaded)

    out_file = ""
    source_file = os.path.join(tmpdir, str(file_name_ext))
    #print("Source path: ", source_file)


    if(compression_type == "ZIP"):
        try:
            out_file = os.path.join(tmpdir, str(file_name) + ".zip")
            with zipfile.ZipFile(out_file, mode="w") as archive:
                archive.write(source_file, file_name_ext, compress_type=zipfile.ZIP_DEFLATED)
                #print("Compresion completed!")
        except zipfile.BadZipFile as error:
            print(error)

    elif (compression_type == "SEVENZIP"):
        try:
            out_file = os.path.join(tmpdir, str(file_name) + ".7z")
            with py7zr.SevenZipFile(out_file, "w") as archive:
                archive.writeall(source_file, file_name_ext)
                #print("Compresion completed!")
        except py7zr.Bad7zFile as error:
            print(error)

    elif (compression_type == "TARBZ2"):
        try:
            out_file = os.path.join(tmpdir, str(file_name) + ".tar.bz2")
            with tarfile.open(out_file, "w:bz2") as archive:
                archive.add(source_file, file_name_ext)
                #print("Compresion completed!")
        except tarfile.TarError as error:
            print(error)

    #print("Output path: ", out_file)

    extension = ""
    # Push file to Cloud Storage
    if(compression_type == "ZIP"):
        extension = ".zip"
    elif (compression_type == "SEVENZIP"):
        extension = ".7z"
    elif (compression_type == "TARBZ2"):
        extension = ".tar.bz2"

    blob = bucket.blob("files/compressed/" + str(file_name) + extension)
    blob.upload_from_filename(out_file)

    # /Start/ --------------- Send email --------------
    # Define email sender and receiver
    email_sender = 'desarrollocloudm@gmail.com'
    email_password = 'xyzxyzxyzxyzxyz'
    email_receiver = user_email

    # Set the subject and body of the email
    subject = 'Tarea procesada: ' + str(file_name) 
    body = """
    Se ha comprimido exitosamente su archivo!
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    #print('Se creo objeto mensaje de correo')
    
    # ---- Commented for testing
    # Add SSL (layer of security)
    context = ssl.create_default_context()
    
    # Log in and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.set_debuglevel(1)
            smtp.ehlo()
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    except Exception as e:
        msg = "There was an error sending the mail"
        print("Exception: ", e)
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 500
    
    #print('Email sent!')
    # /End/ --------------- Send email --------------
    
    # connect to connection pool
    with pool.connect() as db_conn:
        data={'x':id_user, 'y':file_name_ext, 'z':'PROCESSED'}
        # query and fetch ratings table
        db_conn.execute(sqlalchemy.text('UPDATE public.task SET status= :z WHERE "user" = :x AND "fileName" = :y'), data)
        db_conn.commit()
        db_conn.close()

    #print("DB Update completed")
    
    return f"Success file compression: {file_name_ext}", 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)