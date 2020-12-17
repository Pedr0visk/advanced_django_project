import django.dispatch

schemas_compare_event = django.dispatch.Signal(
    providing_args=["instance", "created", "user"])

schemas_compare_calc_done = django.dispatch.Signal(
    providing_args=["instance", "created", "user"])
