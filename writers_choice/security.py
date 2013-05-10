def groupfinder(userid, request):
    admin_email = request.registry.settings['admin_email']
    return ['group:editors'] if userid == admin_email else []
