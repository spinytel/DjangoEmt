from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.POST:
        # Gather the email and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the email/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(email=email, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/project/all/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')
