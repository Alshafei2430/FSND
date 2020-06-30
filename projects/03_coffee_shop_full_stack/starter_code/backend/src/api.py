import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

def convert_dict_drink_to_array(dict_drink):
    drink_long = []
    drink_long.append(dict_drink)
    return drink_long
    
## ROUTES
@app.route("/")
def greetings():
    return "hello from api server"
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
def drinks():
    drinks = [drink.short() for drink in  Drink.query.all()]
    return jsonify({
        "success": True,
        'drinks': drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def drink_details(jwt):
    drinks = [drink.long() for drink in Drink.query.order_by(Drink.id).all()]
    return jsonify({
        "success": True,
        "drinks": drinks
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    response = request.get_json()
    drink = Drink(title = response['title'], recipe = json.dumps(response['recipe']))
    drink.insert()
    drink_id = drink.id
    return jsonify({
        "success": True,
        "drinks": convert_dict_drink_to_array(Drink.query.get(drink_id).long())
    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, drink_id):
    response = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is not None:
        try :
            if 'id' in response:
                drink.id = response["id"]
            if 'title' in response:
                drink.title = response['title']
            if 'recipe' in response:
                print(f'test update endpoint {response}')
                drink.recipe = json.dumps(response['recipe'])
            drink.update()
            drink_id = drink.id
            return jsonify({
                "success": True,
                "drinks": convert_dict_drink_to_array(Drink.query.get(drink_id).long())
            }), 200

        except:
            abort(400)
    else:
        abort(404) 
    # print(jwt)
    return jsonify({
        "success": False,
        "status code": 404,
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    print("ooooooooooooooo", drink)
    if drink is not None:
        try :
            drink.delete()
            return jsonify({
                "success": True,
                "delete": drink_id
            }), 200

        except:
            abort(400)
    else:
        abort(404) 
    # print(jwt)
    return jsonify({
        "success": False,
        "status code": 404,
    })

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found',
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def not_found(error):
    return jsonify({
      'success': False,
      'error': AuthError,
      'message': 'authentication error',
    }), AuthError
