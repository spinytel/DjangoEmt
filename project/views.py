from django.shortcuts import render_to_response, redirect, get_object_or_404,render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from .models import Project, ProjectFile, ProjectMember, MilestoneType, Milestone, Ticket, TicketFile, Comment
from django.utils import timezone
import time
from django.utils.dateformat import DateFormat
from django.conf import settings
from authentication.models import Account
from .forms import ProjectForm, MilestoneForm, MilestoneEditForm,ProjectEditForm,TicketForm,TicketEditForm
from django.db.models import Q,F,Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.views import get_logged_in_user_id
import os


@login_required
# project lists @rejoan
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
# Author : @mamun0024
def project_user_type(request, project_id):
    current_user_id = get_logged_in_user_id(request)
    current_user_type = ProjectMember.objects.filter(project_id=project_id,user_id=current_user_id).values('member_type')
    if current_user_type:
        return current_user_type[0]
    else:
        return {'member_type': 0}


@login_required
# project home show project specific streams
# project lists @rejoan & @mamun0024
def project_home(request, project_id):
    current_user_type_l = project_user_type(request, project_id)

    if current_user_type_l['member_type'] != 0:
        project = get_object_or_404(Project, pk=project_id)
        #import pdb;pdb.set_trace()
        leaders = ProjectMember.objects.filter(project_id=project_id,member_type=1).select_related('user').annotate(username=F('user__username'))
        members = ProjectMember.objects.filter(project_id=project_id,member_type=2).select_related('user').annotate(username=F('user__username'))

        latest_three = Comment.objects.extra(select={'create_date':"to_char(create_date,'DD-MM-YYYY')"}).values('create_date').annotate(dcount=Count('create_date')).order_by('-create_date')
        comments = Comment.objects.filter(ticket__project_id=project_id).select_related('creator','ticket').annotate(username=F('creator__username'),t_title=F('ticket__title')).values()
        return render(request, 'project/home.html', {'project': project, 'project_id': project_id, 'comments': comments, 'leaders': leaders, 'members': members, 'latest_three': latest_three, 'current_user_type': current_user_type_l})
    else:
        return HttpResponse("Access Denied")



