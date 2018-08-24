import json


def get_post_attrs(post):
    return {
        "id": post.id,
        "author": post.author,
        "title": post.title,
        "slug": post.slug,
        "body": post.body,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "published_date": post.published_date,
    }

def serialize_data(body):
    return json.loads(str(body, 'utf-8'))

