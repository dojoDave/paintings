from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User():
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.paintings = []
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create_user(cls,data):   

        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        new_user = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
       
        return new_user

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        check_user = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)

        if(check_user):
            return check_user[0]
        else:
            return False


###### VALIDATIONS ######

    @staticmethod
    def validate_login(user):
        valid = True
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not email_regex.match(user['email']):
            flash("Email can't be blank and needs to be valid")
            valid = False
        if len(user['password']) < 1:
            flash("Password field needs to be filled out")
            valid = False        
        return valid

    @staticmethod
    def validate_register(user):
        valid = True
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            valid = False
        if not email_regex.match(user['email']):
            flash("Email can't be blank, at least 8 characters, and needs to be valid")
            valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            valid = False
        if user["password"] != user["confirm_password"]:
            flash("Passwords do not match")
            valid = False
        
        return valid
           
            