from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return u'%s: %s' % (self.user.username, self.name)

class Story(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    headline = models.CharField(max_length=64)
    Categories = [('pol','Politics'),('art','Art'),('tech','Technology New'),('trivia','Trivial News')]
    category = models.CharField(max_length=32, choices=Categories)
    Regions = [('uk','UK News'),('eu','European News'),('w','World News')]
    region = models.CharField(max_length=32, choices=Regions)
    details = models.CharField(max_length=512)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return u'%s by %s' % (self.headline, self.author.name)
