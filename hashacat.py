#!.//venv/bin/python

from flask import Flask, send_file, request, render_template
from flask.ext.jsonpify import jsonify
from corsSupport import crossdomain
from rateLimiting import rate_limit
import re
import os, os.path
import hashlib
import random
import base64
app = Flask(__name__)

def updateCatCount():
	global catCount 
	catCount = len(os.walk('./static/cats/').next()[2])
	pass


def verifyHash(hash):
		return bool(re.search("^([a-f0-9]{40})$|^([a-f0-9]{32})$", hash))

@app.route('/cat/<hash>')
@crossdomain(origin='*')
@rate_limit(5, 3)
def returnCat(hash):
	if verifyHash(hash):
		catID = int(hash, 16) % catCount
		if request.args.get('size') == 'small':
			catURL = "http://cats.hashacat.com/small/" + str(catID) + ".gif"
		else:
			catURL = "http://cats.hashacat.com/" + str(catID) + ".jpg"
		if request.args.get('format') == 'json':
			return jsonify(cat=catURL)
		else:
			if request.args.get('size') == 'small':
				catPath = 'static/cats/small' + str(catID) + '.gif'
			else:
				catPath = 'static/cats/' + str(catID) + '.jpg'
			return send_file(catPath)
	else:
		return "Bad hash!"


@app.route('/info')
def displayInfo():
	return render_template('info.html')
	
	
@app.route('/randomHash')
@rate_limit(5, 3)
def getRandomHash():
	hash = hashlib.sha1(str(random.random())).hexdigest()
	return jsonify(hash=hash)
	
	
@app.route('/hash/<hashText>')
@rate_limit(5, 3)
def getHash(hashText):
	try:
		decoded = base64.b64decode(hashText)
		hash = hashlib.sha1(str(decoded[:255])).hexdigest()
		return jsonify(hash=hash)
	except:
		return "Couldn't hash that, is it base64?"
	

@app.route('/')
def displayIndex():
	return render_template('mainPage.html')


if __name__ == '__main__':
	app.run()

updateCatCount()
