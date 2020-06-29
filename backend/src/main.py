import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth, get_token_auth_header

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():

    # Get all the drinks from db
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [d.short() for d in drinks]
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):

    # Get all the drinks from db
    drinks = Drink.query.all()

    # Transform Drinks to long drinks

    return jsonify({
        'success': True,
        'drinks': [d.long() for d in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    # Get the body
    req = request.get_json()
    try:
        # create new Drink
        drink = Drink()
        drink.title = req['title']
        # convert recipe to String
        drink.recipe = json.dumps(req['recipe'])
        # insert the new Drink
        drink.insert()

    except Exception:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]})


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    # Get the body
    req = request.get_json()

    # Get the Drink with requested Id
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    # if no drink with given id abort
    if not drink:
        abort(404)

    try:

        req_title = req.get('title')
        req_recipe = req.get('recipe')

        # check if the title is the one is updated
        if req_title:
            drink.title = req_title

        # check if the recipe is the one is updated
        if req_recipe:
            drink.recipe = json.dumps(req['recipe'])

        # update the drink
        drink.update()
    except Exception:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]}), 200


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    # Get the Drink with requested Id
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    # if no drink with given id abort
    if not drink:
        abort(404)

    try:
        # delete the drink
        drink.delete()
    except Exception:
        abort(400)

    return jsonify({'success': True, 'delete': id}), 200


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405


if __name__ == "__main__":
    app.debug = True
    app.run()
