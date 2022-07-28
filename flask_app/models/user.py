from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import message

class User:
    db = "tunas_only_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthdate = data['birthdate']
        self.user_type = data['user_type']
        self.looking_for = data['looking_for']
        self.bio = data['bio']
        self.profile_photo = data['profile_photo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, birthdate, user_type, looking_for, bio, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(birthdate)s,%(user_type)s,%(looking_for)s,%(bio)s,NOW(),NOW());"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id_except(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        users = []
        for row in results:
            users.append( cls(row))
        return users
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,birthdate=%(birthdate)s,user_type=%(user_type)s,looking_for=%(looking_for)s,bio=%(bio)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM users WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid= False
        return is_valid

    @staticmethod
    def validate_user_update(user_update):
        is_valid = True
        if not EMAIL_REGEX.match(user_update['email']):
            flash("Invalid Email","user_update")
            is_valid=False
        if len(user_update['first_name']) < 3:
            flash("First name must be at least 3 characters","user_update")
            is_valid= False
        if len(user_update['last_name']) < 3:
            flash("Last name must be at least 3 characters","user_update")
            is_valid= False
        return is_valid