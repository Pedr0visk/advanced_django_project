import django.dispatch

task_initiated = django.dispatch.Signal(
    providing_args=["instance", "created", "user_id"])

task_completed = django.dispatch.Signal(
    providing_args=["instance", "created", "user_id"])
