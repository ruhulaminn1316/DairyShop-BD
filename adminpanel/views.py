from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# শুধু superuser বা staff access করতে পারবে
def admin_only(user):
    return user.is_staff

@login_required
@user_passes_test(admin_only)
def dashboard_home(request):
    return render(request, 'adminpanel/dashboard_home.html')
