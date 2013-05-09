USERS = ['devel@antoneliasson.se',
         'anton.e.92@gmail.com']
GROUPS = {'devel@antoneliasson.se':['group:editors']}

def groupfinder(userid, request):
    admin_email = request.registry.settings['admin_email']
    return ['group:editors'] if userid == admin_email else []
#    return GROUPS.get(userid, [])
