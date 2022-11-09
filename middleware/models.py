# type: ignore
from django.db.models import *

class Request(Model):
    id = AutoField(primary_key=True)

    url = CharField(max_length=255)
    method = CharField(max_length=255)
    data = JSONField(null=True)

    statusCode = IntegerField()
    response = JSONField()

class Comparision(Model):
    id = AutoField(primary_key=True)
    
    primaryRequest = ForeignKey(Request, on_delete=PROTECT, related_name='primary')
    secondaryRequest = ForeignKey(Request, on_delete=PROTECT, related_name='secondary')

    statusCodeEqual = BooleanField()
    responseEqual = BooleanField()
    equals = BooleanField()