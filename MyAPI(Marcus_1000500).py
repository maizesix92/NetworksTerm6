from flask import Flask, url_for
from flask import json
from flask import Response
from flask import request
from functools import wraps
import re
"""
Networks Lab 3
Name: Tan Yi Xiang Marcus
ID: 1000500
"""
import logging
app = Flask(__name__)
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

user_pass = {
	"admin":"Password123",
	"admin2":"Password1",
	"admin3":"Password"
}

stalls = [
		{
			"id" : 1,
			"name" : "Drinks",
			"itemsonsale": 5
		},{
			"id" : 2,
			"name" : "Western",
			"itemsonsale": 12
		},{
			"id" : 3,
			"name" : "Chinese",
			"itemsonsale": 8
		},{
			"id" : 4,
			"name" : "Thai",
			"itemsonsale": 10
		}
	]

inventory = {
	"tv": 3,
	"sink": 7,
	"table": 65,
	"chair": 124
}

accounts = {
	"bank": 500000,
	"profit": 123456,
	"cost": 50000,
	"debt": 2100
}

discount = []

@app.route('/sutdcanteen')
def api_root():
    return 'Welcome the SUTD canteen API\n'

"""
GET examples
curl -v -X  GET localhost:5000/sutdcanteen/listofstalls
curl -v -X  GET localhost:5000/sutdcanteen/listofstalls?id=3

POST examples 
curl -v -X POST localhost:5000/sutdcanteen/listofstalls -H "Content-Type:application/json" -d '{"id":123,"name":"Korean","itemsonsale":50}'


"""
@app.route('/sutdcanteen/listofstalls', methods = ["GET", "POST"])
def api_listofstalls():
	global stalls
	if request.method == "POST":
		if request.headers["Content-Type"] == "application/json":
			obj = request.json
			stalls.append(obj)
		return getJSONResp(stalls, 201)
	elif request.method == "GET":
		if "id" in request.args:
			target = request.args["id"]
			target = int(target)
			for elems in stalls:
				if elems["id"] == target:
					return getJSONResp(elems, 200)
			return query_not_found()
		else:	
			logI("list all stalls")
			return getJSONResp(stalls, 200)

"""
PUT examples
curl -v -X  PUT localhost:5000/sutdcanteen/listofstalls/2?name="Vietnamese"\&items=10000
curl -v -X  PUT localhost:5000/sutdcanteen/listofstalls/2?name="Western"
curl -v -X  PUT localhost:5000/sutdcanteen/listofstalls/2?items=54

DELETE examples
curl -v -X DELETE localhost:5000/sutdcanteen/listofstalls/<id>
curl -v -X DELETE localhost:5000/sutdcanteen/listofstalls/158

GET examples
curl -v -X GET localhost:5000/sutdcanteen/listofstalls/1

"""
@app.route('/sutdcanteen/listofstalls/<int:stallid>', methods = ["GET", "PUT", "DELETE"])
def api_stall(stallid):
	global stalls
	target = int(stallid)
	for idx in xrange(len(stalls)):
		if stalls[idx]["id"] == target:
			if request.method == "GET":		
				return getJSONResp(stalls[idx], 200)
			elif request.method == "PUT":
				if "items" in request.args:
					stalls[idx]["itemsonsale"] = request.args["items"]
				if "name" in request.args:
					stalls[idx]["name"] = request.args["name"]
				return getJSONResp(stalls[idx], 200)
			elif request.method == "DELETE":
				del stalls[idx]
				return getJSONResp(stalls, 200)
	return query_not_found()
	
"""
PUT examples
curl -v -X  PUT localhost:5000/sutdcanteen/discount

DELETE examples
curl -v -X DELETE localhost:5000/sutdcanteen/discount/<id>

GET examples
curl -v -X GET localhost:5000/sutdcanteen/discount/1

"""
@app.route('/sutdcanteen/discount/<int:stallid>', methods = ["GET", "DELETE"])
def api_discount(stallid):
	global discount
	target = int(stallid)
	for idx in xrange(len(discount)):
		if discount[idx]["id"] == target:
			if request.method == "GET":		
				return getJSONResp(discount[idx], 200)			
			elif request.method == "DELETE":
				del discount[idx]
				return getJSONResp(discount, 200)
	return query_not_found()

"""
GET examples
curl -v -X GET localhost:5000/sutdcanteen/discount
"""
@app.route('/sutdcanteen/discount', methods = ["GET"])
def api_discount_all():
	global discount
	return getJSONResp(discount, 200)

"""
PUT examples
curl -v -X  PUT localhost:5000/sutdcanteen/discount
"""
@app.route('/sutdcanteen/discount', methods = ["PUT"])
def api_discount_put():
	global discount
	if request.method == "PUT":
		if request.headers["Content-Type"] == "application/json":
			obj = request.json
			for idx in xrange(len(discount)):
				if obj["id"] == int(discount[idx]["id"]):
					del discount[idx]
			discount.append(obj)
			return getJSONResp(discount, 200)	
	return query_not_found()

