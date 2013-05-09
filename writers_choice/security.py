USERS = ['devel@antoneliasson.se',
         'anton.e.92@gmail.com']
GROUPS = {'devel@antoneliasson.se':['editors']}

def groupfinder(userid, request):
    admin_email = request.registry.settings['admin_email']
    return ['editors'] if userid == admin_email else []
#    return GROUPS.get(userid, [])
