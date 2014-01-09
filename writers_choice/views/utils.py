from markdown.extensions import headerid

def format_article_metadata(article):
    id = article.id
    title = article.title
    published = article.date_published.strftime('%Y-%m-%d')

    return {'id' : id, 'title' : title, 'published' : published}
