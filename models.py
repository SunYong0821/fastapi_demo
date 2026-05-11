from tortoise.models import Model
from tortoise import fields
from datetime import datetime

def model_to_dict(s, exclude=None):
    res = {}
    for i in s._meta.fields_map.keys():
        if exclude and i in exclude:
            continue
        val = getattr(s, i)
        if isinstance(val, datetime):
            val = val.strftime('%Y-%m-%d %H:%M:%S')
        res[i] = val
    return res

def model_update(model, **kwargs):
    for k, v in kwargs.items():
        setattr(model, k, v)
    return model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, index=True)
    password = fields.CharField(max_length=300)
    version = fields.IntField(default=0)
    addtime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def to_dict(self):
        return model_to_dict(self, exclude=['password'])
    
    def update(self, **kwargs):
        return model_update(self, **kwargs)
