USERS = ['devel@antoneliasson.se',
         'anton.e.92@gmail.com']
GROUPS = {'devel@antoneliasson.se':['editors']}

def groupfinder(userid, request):
    return GROUPS.get(userid, [])
