from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render
from .models import Project
from .forms import ProjectForm
# Create your views here.
"""
def project(request, question_id):
    try:
        project = Project.objects.get()
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'project/detail.html', {'question': question})
"""
def project_create(request, template_name='project/project_form.html'):

    if request.POST:
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return HttpResponse("ok")
        else:
            context = {
                'project_form': project_form
            }
    else:
        context = {
            'project_form': ProjectForm(),
        }
    return render_to_response(template_name, context, context_instance = RequestContext(request))

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

def project_lists(request,template_name="project/lists.html")
    projects = Project.objects.all()
    context
