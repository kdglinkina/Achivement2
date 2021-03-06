from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://guest:12345678@91.77.169.186:5432/storage"

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
@app.route('/adding/<int:num>', methods=['GET'])
def adding(num):
    result = ""
    if request.method == "GET":
        user_number = int(num)
        # Inserted number is absent in DB
        if Article.query.filter_by(user_number=user_number).first() is None:
            # Increased number is absent in DB
            if Article.query.filter_by(user_number=user_number + 1).first() is None:
                increased = int(user_number) + 1
                article = Article(id=user_number,user_number=user_number)
                try:
                    # Adding increased number to DB
                    db.session.add(article)
                    db.session.commit()
                    result = 'Added {}'.format(increased)
                except:
                    result = 'An error occurred by adding'
            # Increased number is already in DB
            else:
                result = 'Inserted number has been already increased and added to database'
        # Inserted number is already in DB
        else:
            result = 'This number already exists in database'
        print(result)
    return {"result": result }



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

print (SQLALCHEMY_DATABASE_URI)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
