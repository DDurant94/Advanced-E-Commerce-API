from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from database import db
from schema import ma
from limiter import limiter
from caching import cache
from sqlalchemy.orm import Session

from models.customer import Customer
from models.customerAccount import CustomerAccount
from models.order import Order
from models.product import Product
from models.orderProduct import OrderProducts
from models.role import Role
from models.customerManagementRole import CustomerManagementRole

from routes.customerBP import customer_blueprint
from routes.customerAccountBP import customer_account_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.roleBP import role_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={
    'app_name': "E-Commerce API"
  }
)

def create_app(config_name):
  app = Flask(__name__)
  
  app.config.from_object(f'config.{config_name}')
  db.init_app(app)
  ma.init_app(app)
  cache.init_app(app)
  limiter.init_app(app)
  CORS(app)
  
  
  return app

def blue_print_config(app):
  app.register_blueprint(customer_blueprint, url_prefix='/customers')
  app.register_blueprint(customer_account_blueprint,url_prefix='/customer-accounts')
  app.register_blueprint(order_blueprint,url_prefix='/orders')
  app.register_blueprint(product_blueprint,url_prefix='/products')
  app.register_blueprint(role_blueprint,url_prefix='/roles')
  app.register_blueprint(swagger_blueprint,url_prefix=SWAGGER_URL)
  

def configure_rate_limit():
  limiter.limit("100 per day")(customer_blueprint)
  limiter.limit("100 per day")(customer_account_blueprint)
  limiter.limit("100 per day")(order_blueprint)
  limiter.limit("100 per day")(product_blueprint)
  limiter.limit("100 per day")(role_blueprint)
  limiter.limit("100 per day")(swagger_blueprint)

def init_roles_data():
  with Session(db.engine) as session:
    with session.begin():
      roles = [
        Role(role_name = 'admin'),
        Role(role_name = 'user'),
        Role(role_name = 'guest')
      ]
      session.add_all(roles)

if __name__ == '__main__':
  app = create_app('DevelopmentConfig')
  
  blue_print_config(app)
  configure_rate_limit()
  
  with app.app_context():
    db.create_all()
    
  app.run(debug=True)