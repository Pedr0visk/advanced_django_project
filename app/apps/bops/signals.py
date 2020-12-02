import django.dispatch

bop_created = django.dispatch.Signal(providing_args=["instance", "created"])
