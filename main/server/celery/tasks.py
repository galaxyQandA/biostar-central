from celery import task
from main.server import models
from django.core.mail import EmailMessage

@task(name='remi_task')
def send_mail_bookmarked(post):
    # First: Get the root id of the post
    post_root_id = post.root_id

    # Then: Get all the post_ids where root_id is the root
    posts_root_related = models.Post.objects.filter(root_id=post_root_id)

    # Then: Look in server_vote, if post_id==one of the post_ids and type==4, then, verify if it author_id does not already exist and  add the author_id to the list
    authors_id_related = models.Vote.objects.filter(post_id__in=posts_root_related, type=4).exclude(author_id=post.author).values_list('author_id', flat=True).distinct()

    # Then: Get all the email address from auth_user where author_id match, and put the email field in mail_list
    emails = models.User.objects.filter(id__in=authors_id_related).values_list('email', flat=True)

    # send_mail('GalaxyQ&A: %s' % post.get_title(),"A new post has been added, Here is the content:\n\n%s" % post.content, 'remi.marenco@gmail.com', emails, fail_silently=False)

    email = EmailMessage('GalaxyQ&A: %s' % post.get_title(), 'A new post has been added, Here is the content:\n\n%s' % post.content, 'remi.marenco@gmail.com',[], emails,)

    email.send(fail_silently=False)
