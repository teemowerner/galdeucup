from app import db, app
from sqlalchemy import inspect

# 애플리케이션 컨텍스트 내에서 실행
with app.app_context():
    inspector = inspect(db.engine)
    print(inspector.get_table_names())
