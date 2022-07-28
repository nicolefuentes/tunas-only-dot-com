from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
from flask import flash
from flask_app.models import user
from datetime import datetime
import math
from flask_app.models import user

class Testimonial:
    db = "tunas_only_schema"
    def __init__(self,data):
        self.id = data['id']
        self.testimonial = data['testimonial']
        self.share = data['share']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO testimonials (testimonial, share, user_id, created_at, updated_at) VALUES (%(testimonial)s, %(share)s,  %(user_id)s, now(), now())"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM testimonials;"
        results = connectToMySQL(cls.db).query_db(query)
        testimonials = []
        for testimonial in results:
            testimonials.append(cls(testimonial))
        return testimonials

    @classmethod
    def get_testimonials(cls):
        query = "SELECT users.first_name, users.last_name, testimonials.* FROM users LEFT JOIN testimonials ON users.id =  testimonials.user_id WHERE testimonials.share = 'yes';"
        results = connectToMySQL(cls.db).query_db(query)
        testimonials = []
        for testimonial in results:
            testimonials.append(cls(testimonial))
        return testimonials
    

