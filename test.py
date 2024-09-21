from app import db, app
from sqlalchemy import inspect
from googletrans import Translator
from slugify import slugify
a = Translator().translate('나이키윔블던', src='ko', dest='en')
print(a.text.lower())
print(slugify("대학교3학년").lower())