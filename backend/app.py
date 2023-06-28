from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

# Create the object of Flask
app = Flask(__name__)

# Sqlalchemy Database configuration with MySql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/python_articles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body


class ArticleShema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


article_schema = ArticleShema()
articles_schema = ArticleShema(many=True)


@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)


@app.route('/delete/<id>/', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/add', methods=['POST'])
def add_articles():
    title = request.json['title']
    body = request.json['body']

    article = Articles(title, body)
    db.session.add(article)
    db.session.commit()
    return article_schema.jsonify(article)


if __name__ == "__main__":
    app.run(debug=True)
