from flask_sqlalchemy import SQLAlchemy
from slugify import slugify  # 'python-slugify' 라이브러리를 사용해 URL-friendly 문자열 생성

# SQLAlchemy 객체 생성 (초기화는 app.py에서 수행)
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        # 'name'을 바탕으로 'url' 필드를 자동 생성
        self.url = slugify(name)
    def to_dict(self):
        # 한국어에서 영어로 번역
        return {"id": self.id, "name": self.name, "url": self.url}

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "votes": self.votes, "category_id": self.category_id}

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    item = db.relationship('Item', backref=db.backref('vote_records', lazy=True))
