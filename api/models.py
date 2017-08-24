from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User

LanguageChoices = (
    ('Scientific Python', 'Scientific Python'),  # Include numpy, pandas, ect..
    ('Python', 'Python'),
    ('Javascript', 'Javascript'),
    ('C', 'C'),
    ('Java', 'Java'),
    ('C++', 'C++'),
    ('Go', 'Go'),
    ('Ruby', 'Ruby')
)


class Task(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey('auth.User', related_name='posted_tasks', on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    solutions = JSONField()
    tags = ArrayField(models.CharField(max_length=40), null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


class Answer(models.Model):
    author = models.ForeignKey('auth.User', related_name='posted_answers', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='answers', on_delete=models.CASCADE)
    language = models.CharField(max_length=20, choices=LanguageChoices)
    is_right = models.BooleanField(default=False)
    code = models.FileField()

    def __str__(self):
        return '%s`s %s solution' % (self.author.username, self.task.name)


