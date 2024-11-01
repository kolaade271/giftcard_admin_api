from marshmallow import Schema, fields, ValidationError


class AdminLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
class AdminRateSchema(Schema):
    _id = fields.Str(required=True)
    rate = fields.Str(required=True,)
    
class AdminSelltrxSchema(Schema):
    _id = fields.Str(required=True)
    status = fields.Str(required=True,)

admin_login_schema = AdminLoginSchema()
admin_rate_schema = AdminRateSchema()
admin_sell_trx_schema = AdminSelltrxSchema()
