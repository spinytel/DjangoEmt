from project.models import Milestone, Ticket
from django.template import Library
register = Library()


@register.simple_tag
def get_close_tickets(milestone_id):
    close_t = Ticket.objects.filter(milestone_id=milestone_id, status__in=['Fixed'])
    total = close_t.count()
    return total


@register.simple_tag
def get_open_tickets(milestone_id):
    open_t = Ticket.objects.filter(milestone_id=milestone_id, status__in=['New', 'Accepted', 'Test'])
    total = open_t.count()
    return total


@register.simple_tag
def get_done_tickets(milestone_id):
    total_open = get_open_tickets(milestone_id)
    total_close = get_close_tickets(milestone_id)
    if total_close == 0:
        return 0
    else:
        return float("{0:.1f}".format((total_close/(total_open+float(total_close)))*100))
