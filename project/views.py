from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from .models import Project, ProjectFile, ProjectMember, MilestoneType, Milestone, Ticket, TicketFile
from django.utils import timezone
import time
from django.utils.dateformat import DateFormat
from django.conf import settings
from authentication.models import Account
from .forms import ProjectForm, MilestoneForm, MilestoneEditForm,ProjectEditForm,TicketForm,TicketEditForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
import os
# Create your views here.

#project lists @rejoan
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


@login_required
#project create method @rejoan
def project_create(request, template_name='project/create.html'):
    proj_form = ProjectForm()
    leaders = Account.objects.filter(~Q(email= "hrd@spinytel.com"))
    members = Account.objects.filter(is_admin = False).order_by('id')

    if request.POST:# if submit form
        proj_form = ProjectForm(request.POST,request.FILES)
        if proj_form.is_valid(): #if form valid
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

#prject edit method @rejoan
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

            #update ProjectMember
            ProjectMember.objects.filter(project_id=p_id).filter(member_type=1).delete()
            for lead_member in request.POST.getlist('lead_user_ID'):
                project_lead = ProjectMember.objects.create(project_id=p_id,user_id=lead_member,member_type=1)

            #update projectfile
            ProjectMember.objects.filter(project_id=p_id).filter(member_type=2).delete()
            for normal_member in request.POST.getlist('normal_user_ID'):
                project_member = ProjectMember.objects.create(project_id=p_id,user_id=normal_member,member_type=2)

            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            for file in request.FILES.getlist('project_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                dest = open(os.path.join(settings.MEDIA_ROOT, str(p_id)+'_'+extn+'_'+file.name), 'wb')
                for chunk in file.chunks():
                    dest.write(chunk)
                    dest.close()
                file_name = file.name
                project_files = ProjectFile.objects.create(file_name=file_name,project_id=p_id)
                project_files.save()

            #redirect to project lists
            return HttpResponseRedirect("/project/")

    #send data row to edit
    data = {'name':project.name,'deadline':DateFormat(project.deadline).format('Y-m-d'),'project_update_id':project.id}
    proj_form = ProjectEditForm(data)
    proj_form.submit_val = 'Update Project'
    #import pdb; pdb.set_trace()
    return render_to_response(template_name, {'proj_form':proj_form, 'leaders': leaders, 'members':members, 'selected_lead': selected_lead,'selected_member':selected_member,'project_files':project_files}, context_instance = RequestContext(request))


#ticket manager @rejoan
def ticket_create(request, project_id, template_name='ticket/create.html'):
    tick_form = TicketForm(initial={'project_id': project_id})
    assign_to = [(a.user.get_id(), a.user.get_full_name()) for a in ProjectMember.objects.filter(project__id = project_id)]
    milestones = Milestone.objects.filter(project_id = project_id).values()
    project = get_object_or_404(Project,pk=project_id)

    if request.POST:# if submit form
        tick_form = TicketForm(request.POST, request.FILES)
        #import pdb;pdb.set_trace()
        if tick_form.is_valid(): #if form valid
            form_data = tick_form.cleaned_data
            create_date = timezone.now()
            project_id = form_data['project_id']
            status = form_data['status']
            priority = form_data['priority']
            assign = request.POST['t_assign']
            milestone = request.POST['t_milestone']
            estimate = form_data['estimate']
            title = form_data['title']
            description = form_data['description']
            creator_id = 1 # after authentication make session

            ticket_row = Ticket.objects.create(create_date=create_date,title=title,description=description,status=status,priority=priority,estimate=estimate,assign_person_id=assign,creator_id=creator_id,milestone_id=milestone,project_id=project_id)
            ticket_row.save()

            #Ticket file process start
            latest = Ticket.objects.latest('id')
            ticket_id = latest.pk
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            for file in request.FILES.getlist('ticket_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                dest = open(os.path.join(settings.MEDIA_ROOT, str(ticket_id)+'_'+extn+'_'+file.name), 'wb')
                for chunk in file.chunks():
                    dest.write(chunk)
                dest.close()

                file_name = file.name
                ticket_files = TicketFile.objects.create(file_name=file_name,ticket_id=ticket_id)
                ticket_files.save()

            return HttpResponse('/ticket/')
    tick_form.submit_val = 'Add Ticket'
    return render(request, template_name, {'tick_form': tick_form, 'assign_to': assign_to,'milestones':milestones,'project':project})


#ticket manager @rejoan
def ticket_edit(request, project_id, ticket_id, template_name='ticket/create.html'):
    if ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        tick_form = TicketEditForm(initial={'project_id': project_id,'ticket_id':ticket_id})

        assign_to = [(a.user.get_id(), a.user.get_full_name()) for a in ProjectMember.objects.filter(project__id = project_id)]
        milestones = Milestone.objects.filter(project_id = project_id).values()
        ticket_files = TicketFile.objects.filter(ticket_id=int(ticket_id)).values_list('id', 'file_name')
        project = get_object_or_404(Project,pk=project_id)

    if request.POST:# if submit form
        tick_form = TicketEditForm(request.POST, request.FILES)
        #import pdb;pdb.set_trace()
        if tick_form.is_valid(): #if form valid
            form_data = tick_form.cleaned_data
            t_id = form_data['ticket_id']
            create_date = timezone.now()
            project_id = form_data['project_id']
            status = form_data['status']
            priority = form_data['priority']
            assign = request.POST['t_assign']
            milestone = request.POST['t_milestone']
            estimate = form_data['estimate']
            title = form_data['title']
            description = form_data['description']
            creator_id = 1 # after authentication make session

            ticket_row = Ticket.objects.filter(pk=t_id).update(create_date=create_date,title=title,description=description,status=status,priority=priority,estimate=estimate,assign_person_id=assign,creator_id=creator_id,milestone_id=milestone,project_id=project_id)

            #Ticket file process start
            latest = Ticket.objects.latest('id')
            ticket_id = latest.pk
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            for file in request.FILES.getlist('ticket_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                dest = open(os.path.join(settings.MEDIA_ROOT, str(ticket_id)+'_'+extn+'_'+file.name), 'wb')
                for chunk in file.chunks():
                    dest.write(chunk)
                dest.close()

                file_name = file.name
                ticket_files = TicketFile.objects.create(file_name=file_name,ticket_id=ticket_id)
                ticket_files.save()

            return HttpResponse('/ticket/')
    data = {'project_id':project_id,'title':ticket.title,'description':ticket.description, 'ticket_id':ticket.id,'status':ticket.status,'priority':ticket.priority,'estimate':ticket.estimate}

    tick_form = TicketEditForm(data)
    tick_form.submit_val = 'Update Ticket'
    #import pdb;pdb.set_trace()
    return render(request, template_name, {'tick_form': tick_form, 'assign_to': assign_to,'milestones':milestones,'ticket_files':ticket_files,'milesId':ticket.milestone_id,'assignId':ticket.assign_person_id,'project':project})


def tickets(request,project_id):
    f_ticket = Ticket.objects.filter(project_id=project_id).values()
    if request.POST:
        posted = 'yes'
        t_id = request.POST['f_ticket_ID']
        f_priority = request.POST['f_priority']
        f_status = request.POST['f_status']

        if t_id.isdigit():
            f_ticket = Ticket.objects.filter(project_id=project_id).filter(id=int(t_id)).values()

        if f_priority.isdigit():
            f_ticket = Ticket.objects.filter(project_id=project_id).filter(priority=int(f_priority)).values()

        if f_status.isalnum():
            f_ticket = Ticket.objects.filter(project_id=project_id).filter(status=str(f_status)).values()
        #import pdb;pdb.set_trace()
    else:
        t_id = f_status = f_priority = posted = 'no'


    ticket = [[a['id'],a['title'],a['milestone_id'],a['assign_person_id'],a['status'],a['priority'],a['estimate']] for a in f_ticket]
    milestones = [Milestone.objects.values_list('title',flat=True).filter(id=int(b[2])) for b in ticket]
    assigned_to = [Account.objects.filter(id=int(b[3])).values_list('username', flat=True) for b in ticket]
    project = get_object_or_404(Project, pk=project_id)

    tickets = []
    for i in range(0,len(ticket)) :
        t = ticket[i]
        t[2] = milestones[i]
        t[3] = assigned_to[i]
        tickets.append(t)

    return render(request, 'ticket/lists.html',{'tickets':tickets,'project':project,'posted':posted,'t_id':t_id,'f_priority':f_priority,'f_status':f_status})


@login_required
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
            return redirect('/project/'+project_id+'/milestone/')

    return render(request, template_name, {'form': form, 'project_id': project_id})


@login_required
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
            return redirect('/project/'+project_id+'/milestone/')
        else:
            return HttpResponse(form)

    return render(request, template_name, {'form': form, 'project_id': project_id})


@login_required
def milestone_delete(request, project_id, milestone_id):
    data = get_object_or_404(Milestone, pk=milestone_id)
    data.delete()
    return redirect('/project/'+project_id+'/milestone/')


@login_required
def milestone_all(request, project_id, template_name='milestone/milestone_all.html'):
    milestone_details = Milestone.objects.filter(project_id=project_id)
    return render(request, template_name, {'milestone_details': milestone_details, 'project_id': project_id})
