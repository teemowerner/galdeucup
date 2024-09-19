import os
from flask import Flask, send_from_directory
from models import db  # 모델에서 db 가져오기

app = Flask(__name__, static_folder="static", template_folder="static")

# 데이터베이스 설정
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'galdeucup.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # SQLAlchemy 쿼리 로깅 활성화

# SQLAlchemy 객체 초기화
db.init_app(app)

@app.route('/')
def serve_vue_app():
    return send_from_directory(app.static_folder, 'index.html')

# 명시적으로 테이블 생성
if __name__ == '__main__':
    from models import Category, Item  # 모델 불러오기
    with app.app_context():  # 애플리케이션 컨텍스트 내에서 테이블 생성
        print("Attempting to create tables inside app context...")
        db.create_all()
        print("Tables created (if not already existing).")
    app.run(debug=True)
