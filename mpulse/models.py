# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Max
from django.db import models
from django.core.validators import RegexValidator



# Member Model
class Member(models.Model):
    first = models.CharField(max_length=255, blank=True)
    last = models.CharField(max_length=255,blank=True)
    telephone = models.CharField(max_length=10,null=True, unique=True)
    clientid = models.CharField(max_length=255,unique=True, null=True)
    accountid = models.CharField(max_length=255, null=True)

class Conflict(models.Model):
    first = models.CharField(max_length=255, blank=True)
    last = models.CharField(max_length=255,blank=True)
    telephone = models.CharField(max_length=10,null=True)
    clientid = models.CharField(max_length=255,null=True)
    accountid = models.CharField(max_length=255, null=True)




    


