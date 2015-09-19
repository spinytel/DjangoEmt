from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from .models import Project,ProjectFile,ProjectMember, MilestoneType, Milestone
from django.utils import timezone
import time
from django.utils.dateformat import DateFormat
from django.conf import settings
from authentication.models import Account
from .forms import ProjectForm, MilestoneForm, MilestoneEditForm,ProjectEditForm
from django.db.models import Q
import os
# Create your views here.

def projects(request):
    ps = [[a['id'],a['create_date'],a['name'],a['deadline']] for a in Project.objects.all().values()]
    lm = [[Account.objects.values_list('username',flat=True).filter(id=int(b['user_id'])) for b in ProjectMember.objects.select_related().filter(project_id__id=int(a[0])).filter(member_type=1).values()] for a in ps]
    nm = [[Account.objects.values_list('username',flat=True).filter(id=int(b['user_id'])) for b in ProjectMember.objects.select_related().filter(project_id__id=int(a[0])).filter(member_type=2).values()] for a in ps]

    projects = []
    k = ['project_id', 'create_date', 'name','deadline','leaders','members']
    for i in range(0,len(ps)) :
        a = ps[i]
        a.append(lm[i])
        a.append(nm[i])
        projects.append(dict(zip(k,a)))
    return render(request, 'project/lists.html',{'projects':projects})

def project_create(request, template_name='project/create.html'):
    proj_form = ProjectForm()
    leaders = Account.objects.filter(~Q(email= "hrd@spinytel.com"))
    members = Account.objects.filter(is_admin = False).order_by('id')

    if request.POST:

        proj_form = ProjectForm(request.POST,request.FILES)
        if proj_form.is_valid():
            form_data = proj_form.cleaned_data
            p_name = form_data['name']
            create_date = timezone.now()
            deadline = form_data['deadline']
            project_row = Project.objects.create(name=p_name,create_date=create_date,deadline=deadline,status='new')
            project_row.save()

            #project file process start
            latest = Project.objects.latest('id')
            proj_id = latest.pk
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            for file in request.FILES.getlist('project_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                dest = open(os.path.join(settings.MEDIA_ROOT, str(proj_id)+'_'+extn+'_'+file.name), 'wb')
                for chunk in file.chunks():
                    dest.write(chunk)
                    dest.close()

                file_name = file.name
                project_files = ProjectFile.objects.create(file_name=file_name,project_id=proj_id)
                project_files.save()

            #project and lead members process
            for lead_member in request.POST.getlist('lead_user_ID'):
                project_lead = ProjectMember.objects.create(project_id=proj_id,user_id=lead_member,member_type=1)

            for normal_member in request.POST.getlist('normal_user_ID'):
                project_member = ProjectMember.objects.create(project_id=proj_id,user_id=normal_member,member_type=2)

            return HttpResponseRedirect('/project/')
    proj_form.submit_val = 'Add Project'
    return render(request, template_name, {'proj_form': proj_form, 'leaders': leaders, 'members':members})


def project_edit(request,project_id,template_name="project/create.html"):
    #import pdb; pdb.set_trace()
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        project_files = ProjectFile.objects.filter(project_id=project_id).values_list('id', 'file_name')
        #import pdb; pdb.set_trace()
        selected_lead = ProjectMember.objects.filter(project_id=project_id).filter(member_type=1).values_list('user_id',flat=True)
        selected_member = ProjectMember.objects.filter(project_id=project_id).filter(member_type=2).values_list('user_id',flat=True)

        leaders = Account.objects.filter(~Q(email= "hrd@spinytel.com"))
        members = Account.objects.filter(is_admin = False).order_by('id')
    if request.POST:
        form = ProjectEditForm(request.POST,request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            p_id = form_data['project_update_id']
            p_name = form_data['name']
            create_date = timezone.now()
            deadline = form_data['deadline']
            project_row = Project.objects.filter(pk=p_id).update(name=p_name,deadline=deadline,status='new')

            ProjectMember.objects.filter(project_id=p_id).filter(member_type=1).delete()
            #project and lead members process
            for lead_member in request.POST.getlist('lead_user_ID'):
                project_lead = ProjectMember.objects.create(project_id=p_id,user_id=lead_member,member_type=1)

            ProjectMember.objects.filter(project_id=p_id).filter(member_type=2).delete()
            for normal_member in request.POST.getlist('normal_user_ID'):
                project_member = ProjectMember.objects.create(project_id=p_id,user_id=normal_member,member_type=2)

            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            for file in request.FILES.getlist('project_file'):
                """
                while os.path.exists(os.path.join(settings.MEDIA_ROOT, file.name)):
                    file.name = '_' + file.name
                    import pdb; pdb.set_trace()
                """
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                dest = open(os.path.join(settings.MEDIA_ROOT, str(p_id)+'_'+extn+'_'+file.name), 'wb')
                for chunk in file.chunks():
                    dest.write(chunk)
                    dest.close()

                file_name = file.name
                project_files = ProjectFile.objects.create(file_name=file_name,project_id=p_id)
                project_files.save()

            #import pdb; pdb.set_trace()
            #project_row.save()
            return HttpResponseRedirect("/project/")

    data = {'name':project.name,'deadline':DateFormat(project.deadline).format('Y-m-d'),'project_update_id':project.id}

    proj_form = ProjectEditForm(data)
    proj_form.submit_val = 'Update Project'  
    #import pdb; pdb.set_trace()
    return render_to_response(template_name, {'proj_form':proj_form, 'leaders': leaders, 'members':members, 'selected_lead': selected_lead,'selected_member':selected_member,'project_files':project_files}, context_instance = RequestContext(request))


def milestone_all(request, project_id, template_name='milestone/milestone_all.html'):
    milestone_details = Milestone.objects.filter(project_id=project_id)
    return render(request, template_name, {'milestone_details': milestone_details})


def milestone_create(request, project_id, template_name='milestone/milestone_create.html'):
    form = MilestoneForm(passing_id=project_id)

    if request.POST:
        form = MilestoneForm(request.POST, passing_id=project_id)
        if form.is_valid():
            form = form.cleaned_data
            form = Milestone.objects.create(
                title=form['title'],
                description=form['description'],
                start_date=form['start_date'],
                due_date=form['due_date'],
                budget=form['budget'],
                project_id=form['project_id'],
                user_id=form['m_responsible'],
                type_id=form['m_type'])
            form.save()
            return HttpResponse('OK')

    return render(request, template_name, {'form': form})


def milestone_edit(request, project_id, milestone_id, template_name='milestone/milestone_edit.html'):
    form = MilestoneEditForm(passing_milestone_id=milestone_id)

    if request.POST:
        form = MilestoneEditForm(request.POST, passing_milestone_id=milestone_id)
        if form.is_valid():
            form = form.cleaned_data
            Milestone.objects.filter(pk = milestone_id).update(
                title=form['title'],
                description=form['description'],
                start_date=form['start_date'],
                due_date=form['due_date'],
                budget=form['budget'],
                project_id=form['project_id'],
                user_id=form['m_responsible'],
                type_id=form['m_type'])
            return HttpResponse('OK')
        else:
            return HttpResponse(form)

    return render(request, template_name, {'form': form})
