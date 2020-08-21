from django.shortcuts import redirect
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # messages.info(request, 'Only managers can access this page, you are logged as %s' %
                # request.user.username)
                return redirect('%s?next=%s' % ('/manager/unauthorized/', request.path))

        return wrapper_func