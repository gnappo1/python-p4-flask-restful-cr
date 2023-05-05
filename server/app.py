#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        
        response = make_response(
            response_dict,
            200
        )

        return response
api.add_resource(Home, '/')
class Newsletters(Resource):
    def get(self):
        response_dict_list = [
            news.to_dict() for news in Newsletter.query.all()
        ]
        
        response = make_response(
            response_dict_list,
            200
        )
        return response

    def post(self):
        # retrieve data from request and make a newsletter object
        new_dict = Newsletter(
            title=request.json['title'], 
            body=request.json['body']
        )
        # add and commit to the session
        db.session.add(new_dict)
        db.session.commit()
        # use the to_dict() method on the object and prepare the response
        response = make_response(new_dict.to_dict(), 201)
        
        return response
        
api.add_resource(Newsletters, '/newsletters')

class NewsletterById(Resource):
    
    def get(self, id):
        newsletter = Newsletter.query.filter(Newsletter.id==id).first()
        response = make_response(newsletter.to_dict(), 200)
        return response
        
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
