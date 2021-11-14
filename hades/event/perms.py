from .models import Event,Permission

def has_permission(name,event_id,user):
    try:
        role_inst_m = Event.objects.get(id=event_id).organisation.members.get(user=user).role.all()
        Permission.objects.get(perm=name,role__in=role_inst_m)
    except:
        return False
    return True

def list_permissions(event_id,user):
    try:
        role_inst_m = Event.objects.get(id=event_id).organisation.members.get(user=user).role.all()
    except:
        return []
    role_perm_m = Permission.objects.filter(role__in=role_inst_m).values_list('perm',flat=True)
    return role_perm_m