@login_required
# Author : @mamun0024
def project_wall(request,project_id):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'project/wall.html', {'project': project, 'project_id': project_id})
    else:
        return HttpResponse("Access Denied")


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
            dest = False
            for f in request.FILES.getlist('project_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                file_name = str(proj_id)+'_'+extn+'_'+f.name
                dest = open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb')
                for chunk in f.chunks():
                    dest.write(chunk)

                project_files = ProjectFile.objects.create(file_name=file_name,project_id=proj_id)
                project_files.save()
            if dest:
                dest.close()

            #project and lead members process
            for lead_member in request.POST.getlist('lead_user_ID'):
                project_lead = ProjectMember.objects.create(project_id=proj_id,user_id=lead_member,member_type=1)

            for normal_member in request.POST.getlist('normal_user_ID'):
                project_member = ProjectMember.objects.create(project_id=proj_id,user_id=normal_member,member_type=2)

            messages.info(request, 'Project Created Successfully')
            return HttpResponseRedirect('/project/')
    proj_form.submit_val = 'Add Project'
    return render(request, template_name, {'proj_form': proj_form, 'leaders': leaders, 'members':members})

#prject edit method @rejoan
@login_required
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
            dest = False
            for f in request.FILES.getlist('project_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                file_name = str(p_id)+'_'+extn+'_'+f.name
                dest = open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb')
                for chunk in f.chunks():
                    dest.write(chunk)
                project_files = ProjectFile.objects.create(file_name=file_name,project_id=p_id)
                project_files.save()
            if dest:
                dest.close()

            messages.info(request, 'Project Updated Successfully')
            return HttpResponseRedirect("/project/")

    #send data row to edit
    data = {'name':project.name,'deadline':DateFormat(project.deadline).format('Y-m-d'),'project_update_id':project.id}
    proj_form = ProjectEditForm(data)
    proj_form.submit_val = 'Update Project'
    #import pdb; pdb.set_trace()
    return render_to_response(template_name, {'proj_form':proj_form, 'leaders': leaders, 'members':members, 'selected_lead': selected_lead,'selected_member':selected_member,'project_files':project_files}, context_instance = RequestContext(request))


#ticket manager @rejoan
@login_required
def ticket_create(request, project_id, template_name='ticket/create.html'):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        tick_form = TicketForm(initial={'project_id': project_id})
        assign_to = [(a.user.get_id(), a.user.get_full_name()) for a in ProjectMember.objects.filter(project__id = project_id)]
        milestones = Milestone.objects.filter(project_id = project_id).values()
        project = get_object_or_404(Project,pk=project_id)

        if request.POST:# if submit form
            tick_form = TicketForm(request.POST, request.FILES)
            #import pdb;pdb.set_trace()
            if tick_form.is_valid(): #if form valid
                form_data = tick_form.cleaned_data
                milstn = request.POST['t_milestone']
                if not milstn.isdigit():
                    messages.error(request, 'Select a milestone. If none add first')
                    #import pdb;pdb.set_trace()
                    return HttpResponseRedirect('/project/'+project_id+'/ticket/create')
                create_date = timezone.now()
                project_id = form_data['project_id']
                status = form_data['status']
                priority = form_data['priority']
                assign = request.POST['t_assign']
                milestone = milstn
                estimate = form_data['estimate']
                title = form_data['title']
                description = form_data['description']
                creator_id = request.user.id

                ticket_row = Ticket.objects.create(create_date=create_date,title=title,description=description,status=status,priority=priority,estimate=estimate,assign_person_id=assign,creator_id=creator_id,milestone_id=milestone,project_id=project_id)
                ticket_row.save()

                #Ticket file process start
                latest = Ticket.objects.latest('id')
                ticket_id = latest.pk
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)
                dest = False
                for f in request.FILES.getlist('ticket_file'):
                    dt = timezone.now()
                    extn = str(int(time.mktime(dt.timetuple())))
                    file_name = str(ticket_id)+'_'+extn+'_'+f.name
                    dest = open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb')
                    for chunk in f.chunks():
                        dest.write(chunk)

                    ticket_files = TicketFile.objects.create(file_name=file_name,ticket_id=ticket_id)
                    ticket_files.save()
                if dest:
                    dest.close()
                messages.info(request, 'Ticket Created Successfully')
                return HttpResponseRedirect('/project/'+project_id+'/tickets/')
        tick_form.submit_val = 'Add Ticket'
        return render(request, template_name, {'tick_form': tick_form, 'assign_to': assign_to,'milestones':milestones,'project':project,'project_id':project_id})
    else:
        return HttpResponse("Access Denied")


#ticket edit @rejoan
@login_required
def ticket_edit(request, project_id, ticket_id, template_name='ticket/create.html'):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
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
                milstn = request.POST['t_milestone']
                if not milstn.isdigit():
                    messages.error(request, 'Select a milestone. If none add first')
                    #import pdb;pdb.set_trace()
                    return HttpResponseRedirect('/project/'+project_id+'/ticket/'+ticket_id+'/edit')
                t_id = form_data['ticket_id']
                create_date = timezone.now()
                project_id = form_data['project_id']
                status = form_data['status']
                priority = form_data['priority']
                assign = request.POST['t_assign']
                milestone = milstn
                estimate = form_data['estimate']
                title = form_data['title']
                description = form_data['description']
                creator_id = request.user.id

                ticket_row = Ticket.objects.filter(pk=t_id).update(create_date=create_date,title=title,description=description,status=status,priority=priority,estimate=estimate,assign_person_id=assign,creator_id=creator_id,milestone_id=milestone,project_id=project_id)

                #Ticket file process start
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)
                dest = False
                for f in request.FILES.getlist('ticket_file'):
                    dt = timezone.now()
                    extn = str(int(time.mktime(dt.timetuple())))
                    file_name = str(ticket_id)+'_'+extn+'_'+f.name
                    dest = open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb')
                    #import pdb;pdb.set_trace()
                    for chunk in f.chunks():
                        dest.write(chunk)
                    ticket_files = TicketFile.objects.create(file_name=file_name,ticket_id=ticket_id)
                    ticket_files.save()
                if dest:
                    dest.close()

                messages.info(request, 'Ticket Updated Successfully')
                return HttpResponseRedirect('/project/'+project_id+'/tickets/')
        data = {'project_id':project_id,'title':ticket.title,'description':ticket.description, 'ticket_id':ticket.id,'status':ticket.status,'priority':ticket.priority,'estimate':ticket.estimate,'project_id':project_id}

        tick_form = TicketEditForm(data)
        tick_form.submit_val = 'Update Ticket'
        #import pdb;pdb.set_trace()
        return render(request, template_name, {'tick_form': tick_form, 'assign_to': assign_to,'milestones':milestones,'ticket_files':ticket_files,'milesId':ticket.milestone_id,'assignId':ticket.assign_person_id,'project':project,'project_id':project_id})
    else:
        return HttpResponse("Access Denied")

#all tickets of particual project and tiicket search
@login_required
def tickets(request,project_id):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        f_ticket = Ticket.objects.filter(project_id=project_id).values()
        if request.POST:
            posted = 'yes'
            t_id = request.POST['f_ticket_ID']
            f_priority = request.POST['f_priority']
            f_status = request.POST['f_status']
            f_args = {}
            if t_id.isdigit():
                f_args['id'] = int(t_id)

            if f_priority.isdigit():
                f_args['priority'] = int(f_priority)

            if f_status.isalnum():
                f_args['status'] = f_status

            f_ticket = Ticket.objects.filter(project_id=project_id).filter(**f_args).values()
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

        return render(request, 'ticket/lists.html',{'tickets':tickets,'project':project,'project_id':project_id,'posted':posted,'t_id':t_id,'f_priority':f_priority,'f_status':f_status})
    else:
        return HttpResponse("Access Denied")

