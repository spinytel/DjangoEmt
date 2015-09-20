from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from authentication.models import Account
from .forms import UserForm, UserEditForm


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


def my_validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@login_required
def user_create(request):
    form = UserForm()

    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if my_validate_email(data['email']):
                if data['password'] and data['confirm_password'] and data['password'] == data['confirm_password']:
                    form.save()
                    return redirect('/accounts/users/')
                else:
                    return HttpResponse('Password Mismatch')
            else:
                return HttpResponse("Please enter valid Email Address.")

    form.submit = 'Add User'
    form.breadcrumb = 'User Add'
    return render(request, 'user.html', {'form': form})


@login_required
def user_edit(request, user_id):
    form = get_object_or_404(Account, pk=user_id)

    if request.POST:
        form = UserEditForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if my_validate_email(form_data['email']):
                pk = form_data['user_pre_id']
                Account.objects.filter(pk = pk).update(
                        username=form_data['username'],
                        email=form_data['email'],
                        is_admin=form_data['is_admin'])
                return redirect('/accounts/users/')
            else:
                return HttpResponse("Please enter valid Email Address.")

    data = {'username': form.username, 'email': form.email, 'is_admin': form.is_admin, 'user_pre_id': form.id}
    form = UserEditForm(data)
    form.submit = 'Update User'
    form.breadcrumb = 'User Edit'
    return render(request, 'user.html', {'form': form})


@login_required
def user_delete(request, user_id):
    data = get_object_or_404(Account, pk=user_id)
    data.delete()
    return redirect('/accounts/users/')


@login_required
def user_all(request):
    user_details = Account.objects.all()
    return render(request, 'user_all.html', {'user_details': user_details})
