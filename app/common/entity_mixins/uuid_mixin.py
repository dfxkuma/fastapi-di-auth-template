from tortoise import fields


class UUIDEntityMixin:
    id = fields.UUIDField(pk=True)
