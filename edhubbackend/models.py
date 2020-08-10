from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    lastlogin = models.DateTimeField(auto_now_add=True);
    displaypicture = models.CharField();
    subnumber = models.CharField(max_length=1000);

class Tag(models.Model):
    text=models.CharField(max_length=100);
    color=models.CharField(max_length=100);


class Classroom(models.Model):
    name=models.CharField(max_length=1000);
    teachers = models.ManyToManyField(User , related_name='classrooms_created');
    students = models.ManyToManyField(User , related_name='classrooms_joined');
    join_requests = models.ManyToManyField(User , related_name='classroom_join_requests');
    display_picture=models.ImageField();
    isprivate=models.BooleanField();
    tag=models.ManyToManyField(Tag , related_name='classrooms');
    class Meta:
        ordering=['name'];
    def __str__(self):
        return '%s' %(self.name)

class Thread(models.Model):
    title=models.CharField(max_length=1000)
    classroom=models.ManyToManyField(Classroom , related_name='threads')
    members=models.ManyToManyField(User , related_name='threads')
    display_picture=models.ImageField()

class Assignment(models.Model):
    owner=models.ManyToManyField(User , related_name='assignments')
    title=models.TextField(max_length=1000)
    text=models.TextField(max_length=2000)
    timestamp=models.DateTimeField(auto_add_now=True)
    expires_at=models.DateTimeField()
    max_marks=models.IntegerField()
    classroom=models.ForeignKey(Classroom , related_name='assignment')

class Post(models.Model):
    owner=models.ForeignKey(User , related_name='posts')
    content = models.TextField(max_length=2000)
    timestamp=models.DateTimeField(auto_add_now=True)
    comments_allowed=models.BooleanField()
    thread=models.ForeignKey(Thread , related_name='post')



class Submission(models.Model):
    owner=models.ForeignKey(User , related_name='submissions')
    timestamp=models.DateTimeField(auto_add_now=True)
    assignment = models.ForeignKey(Assignment)
    marks_obtained=models.IntegerField()


class Comment(models.Model):
    owner=models.ForeignKey(User , related_name='comments')
    content = models.TextField(max_length=1000)
    post = models.ForeignKey(Post , on_delete=models.CASCADE,related_name='comments');
    timestamp=models.DateTimeField(auto_add_now=True)


class File(models.Model):
    filetype=models.CharField()
    content_type=models.ForeignKey(ContentType , on_delete=models.CASCADE , related_name='files')
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type'  , 'object_id')
    timestamp=models.DateTimeField(auto_add_now=True)




