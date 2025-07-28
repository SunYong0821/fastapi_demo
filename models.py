from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, index=True)
    password = fields.CharField(max_length=300)
    addtime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def to_dict(self):
        json = {}
        for i in self._meta.fields_map.keys():
            json[i] = getattr(self, i)
        return json

    @classmethod
    async def list_to_dict(cls, objects):
        return [obj.to_dict() for obj in objects]

