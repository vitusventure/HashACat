#!venv/bin/python

from flask import Flask, jsonify, send_file, request, render_template
import re
import os, os.path
import hashlib
import random
app = Flask(__name__)

def updateCatCount():
	global catCount 
	catCount = len(os.walk('./static/cats/').next()[2])
	pass


def verifyHash(hash):
		return bool(re.search("^([a-f0-9]{40})$|^([a-f0-9]{32})$", hash))

@app.route('/cat/<hash>')
def returnCat(hash):
	if verifyHash(hash):
		catID = int(hash, 16) % catCount
		catURL = "http://cats.hashacat.com/" + str(catID) + ".jpg"
		if request.args.get('format') == 'json':
			return jsonify(cat=catURL)
		else:
			catPath = 'static/cats/' + str(catID) + '.jpg'
			return send_file(catPath)
	else:
		return "Bad hash!"


@app.route('/info')
def displayInfo():
	return render_template('info.html')
	
	
@app.route('/randomHash')
def getRandomHash():
	hash = hashlib.sha1(str(random.random())).hexdigest()
	return jsonify(hash=hash)


@app.route('/')
def displayIndex():
	return render_template('mainPage.html')
	

if __name__ == '__main__':
	app.run()

updateCatCount()
