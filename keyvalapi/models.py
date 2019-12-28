from django.db import models


class KeyValStore(models.Model):
	key = models.CharField(max_length=255)
	value = models.TextField()
	ttl = models.DateTimeField(auto_now=True) 