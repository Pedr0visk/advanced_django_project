import django.dispatch

task_initiated = django.dispatch.Signal(
    providing_args=["instance", "completed", "user_id"])

task_completed = django.dispatch.Signal(
    providing_args=["instance", "completed", "user_id"])
