from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from Models.Dailies import Dailies


app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True

api.add_resource(Dailies, '/api/dailies')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

