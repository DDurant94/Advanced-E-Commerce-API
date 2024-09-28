from marshmallow import fields,validate
from schema import ma

class CustomerAccountSchema(ma.Schema):
  id = fields.Integer(required=False)
  username = fields.String(required=True,validate=validate.Length(min=1))
  password = fields.String(required=True,validate=validate.Length(min=1))
  role = fields.String(required=False,validate=validate.Length(min=2))
  customer = fields.Nested('CustomerSchema')
  
class CustomerAddAccountSchema(ma.Schema):
  id = fields.Integer(required=False)
  username = fields.String(required=True,validate=validate.Length(min=1))
  password = fields.String(required=True,validate=validate.Length(min=1))
  customer_id = fields.Integer(required = True)
  role = fields.String(required=False,validate=validate.Length(min=2))
  
add_customer_account_schema = CustomerAddAccountSchema()
    
customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)