from django.db import models

# Create your models here.
class movie_info(models.Model):
    '''説明文'''
    movie_title = models.CharField(max_length=200)
    movie_id = models.IntegerField(default=0)
    movie_update = models.DateTimeField('movie updatetime', null=True)
    def __str__(self):
        return self.movie_title


class movie_comments(models.Model):
    '''説明文'''
    movie_info = models.ForeignKey(movie_info, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=99999)
    agree_vote = models.IntegerField(default=0)
    disagree_vote = models.IntegerField(default=0)
    def __str__(self):
        return self.comment_text
    
