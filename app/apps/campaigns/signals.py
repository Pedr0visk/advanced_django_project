import django.dispatch

schema_created_or_updated = django.dispatch.Signal(
    providing_args=["instance", "created", "user_id"])

event_created_or_updated = django.dispatch.Signal(
    providing_args=["instance", "created"])
