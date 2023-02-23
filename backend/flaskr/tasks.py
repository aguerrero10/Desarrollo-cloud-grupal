from celery import Celery

#app = Celery( 'tasks' , broker = 'redis://localhost:6379/0')
app = Celery( 'tasks' , broker = 'redis://localhost:6360/0')


@app.task
def sumar(x,y):
    print('Se sumaron los números')
    return x + y