from src.app import ma

class roleSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description")
