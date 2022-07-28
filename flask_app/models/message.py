from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
from flask import flash
from datetime import datetime
import math
from flask_app.models import user

class Message:
    db = "tunas_only_schema"
    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.recipient_id = data['recipient_id']
        self.recipient = data['recipient']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (message, sender_id, recipient_id, created_at, updated_at) VALUES (%(message)s,  %(sender_id)s,  %(recipient_id)s, now(), now())"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages;"
        results = connectToMySQL(cls.db).query_db(query)
        messages = []
        for row in results:
            messages.append( cls(row))
        return messages

    @classmethod
    def get_by_conversation(cls,data):
        query = "SELECT users.first_name as sender, users2.first_name as recipient, messages.* FROM users LEFT JOIN messages ON users.id =  messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.recipient_id WHERE users2.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages
        
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"
    
    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM messages WHERE messages.id = %(message_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    