"""
GET examples
curl -v -X GET localhost:5000/sutdcanteen/inventory

PATCH examples
curl -v -X  PATCH localhost:5000/sutdcanteen/inventory?name="chair"\&new=421

DELETE examples
curl -v -X DELETE localhost:5000/sutdcanteen/inventory?name="chair"

POST examples
curl -v -X POST localhost:5000/sutdcanteen/inventory -H "Content-type:application/json" -d '{"chair":500}'
OR
curl -v -X POST localhost:5000/sutdcanteen/inventory -H "Content-type:text/plain" -d 'lamp:5'


"""
@app.route('/sutdcanteen/inventory', methods = ["GET", "PATCH", "DELETE", "POST"])
def api_inventory():
	global inventory
	if request.method == "GET":
		return getJSONResp(inventory, 200)
	elif request.method == "POST":
		if request.headers["Content-Type"] == "application/json":
			obj = request.json
			inventory.update(obj)
			return getJSONResp(inventory, 201)
		if request.headers["Content-Type"] == "text/plain":
			obj = request.data
			lis = re.split(":", obj)
			try:
				temp = {
					lis[0]: int(lis[1])
				}
				inventory.update(temp)
				return getJSONResp(inventory, 201)
			except ValueError:
				error_message = {
					"message": "Please key in the text in this format ('<name>':<number>)"
				}
				return getJSONResp(error_message, 500)
	elif request.method == "DELETE":
		if "name" in request.args:
			del inventory[request.args["name"]]
			return getJSONResp(inventory, 200)
		else:
			return query_not_found()
	elif request.method == "PATCH":
		if "name" in request.args and "new" in request.args:
			inventory[request.args["name"]] = request.args["new"]
			return getJSONResp(inventory, 200)

"""
GET example
curl -v -X GET localhost:5000/sutdcanteen/inventory/chair
curl -v -X GET localhost:5000/sutdcanteen/inventory/table

DELETE example
curl -v -X DELETE localhost:5000/sutdcanteen/inventory/tv
curl -v -X DELETE localhost:5000/sutdcanteen/inventory/table
"""
@app.route('/sutdcanteen/inventory/<name>', methods = ["GET", "DELETE"])
def api_inventory_item(name):
	global inventory
	try:
		if request.method == "GET":
			result = {
				name: inventory[name]
			}
			return getJSONResp(result, 200)
		elif request.method == "DELETE":
			del inventory[name]
			return getJSONResp(inventory, 200)
	except KeyError:
		return query_not_found()




def authenticate(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth:
        	# if no authentication credentials provided
			return error_authenticate("Please provide login credentials in the format of <user>:<pass>")
		elif not check_credentials(auth.username, auth.password):
			return error_authenticate("Wrong username and password provided. Please try again")
		return f(*args, **kwargs)
	return decorated


def check_credentials(user, password):
	global user_pass
	if user in user_pass:
		return password == user_pass[user]
	return False



def error_authenticate(msg):
	message = {
		"message": msg
	}
	resp = getJSONResp(message, 401)
	resp.headers["WWW-Authenticate"] = 'Basic realm="Login required"'
	return resp


"""
GET example
curl -v -X GET localhost:5000/sutdcanteen/accounts -u 'admin:Password123'

PATCH example
curl -v -X PATCH localhost:5000/sutdcanteen/accounts?name="bank"\&new="200540" -u 'admin2:Password1'

"""
@app.route('/sutdcanteen/accounts', methods = ["GET", "PATCH"])
@authenticate
def api_accounts():
	global accounts
	if request.method == "GET":
		return getJSONResp(accounts, 200)
	elif request.method == "PATCH":
		if "name" in request.args and "new" in request.args:
			if request.args["name"] in accounts:
				accounts[request.args["name"]] = int(request.args["new"])
				return getJSONResp(accounts, 200)
			else:
				return getJSONResp({"message": "Key does not exist"}, 404)
		else:
			return getJSONResp({"message": "Params error"}, 500)

"""
GET example
curl -v -X GET localhost:5000/sutdcanteen/accounts/profit -u 'admin:Password123'

curl -v -X GET localhost:5000/sutdcanteen/accounts/bank -u 'admin:Password123'

"""
@app.route('/sutdcanteen/accounts/<name>', methods = ["GET"])
@authenticate
def api_accounts_component(name):
	global accounts
	if request.method == "GET":
		temp = {
			name: accounts[name]
		}
		return getJSONResp(temp, 200)


@app.errorhandler(404)
def query_not_found(error=None):
	error_message = {
		"status" : 404,
		"message" : "The query that you were searching for is not found"
	}
	return getJSONResp(error_message, 404)

"""
Convenient method for returning a JSON response
"""
def getJSONResp(diction, status):
	js = json.dumps(diction, indent=4, separators=(',', ': '))
	resp = Response(js, status, mimetype="application/json")
	return resp

"""
Convenient method for logging(info)
"""
def logI(stringmsg):
	app.logger.info(stringmsg)

"""
Convenient method for logging(error)
"""
def logE(stringmsg):
	app.logger.error(stringmsg)

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)

