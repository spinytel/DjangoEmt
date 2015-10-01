from project.models import Ticket
from authentication.models import Account
from django.template import Library
register = Library()


@register.simple_tag
def wall_ticket_number(status, project_id):
    a = Ticket.objects.filter(project_id=project_id, status=status)
    total = a.count()
    return total


@register.simple_tag
def wall_ticket_estimate(status, project_id):
    count_estimate = 0
    a = Ticket.objects.filter(project_id=project_id, status=status).values()
    for b in a:
        if b['estimate'] == 'None':
            count_estimate += 0
        elif b['estimate'] == 'Small':
            count_estimate += 1
        elif b['estimate'] == 'Medium':
            count_estimate += 2
        elif b['estimate'] == 'Large':
            count_estimate += 3

    return count_estimate


@register.assignment_tag
def wall_ticket_all(status, project_id):
    a = Ticket.objects.filter(project_id=project_id, status=status).values()
    return a


@register.simple_tag
def wall_ticket_priority(priority):
    if priority == 1:
        return "wall-priority-highest"
    elif priority == 2:
        return "wall-priority-high"
    elif priority == 3:
        return "wall-priority-normal"
    elif priority == 4:
        return "wall-priority-low"
    elif priority == 5:
        return "wall-priority-lowest"


@register.simple_tag
def wall_ticket_estimate_image(estimate):
    if estimate == 'None':
        return "estimate_none.png"
    elif estimate == 'Small':
        return "estimate_small.png"
    elif estimate == 'Medium':
        return "estimate_medium.png"
    elif estimate == 'Large':
        return "estimate_large.png"


@register.simple_tag
def wall_ticket_assign_to(user_id):
    a = Account.objects.filter(id=user_id).values('username')
    return a[0]['username']
