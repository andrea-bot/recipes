from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    data ={
        'id' : session['logged_user']
    }
    logged_user = User.get_one(data)
    all_recipes = Recipe.get_all()
    return render_template('dashboard.html', user = logged_user, recipes = all_recipes)

@app.route('/recipes/add')
def add_recipe():
    return render_template('add.html')

@app.route('/recipes/create',methods=['post'])
def create_recipes():

    if not Recipe.validate_Recipe(request.form):
        return redirect('/recipes/add')  

    data= {
        'name': request.form['name'],
        'descriptions': request.form['descriptions'],
        'instructions': request.form['instructions'],
        'under_thirty': request.form['under_thirty'],
        'user_id': session['logged_user'],
        
    }

    new_recipe_id = Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    data ={
        'id':id
    }
    recipe=Recipe.get_one(data)
    return render_template('edit.html',recipe = recipe)

@app.route('/recipes/<int:id>/update',methods=['post'])
def update_recipe(id):

    if not Recipe.validate_Recipe(request.form):
        return redirect(f'/recipes/{id}/edit')  
    
    data= {
        'name': request.form['name'],
        'descriptions': request.form['description'],
        'instructions': request.form['instructions'],
        'under_thirty': request.form['under_thirty'],
        'user_id': session['logged_user'],
        'id':id
        
    }

    recipe_id=Recipe.update(data)
    print(recipe_id)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    data = {
        'id':id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/view')
def view_recipe(id):
    data ={
        'id':id
    }
    one_recipe = Recipe.get_one(data)
    
    return render_template('view.html', recipes = one_recipe)