import os
os.chdir(r'c:\Users\Antho\OneDrive\Documents\Programming\workspace\Chatter\backend')
from app import create_app
app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
for rule in app.url_map.iter_rules():
    print(rule.endpoint, rule.rule)
