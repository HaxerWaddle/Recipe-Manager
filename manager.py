from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    descriptions = db.relationship('Recipe_Desc', backref='recipe', lazy=True)
    def __repr__(self):
        return f'<Recipe {self.id!r}>'
    
class Recipe_Desc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<Recipe_Desc {self.id}: {self.desc}>' 

with app.app_context():
    db.create_all()
    
@app.route('/', methods=["GET", 'POST'])
def home():
    if request.method == "POST":
        recipe_content = request.form['content']
        new_recipe = Recipe(content=recipe_content)
        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while adding recipe.'
    else:
        recipes = Recipe.query.order_by(Recipe.id).all()
        return render_template('page.html', recipes=recipes)

@app.route('/delete/<int:id>')
def delete(id):
    recipe_to_del = Recipe.query.get_or_404(id)

    try:
        db.session.delete(recipe_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error while deleting recipe.'

@app.route('/details/<string:content>/<int:id>')
def details(content, id):
    recipe = Recipe.query.get_or_404(id)

    return render_template('detail.html', recipe=recipe)

@app.route('/details/<string:content>/<int:id>/edit', methods=['GET', 'POST'])
def edit(content, id):
    recipe_to_edit = Recipe.query.get_or_404(id)

    if request.method == "POST":
        try:
            recipe_to_edit.content = request.form['recipe_content']
            db.session.commit()
            return redirect(url_for('edit', content=recipe_to_edit.content, id=id))

        except:
            db.session.rollback()
            return "Error while updating recipe content."

    return render_template('detail-edit.html', recipe=recipe_to_edit)

@app.route('/details/<string:content>/<int:id>/add_desc', methods=["POST"])
def add_desc(content, id):
    recipe = Recipe.query.get_or_404(id)

    if request.method == "POST":
        description = request.form['desc_content']
        new_desc = Recipe_Desc(desc=description, recipe_id=id)
        try:
            db.session.add(new_desc)
            db.session.commit()
            return redirect(url_for('edit', content=recipe.content, id=id))  # Reload page to show new description
        
        except:
            db.session.rollback()
            return "Error while adding description."

    return redirect(url_for('edit', content=recipe.content, id=id))  # Just in case

@app.route('/details/<string:content>/<int:id>/del_desc/<int:desc_id>')
def del_desc(content, id, desc_id):
    recipe = Recipe.query.get_or_404(id)
    desc_to_del =  Recipe_Desc.query.get_or_404(desc_id)

    try:
        db.session.delete(desc_to_del)
        db.session.commit()
    except:
        return 'Error while deleting description.'
    
    return redirect(url_for('edit', content=recipe.content, id=id))



if __name__ == "__main__":
    app.run(debug=True)