from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from Models import Dailies, Daily, Sections, Notes


app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True

api.add_resource(Dailies, '/api/dailies')
api.add_resource(Daily, '/api/dailies/<int:week>')
api.add_resource(Sections, '/api/sections')
api.add_resource(Notes, '/api/notes')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

