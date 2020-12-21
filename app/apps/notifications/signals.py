import django.dispatch

task_created = django.dispatch.Signal(
    providing_args=["instance", "user_id"])
