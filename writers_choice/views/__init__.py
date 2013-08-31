import markdown.extensions.headerid

def format_article_metadata(article):
    id = article.id
    title = article.title
    published = article.date_published.strftime('%Y-%m-%d')

    return {'id' : id, 'title' : title, 'published' : published}

def slugify(url):
    return markdown.extensions.headerid.slugify(url, '-')

conn_err_msg = """\
(Tabellen finns inte)

Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_Writers_Choice_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
