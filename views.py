from flask import Blueprint, jsonify, request
from models import db, Category, Item, Vote  # models.py에서 db, Category, Item을 가져오기

main = Blueprint('main', __name__)

@main.route('/create_category', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "카테고리 이름이 필요합니다."}), 400
    category = Category(name=name)
    db.session.add(category)
    print("teemo", category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

@main.route('/create_item', methods=['POST'])
def create_item():
    data = request.json
    name = data.get('name')
    category_id = data.get('category_id')

    if not name or not category_id:
        return jsonify({"error": "품목 이름과 카테고리 ID가 필요합니다."}), 400

    item = Item(name=name, category_id=category_id)
    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), 201

@main.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@main.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items(category_id):
    items = Item.query.filter_by(category_id=category_id).all()
    return jsonify([item.to_dict() for item in items])
