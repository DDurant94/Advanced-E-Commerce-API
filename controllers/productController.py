from flask import request, jsonify
from models.schemas.productSchema import product_schema,products_schema
from services import productService
from marshmallow import ValidationError
from caching import cache

from utils.util import token_required,role_required

@token_required
@role_required('admin')
def save():
  try:
    product_data = product_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    product_save = productService.save(product_data)
    return product_schema.jsonify(product_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
@cache.cached(timeout=60)
@token_required
def find_all():
  page = request.args.get('page',1,type=int)
  per_page=request.args.get('per_page',10,type=int)
  return products_schema.jsonify(productService.find_all(page=page,per_page=per_page)), 200

@cache.cached(timeout=60)
@token_required
def find_by_id(id):
  product = productService.find_by_id(id)
  return product_schema.jsonify(product),200

@token_required
@role_required('admin')
def update(id):
  try:
    product_data = product_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    updated_product = productService.update(product_data,id)
    return product_schema.jsonify(updated_product),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400

@token_required
@role_required('admin')  
def delete(id):
  product = productService.delete(id)
  if product == "successful":
    return jsonify({"message": "Product removed successfully"}), 200
  else:
    return jsonify({"message": f"Couldn't find product with ID {id}"}), 404 