from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Painting():
    def __init__(self,data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.price = data["price"]
        self.quantity = data["quantity"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create_painting(cls,data):   

        query = "INSERT INTO paintings (title,description,price,user_id,quantity) VALUES (%(title)s,%(description)s,%(price)s,%(user_id)s,%(quantity)s)"
        new_painting = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
       
        return new_painting

    @classmethod
    def get_all_paintings(cls):   

        query = "SELECT * FROM users JOIN paintings ON users.id = paintings.user_id"
        all_paintings = connectToMySQL("exam_paintings_blackbelt").query_db(query)
        return all_paintings
    
    @classmethod
    def get_all_purchpaintings(cls,data):
        query = "SELECT * FROM boughtpaintings AS bp JOIN paintings AS p ON bp.painting_id = p.id JOIN users AS u ON u.id = p.user_id WHERE bp.user_id = %(user_id)s"
        all_purch_paintings = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
        return all_purch_paintings

    @classmethod
    def count_purchased(cls,data):
        query = "SELECT count(*) AS total FROM boughtpaintings WHERE painting_id = %(painting_id)s GROUP BY painting_id"
        total_purchases = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
        return total_purchases

    @classmethod
    def view_painting(cls,data):   

        query = "SELECT * FROM users JOIN paintings ON users.id = paintings.user_id WHERE paintings.id = %(painting_id)s"
        painting = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
        return painting

    @classmethod
    def edit_painting(cls,data):   

        query = "UPDATE paintings SET title=%(title)s,description=%(description)s,price=%(price)s,user_id=%(user_id)s,quantity=%(quantity)s WHERE id = %(painting_id)s"
        
        updated_painting = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
        return updated_painting

    @classmethod
    def delete_painting(cls,data):   

        query = "DELETE FROM paintings WHERE id = %(painting_id)s"
        deleted_painting = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
        return deleted_painting

    @classmethod
    def buy_painting(cls,data):   

        query = "INSERT INTO boughtpaintings (user_id,painting_id) VALUES (%(user_id)s,%(painting_id)s)"

        bought_painting = connectToMySQL("exam_paintings_blackbelt").query_db(query,data)
        return bought_painting

###### VALIDATIONS ######

    @staticmethod
    def validate_painting(painting):
        valid = True 
        if len(painting['title']) < 2:
            flash("Title must be more than 2 characters")
            valid = False
        if len(painting['description']) < 10:
            flash("Description must be more than 10 characters")
            valid = False
        if len(painting['price']) < 1 or int(painting['price']) <= 0:
            flash("Price can't be blank and must be more than $0")
            valid = False
        if len(painting['quantity']) < 1 or int(painting['quantity']) <= 0:
            flash("Quantity can't be blank and must be more than 0")
            valid = False            
        return valid
           
            