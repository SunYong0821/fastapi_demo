from tortoise.models import Model
from tortoise import fields
from datetime import datetime

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, index=True)
    password = fields.CharField(max_length=300)
    version = fields.IntField(default=0)
    addtime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def to_dict(self):
        json = {}
        for i in self._meta.fields_map.keys():
            val = getattr(self, i)
            if isinstance(val, datetime):
                val = val.strftime('%Y-%m-%d %H:%M:%S')
            json[i] = val
        return json
    
    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
