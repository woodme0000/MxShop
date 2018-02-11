from django.db import models


# Create your models here.
class Music(models.Model):
    song = models.TextField()
    singer = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "music"

    def __str__(self):
        return self.song


class Car(models.Model):
    name = models.CharField(u'车名', max_length=10)


class Driver(models.Model):
    name = models.CharField(u'人名',max_length=10)
    car = models.ForeignKey(Car, related_name='drivers', verbose_name='司机')