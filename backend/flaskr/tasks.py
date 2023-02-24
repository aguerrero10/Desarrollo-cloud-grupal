from celery import Celery
from celery.schedules import crontab

#app = Celery( 'tasks' , broker = 'redis://localhost:6379/0')
app = Celery( 'tasks' , broker = 'redis://localhost:6360/0')

#app.conf.beat_schedule = {
#    'add-every-30-seconds': {
#        'task': 'tasks.sumar',
#        'schedule': 10.0,
#        'args': (16, 16)
#    },
#}
#app.conf.timezone = 'UTC'


#@app.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, sumar.s(), name='add every 10')

#    sender.add_periodic_task(
#        crontab(minute="*"),
#        test.s('Happy Mondays!'),
#    )

@app.task(name="sumar")
def sumar():
    print('Se sumaron los números')
    print("3")
    return 1 + 2

@app.task(name="test")
def test(arg):
    print(arg)
