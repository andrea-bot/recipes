from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name= data['name']
        self.descriptions = data['descriptions']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.under_thirty = data['under_thirty']
        
    @staticmethod
    def validate_Recipe(form_data):
        is_valid = True
        print(form_data)
        if form_data['name']=="":
            flash("name must be given!","name")
            is_valid=False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name,descriptions,under_thirty,instructions,user_id) VALUES ( %(name)s,%(user_id)s,%(descriptions)s,%(instrucitons)s,%(under_thirty)s);"

        new_recipe_id = connectToMySQL('recipes_db').query_db(query, data)

        return new_recipe_id


    @classmethod
    def get_one (cls,data):
        query="SELECT * FROM recipes where id =%(id)s;"
        result = connectToMySQL('recipes_db').query_db(query,data)
        recipe = cls(result[0])

        return recipe
    


    @classmethod
    def update(cls,data):
        query="UPDATE cars SET name=%(name)s,descriptions=%(description)s,user_id=%(user_id)s,instructions=%(instructions)s,under_thirty=%(under_thirty)s WHERE id=%(id)s;"
        result=connectToMySQL('cardealz_db').query_db(query,data)
        return data['id']
        

    @classmethod
    def delete(cls,data):
        query ="DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL('recipes_db').query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_db').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes