from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .models import Project
from authentication.models import Account
from .forms import ProjectForm
from django.db.models import Q
# Create your views here.
"""
def project(request, question_id):
    try:
        project = Project.objects.get()
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'project/detail.html', {'question': question})
"""
def project_create(request, template_name='project/create.html'):
    form = ProjectForm()
    leaders = Account.objects.filter(~Q(email= "hrd@spinytel.com"))
    members = Account.objects.filter(is_admin = False).order_by('id')

    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(ok)

    return render(request, template_name, {'form': form, 'leaders': leaders, 'members':members})

def project_edit(request,project_id,template_name="project/project_form.html"):
    project = Project.objects.get(pk=int(project_id))
    context = {
        'project_form': ProjectForm(instance=project),
    }
    project_form = ProjectForm(request.POST)
    if project_form.is_valid():
        project_form.save()
        return HttpResponse("ok")
    return render_to_response(template_name, context, context_instance = RequestContext(request))
