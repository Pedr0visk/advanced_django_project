import django.dispatch

bop_created_or_updated = django.dispatch.Signal(providing_args=["instance", "created"])
