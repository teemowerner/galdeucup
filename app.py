import os
from flask import Flask, send_file, abort, request, jsonify, render_template
from models import db, Category, Item  # 필요한 모델들 임포트
from views import main  # 블루프린트 임포트

app = Flask(__name__)  # 기본 설정으로 변경 (static_folder 제거)

# 현재 파일의 디렉토리 경로를 가져와서 절대 경로로 SQLite 파일 생성
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'galdeucup.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 블루프린트 등록
app.register_blueprint(main)

@app.route('/')
def index():
    # 카테고리 목록 조회
    categories = Category.query.all()
    # 카테고리 목록을 index.html로 전달
    return render_template('index.html', categories=categories)

@app.route('/category/<string:url>', methods=['GET'])
def category_page(url):
    print(f"Requested URL: {url}")  # URL이 제대로 들어오는지 확인하는 로그
    # 해당 URL에 맞는 카테고리 찾기
    category = Category.query.filter_by(url=url).first()

    if category is None:
        return jsonify({"error": "해당 카테고리를 찾을 수 없습니다."}), 404

    # 해당 카테고리에 속한 아이템 목록 조회
    items = Item.query.filter_by(category_id=category.id).order_by(Item.votes.desc()).all()

    return render_template('category_page.html', category=category, items=items)

@app.route('/vote', methods=['POST'])
def vote_item():
    data = request.json
    item_id = data.get('item_id')

    if not item_id:
        return jsonify({"error": "아이템 ID가 필요합니다."}), 400

    # 해당 아이템을 찾음
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"error": "해당 아이템을 찾을 수 없습니다."}), 404

    # 투표 수를 증가시킴
    item.votes += 1
    db.session.commit()

    return jsonify({"message": f"'{item.name}'에 투표가 성공적으로 반영되었습니다.", "votes": item.votes}), 200

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    name = data.get('name')
    category_id = data.get('category_id')

    if not name or not category_id:
        return jsonify({"error": "아이템 이름과 카테고리 ID가 필요합니다."}), 400

    # 데이터베이스에 새 아이템 저장
    new_item = Item(name=name, category_id=category_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": f"'{name}' 아이템이 추가되었습니다."}), 201

@app.route('/create_category', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "카테고리 이름이 필요합니다."}), 400

    # 중복 카테고리 확인
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({"error": f"'{name}' 카테고리가 이미 존재합니다."}), 400

    # URL을 생성 (카테고리 이름을 소문자로 변환하고 공백을 하이픈으로 교체)
    url = name.lower().replace(' ', '-')

    # 새로운 카테고리 생성 및 데이터베이스에 저장
    category = Category(name=name, url=url)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": f"'{name}' 카테고리가 성공적으로 추가되었습니다."}), 201

if __name__ == '__main__':
    with app.app_context():
        # 데이터베이스 생성 시 경로 출력
        print(f"Creating database at: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
        print("Tables created.")
    app.run(debug=True)
