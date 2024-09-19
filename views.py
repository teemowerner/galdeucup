from flask import Blueprint, jsonify, request
from models import db, Item, Vote

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    def to_dict(self):
        print("teemo")
        return {"id": self.id, "name": self.name, "votes": self.votes, "category_id": self.category_id}

main = Blueprint('main', __name__)
# IP 기반 중복 투표 방지 로직
# POST 요청만 허용.
@main.route('/vote', methods=['POST'])
def vote_item():
    data = request.json
    item_id = data.get('item_id')
    ip_address = request.remote_addr  # 클라이언트의 IP 주소 가져오기

    # 이미 해당 IP가 투표했는지 확인
    existing_vote = Vote.query.filter_by(item_id=item_id, ip_address=ip_address).first()
    if existing_vote:
        return jsonify({"error": "이미 투표하셨습니다."}), 403

    # 새 투표 기록 추가
    new_vote = Vote(ip_address=ip_address, item_id=item_id)
    db.session.add(new_vote)

    # Item 테이블의 투표 수 증가
    item = Item.query.get_or_404(item_id)
    item.votes += 1
    db.session.commit()

    return jsonify(item.to_dict())

