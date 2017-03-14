from django.db import models
from PIL import Image
#not used finally

'''class Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

     #model_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
'''

class Choice(models.Model):
    choice_text = models.CharField(max_length = 2000) 
    '''flights = models.CharField(max_length = 200)
    bus_dep = models.CharField(max_length = 200)
    bus_arr = models.CharField(max_length = 200)
    cab = models.CharField(max_length = 200)
    uber = models.CharField(max_length = 200)'''
    