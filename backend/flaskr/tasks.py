from celery import Celery
import zipfile
import tarfile
#import py7zr
import os
from os.path import basename


#app = Celery( 'tasks' , broker = 'redis://localhost:6379/0')
app = Celery( 'tasks' , broker = 'redis://localhost:6360/0')


@app.task(name="sumar")
def sumar():
    print('Se sumaron los números')
    print("3")
    return 1 + 2

@app.task(name="test")
def test(arg):
    print(arg)

@app.task(name="compressfile")
def compressfile():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print("test")
    pass