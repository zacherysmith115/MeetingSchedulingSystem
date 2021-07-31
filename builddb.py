from mss import db
from mss.models import *

db.drop_all()
db.create_all()

db.session.add(Admin(first_name='Zachery', last_name='Smith', email='zachery.smith@pss.com', password='password'))
db.session.add(Admin(first_name='Sandy', last_name='Lee', email='sandy.lee@pss.com', password='password'))
db.session.add(Admin(first_name='Hope', last_name='Fisher', email='hope.fisher@pss.com', password='password'))

db.session.add(Client(first_name='John', last_name='Doe', email='john.doe@pss.com', password='password'))
db.session.add(Client(first_name='Sarah', last_name='Brown', email='sarah.brown@pss.com', password='password'))
db.session.add(Client(first_name='James', last_name='Cook', email='james.cook@pss.com', password='password'))
db.session.add(Client(first_name='Kelly', last_name='Chen', email='kelly.chen@pss.com', password='password'))

db.session.commit()

db.session.close()