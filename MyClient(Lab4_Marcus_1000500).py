'''
Networks Lab 4
Name: Tan Yi Xiang Marcus
ID: 1000500
'''
from requests.auth import HTTPBasicAuth
import requests as rq
from flask import json

server_ip = "http://127.0.0.1:5000"

'''
Gets the list of stalls in the canteen
Returns a JSON object of the list of stalls
Return format: (JSON response from server, JSON data in string)
'''
def getListOfStallsClient(id = None):
	if id == None:
		r = rq.get(server_ip + "/sutdcanteen/listofstalls")
		return r.json, r.text
	else:
		r = rq.get(server_ip + "/sutdcanteen/listofstalls/" + str(id))
		return r.json, r.text

'''
Puts in a new stall entry
Returns json object of all the stalls on successful POST
Return format: (JSON response from server, JSON data in string)
'''
def putNewStall(id, name, itemsonsale):
	# newStall is a json
	newStall = {
		"id" : id,
		"name" : name + "",
		"itemsonsale": int(itemsonsale)
	}
	headers = {'content-type':'application/json'}
	r = rq.post(server_ip + "/sutdcanteen/listofstalls", data = json.dumps(newStall), headers = headers)
	return r.json, r.text

'''
Edits information about stall with the id provided
Returns json object of all the stalls on successful PUT
Return format: (JSON response from server, JSON data in string)
'''
def editCurrentStall(id, name, itemsonsale=None):
	id = str(id)
	if name != None and itemsonsale == None:
		r = rq.put(server_ip + "/sutdcanteen/listofstalls/" + id + "?name=" + name)
		return r.json, r.text
	elif name != None and itemsonsale != None:
		r = rq.put(server_ip + "/sutdcanteen/listofstalls/" + id + "?name=" + name + "\&" + "items=" + str(itemsonsale))
		return r.json, r.text

'''
Deletes the stall with the id provided
Returns json object of all the stalls on successful DELETE
Return format: (JSON response from server, JSON data in string)
'''
def deleteStall(id):
	r = rq.delete(server_ip + "/sutdcanteen/listofstalls/" + str(id))
	return r.json, r.text

'''
Gets the accounts for the canteen
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def requestCanteenAccounts(username, password, name = None):
	if name == None:
		r = rq.get(server_ip + "/sutdcanteen/accounts", auth=HTTPBasicAuth(username, password))
		return r.json, r.text
	else:
		r = rq.get(server_ip + "/sutdcanteen/accounts/" + name, auth=HTTPBasicAuth(username, password))
		return r.json, r.text

'''
Modifies the accounts for the canteen
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def modifyCanteenAccounts(username, password, namekey, newvalue):
	r = rq.patch(server_ip + "/sutdcanteen/accounts?name=" + namekey + "&new=" + str(newvalue), auth=HTTPBasicAuth(username, password))
	return r.json, r.text

'''
Gets the inventory for the canteen
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def getCanteenInventory(namekey=None):
	if namekey == None:
		r = rq.get(server_ip + "/sutdcanteen/inventory")
		return r.json, r.text
	else:
		r = rq.get(server_ip + "/sutdcanteen/inventory/" + namekey)
		return r.json, r.text

'''
Modifies the inventory for the canteen, adds a new entry if not found
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def modifyOrAddCanteenInventory(namekey, newvalue):	
	r = rq.patch(server_ip + "/sutdcanteen/inventory?name="  + namekey + "&new=" + str(newvalue))
	return r.json, r.text

'''
Adds the given stall into the Discount list
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def addIntoDiscount(id):
	temp = {}
	js = json.loads(getListOfStallsClient(id)[1])
	for key in js.items():
		if isinstance(key[1], unicode):
			temp[key[0].encode('ascii', 'ignore')] = key[1].encode('ascii', 'ignore')
		else :
			temp[key[0].encode('ascii', 'ignore')] = key[1]
	r = rq.put(server_ip + "/sutdcanteen/discount", headers={'content-type': 'application/json'}, data=json.dumps(temp))
	return r.json, r.text

'''
Gets information about the given stall in the Discount list
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def getDiscountStall(id):
	r = rq.get(server_ip + "/sutdcanteen/discount/" + str(id))
	return r.json, r.text

'''
Gets information about the stalls in the Discount list
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def getDiscountStalls():
	r = rq.get(server_ip + "/sutdcanteen/discount")
	return r.json, r.text

'''
Delete the stall with the given id in the Discount list
Returns json object of canteen accounts
Return format: (JSON response from server, JSON data in string)
'''
def deleteDiscountStall(id):
	r = rq.delete(server_ip + "/sutdcanteen/discount/" + str(id))
	return r.json, r.text

print getDiscountStalls()[1]

print addIntoDiscount(2)[1]

print getDiscountStalls()[1]

print deleteDiscountStall(2)[1]

print getDiscountStalls()[1]
# print modifyCanteenAccounts("admin", "Password123", "bank", 650165)[1]