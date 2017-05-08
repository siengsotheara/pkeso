from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Flask going to be deployed.</h1>'
	
@app.route('/login')
def login():
	return '<h3>this is login page.</h3>'

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)