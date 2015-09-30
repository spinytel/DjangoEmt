from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from authentication.models import Account
from .forms import UserForm, UserEditForm
import json


# Author : @mamun0024
def user_login(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/project/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'login.html')


@login_required
# Author : @mamun0024
def user_logout(request):
    logout(request)
    return render(request, 'login.html')


# Author : @mamun0024
def my_validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@login_required
# Author : @mamun0024
def get_logged_in_user_type(request):
    user_type = request.user.is_admin
    if user_type:
        return True
    else:
        return False


@login_required
# Author : @mamun0024
@api_view(['GET', 'POST', ])
def api_user_type(request):
    user_type = request.user.is_admin
    return Response(user_type)


@login_required
# Author : @mamun0024
def get_logged_in_user_id(request):
    user_id = request.user.id
    return user_id


@login_required
# Author : @mamun0024
def user_create(request):
    user_type = get_logged_in_user_type(request)
    if user_type:
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
                    return HttpResponse("Please enter a valid Email Address.")
            else:
                return HttpResponseRedirect('/accounts/users/create/')

        form.submit = 'Add User'
        form.breadcrumb = 'User Add'
        return render(request, 'user.html', {'form': form, 'user_type': user_type})
    else:
        return HttpResponse("Permission Denied")


@login_required
# Author : @mamun0024
def user_edit(request, user_id):
    user_type = get_logged_in_user_type(request)
    if user_type:
        form = get_object_or_404(Account, pk=user_id)
        if request.POST:
            form = UserEditForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                if my_validate_email(form_data['email']):
                    pk = user_id
                    username = form_data['username']
                    email = form_data['email']
                    is_admin = form_data['is_admin'] == 'True'

                    Account.objects.filter(pk=pk).update(
                            username=username,
                            email=email,
                            is_admin=is_admin)
                    return HttpResponseRedirect('/accounts/users/')
                else:
                    return HttpResponse("Please enter a valid Email Address.")
            else:
                return HttpResponseRedirect('/accounts/users/'+user_id+'/edit/')

        data = {'username': form.username, 'email': form.email, 'is_admin': form.is_admin, 'user_pre_id': form.id}
        form = UserEditForm(data)
        form.submit = 'Update User'
        form.breadcrumb = 'User Edit'
        return render(request, 'user.html', {'form': form, 'user_type': user_type})
    else:
        logged_user_id = get_logged_in_user_id(request)
        #import pdb; pdb.set_trace()
        if logged_user_id == int(user_id):
            form = get_object_or_404(Account, pk=user_id)
            if request.POST:
                form = UserEditForm(request.POST)
                if form.is_valid():
                    form_data = form.cleaned_data
                    if my_validate_email(form_data['email']):
                        pk = user_id
                        username = form_data['username']
                        email = form_data['email']
                        Account.objects.filter(pk = pk).update(
                                username=username,
                                email=email)
                        return redirect('/accounts/users/')
                    else:
                        return HttpResponse("Please enter a valid Email Address.")
                else:
                    return HttpResponseRedirect('/accounts/users/'+user_id+'/edit/')

            data = {'username': form.username, 'email': form.email, 'is_admin': form.is_admin, 'user_pre_id': form.id}
            form = UserEditForm(data)
            form.submit = 'Update User'
            form.breadcrumb = 'User Edit'
            return render(request, 'user.html', {'form': form, 'user_type': user_type})
        else:
            return HttpResponse("Permission Denied")


@login_required
# Author : @mamun0024
@api_view(['GET', 'POST', ])
def api_user_data(request, user_id):
    user_type = get_logged_in_user_type(request)
    if user_type:
        user_data = Account.objects.filter(pk=user_id).values_list('id', 'username', 'email', 'is_admin')
    else:
        logged_user_id = get_logged_in_user_id(request)
        if logged_user_id == int(user_id):
            user_data = Account.objects.filter(pk=user_id).values_list('id', 'username', 'email', 'is_admin')
        else:
            return HttpResponse("Permission Denied")
    a = ['id', 'username', 'email', 'is_admin']
    data = {}
    for b in user_data:
        data = dict(zip(a, list(b)))
    return Response(data)


@login_required
# Author : @mamun0024
def user_delete(request, user_id):
    user_type = get_logged_in_user_type(request)
    if user_type:
        data = get_object_or_404(Account, pk=user_id)
        data.delete()
        return redirect('/accounts/users/')
    else:
        return HttpResponse("Permission Denied")


@login_required
# Author : @mamun0024
def user_all_list(request):
    user_type = get_logged_in_user_type(request)
    if user_type:
        user_details = Account.objects.all().values()
    else:
        user_id = get_logged_in_user_id(request)
        user_details = Account.objects.filter(pk=user_id).values()

    return render(request, 'user_all.html', {'user_details': user_details})


@login_required
# Author : @mamun0024
@api_view(['GET', 'POST', ])
def api_user_all(request):
    user_type = get_logged_in_user_type(request)

    '''
    if user_type:
        user_details = Account.objects.all().values_list('id', 'username', 'email', 'is_admin')
    else:
        user_id = get_logged_in_user_id(request)
        user_details = Account.objects.filter(pk=user_id).values_list('id', 'username', 'email', 'is_admin')

    a = ['id', 'name', 'email', 'is_admin']
    d = []
    for b in user_details :
        d.append(dict(zip(a, list(b))))

    return Response(json.dumps(d))
    '''

    if user_type:
        user_details = Account.objects.all().values()
    else:
        user_id = get_logged_in_user_id(request)
        user_details = Account.objects.filter(pk=user_id).values()

    return Response(user_details)