# ticket details and commenting on ticket
@login_required
def ticket_details(request,project_id,ticket_id):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        tickets = Ticket.objects.filter(project_id=project_id,id=ticket_id).select_related('milestone','assign_person','project','creator').annotate(username=F('assign_person__username'),m_title=F('milestone__title'),p_create_date=F('project__create_date'),p_deadline=F('project__deadline'),project_id=F('project__id'),ticket_creator=F('creator__username')).values()
        ticket_files = TicketFile.objects.filter(ticket_id=ticket_id).values()
        comments = Comment.objects.filter(ticket_id=ticket_id).order_by('id').select_related('creator').annotate(username=F('creator__username')).values()

        comment = {}
        if request.POST:
            if request.POST['comment_desc'] == '':
                messages.info(request, 'Comment can\'t empty')
                return HttpResponseRedirect('/project/'+project_id+'/ticket/'+ticket_id+'/details')

            if request.POST['t_status'].isalpha():
                curr_status = request.POST['t_status']
            else:
                curr_status = tickets[0]["status"]

            comment['create_date'] = timezone.now()
            comment['creator_id'] = request.user.id
            comment['ticket_id'] = ticket_id
            comment['details'] = request.POST['comment_desc']

            if tickets[0]["status"] != curr_status:
                comment['prev_status'] = tickets[0]["status"]
                comment['curr_status'] = curr_status

                Ticket.objects.filter(pk=ticket_id).update(status=curr_status)

            Comment.objects.create(**comment)

            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            dest = False
            for f in request.FILES.getlist('ticket_file'):
                dt = timezone.now()
                extn = str(int(time.mktime(dt.timetuple())))
                file_name = str(ticket_id)+'_'+extn+'_'+f.name
                dest = open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb')
                for chunk in f.chunks():
                    dest.write(chunk)

                ticket_files = TicketFile.objects.create(file_name=file_name,ticket_id=ticket_id)
                ticket_files.save()

            if dest:
                dest.close()
            return HttpResponseRedirect('/project/'+project_id+'/ticket/'+ticket_id+'/details')
        return render(request, 'ticket/details.html', {'tickets':tickets,'ticket_files':ticket_files,'project_id':project_id,'comments':comments})
    else:
        return HttpResponse("Access Denied")

#delete files from edit page (project, ticket)
@login_required
def delete_files(request):
    if request.is_ajax():
        file_id = int(request.POST['ID'])
        file_name = request.POST['f_name']
        is_project = request.POST['project']
        #import pdb; pdb.set_trace()
        if(is_project == 'yes'):
            ProjectFile.objects.filter(pk=file_id).delete()
        else:
            TicketFile.objects.filter(pk=file_id).delete()

        folder = settings.MEDIA_ROOT
        os.remove(os.path.join(folder, file_name))
        return HttpResponse('1')

#delete ticket with associated files
@login_required
def ticket_delete(request, project_id, ticket_id):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        ticket.delete()
        TicketFile.objects.filter(ticket_id=ticket_id).delete()
        messages.info(request, 'Ticket Deleted Successfully')
        return HttpResponseRedirect('/project/'+project_id+'/tickets/')
    else:
        return HttpResponse("Access Denied")

# project files on menu (dashboard)
@login_required
def project_files(request,project_id):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        all_files = ProjectFile.objects.filter(project_id=project_id).values()
        project = get_object_or_404(Project,pk=project_id)
        return render(request, 'project/files.html', {'project':project,'all_files':all_files,'project_id':project_id})
    else:
        return HttpResponse("Access Denied")


@login_required
# Author : @mamun0024
def milestone_create(request, project_id, template_name='milestone/milestone_create.html'):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] == 1:
        form = MilestoneForm(passing_id=project_id)
        project = get_object_or_404(Project, pk=project_id)

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

        return render(request, template_name, {'form': form, 'project_id': project_id, 'project': project})
    else:
        return HttpResponse("Access Denied")


@login_required
# Author : @mamun0024
def milestone_edit(request, project_id, milestone_id, template_name='milestone/milestone_edit.html'):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] == 1:
        form = MilestoneEditForm(passing_milestone_id=milestone_id)
        project = get_object_or_404(Project, pk=project_id)

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

        return render(request, template_name, {'form': form, 'project_id': project_id, 'project': project})
    else:
        return HttpResponse("Access Denied")


@login_required
# Author : @mamun0024
def milestone_delete(request, project_id, milestone_id):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] == 1:
        data = get_object_or_404(Milestone, pk=milestone_id)
        data.delete()
        return redirect('/project/'+project_id+'/milestone/')
    else:
        return HttpResponse("Access Denied")


@login_required
# Author : @mamun0024
def milestone_all(request, project_id, template_name='milestone/milestone_all.html'):
    current_user_type_l = project_user_type(request, project_id)
    if current_user_type_l['member_type'] != 0:
        milestone_details = Milestone.objects.filter(project_id=project_id)
        project = get_object_or_404(Project, pk=project_id)
        return render(request, template_name, {'milestone_details': milestone_details, 'project_id': project_id, 'project': project, 'current_user_type': current_user_type_l})
    else:
        return HttpResponse("Access Denied")
