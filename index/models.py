from django.db import models

# Create your models here.


def md5(string):
    import hashlib
    obj = hashlib.md5()
    obj.update(string.encode("utf-8"))
    return obj.hexdigest()