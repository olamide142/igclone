from django.db import models

import uuid

# Create your models here.

class Account(models.Model):

    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15, unique=True, null=False)
    profile_name = models.CharField(max_length=30, null=True)
    bio = models.TextField(max_length=500, null=True)
    is_private = models.BooleanField(default=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):

    type_of_post_choice = [('CM','Comment'), ('IM','Image')]

    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15, unique=True, null=False)
    type_of_post = models.CharField(max_length=2, choices=type_of_post_choice, null=False)
    post_id = models.UUIDField(null=False)
    content = models.CharField(max_length=300, default=True)
    created_on =  models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Follows(models.Model):

    follows_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username1 = models.CharField(max_length=15, unique=True, null=False)
    username2 = models.CharField(max_length=15, unique=True, null=False)
    is_following = models.CharField(max_length=3, default="0-0")
    is_blocked = models.CharField(max_length=3, default="0-0")
    is_muted = models.CharField(max_length=3, default="0-0")
    created_on =  models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Image(models.Model):

    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15, unique=True, null=False)
    url = models.CharField(max_length=300, null=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Likes(models.Model):

    type_of_post_choice = [('CM','Comment'), ('IM','Image')]

    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15, unique=True, null=False)
    type_of_post = models.CharField(max_length=2, choices=type_of_post_choice, null=False)
    post_id = models.UUIDField(null=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
