from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from flask_swagger_ui import get_swaggerui_blueprint
#from routes import request_api

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/database')
def database():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('database.html', articles=articles)


@app.route('/database/<int:id>')
def details(id):
    article = Article.query.get(id)
    return render_template('details.html', article=article)


# Increment
@app.route('/adding', methods=['POST', 'GET'])
def adding():
    if request.method == "POST":
        user_number = int(request.form['added'])
        if Article.query.filter_by(user_number=user_number).first() is None:
            if Article.query.filter_by(user_number=user_number+1).first() is None:
                increased = int(user_number) + 1
                article = Article(user_number=increased)
            else:
                return 'Inserted number has been already increased and added to database'

            try:
                db.session.add(article)
                db.session.commit()
                return redirect('/database')
            except:
                return 'An error occurred by adding'
        else:
            return 'This number already exists in database'
    return render_template('adding.html')


@app.route('/database/<int:id>/delete')
def delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/database')
    except:
        return 'An error occurred by deleting'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
