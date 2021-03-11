from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

client = app.test_client()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_number = db.Column(db.Integer, nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')


@app.route('/database')
def database():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('database.html', articles=articles)


@app.route('/database/<int:id>', methods=['GET'])
def details(id):
    article = Article.query.get(id)
    return render_template('details.html', article=article)


# Increment
@app.route('/adding', methods=['POST', 'GET'])
def adding():
    result = ()
    if request.method == "POST":
        user_number = int(request.form['added'])
        # Inserted number is absent in DB
        if Article.query.filter_by(user_number=user_number).first() is None:
            # Increased number is absent in DB
            if Article.query.filter_by(user_number=user_number + 1).first() is None:
                increased = request.json(int(user_number) + 1)
                article = Article(user_number=increased)
                try:
                    # Adding increased number to DB
                    db.session.add(article)
                    db.session.commit()
                    result = 'Added', 200
                except:
                    result = 'An error occurred by adding', 500
            # Increased number is already in DB
            else:
                result = 'Inserted number has been already increased and added to database', 400
        # Inserted number is already in DB
        else:
            result = 'This number already exists in database', 400
        print(result)
    return render_template('adding.html')


@app.route('/database/<int:id>/delete', methods=['DELETE'])
def delete(id):
    article = Article.query.get_or_404(id)
    if not article:
        return {'message': 'No number with such id'}, 400
    try:
        db.session.delete(article)
        db.session.commit()
        return 'Deleted', 200
    except:
        return 'An error occurred by deleting', 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
