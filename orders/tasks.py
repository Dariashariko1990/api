# Create your tasks here

from celery import shared_task


@shared_task(name='sum-of-two-numbers')
def add(x, y):
    print(x + y)