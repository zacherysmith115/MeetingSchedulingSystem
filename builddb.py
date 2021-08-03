import datetime
from mss import db
from mss.models import *

# reset db
db.drop_all()
db.create_all()

# populate admin data
db.session.add(Admin(first_name='Zachery', last_name='Smith', email='zachery.smith@pss.com', password='password'))
db.session.add(Admin(first_name='Sandy', last_name='Lee', email='sandy.lee@pss.com', password='password'))
db.session.add(Admin(first_name='Hope', last_name='Fisher', email='hope.fisher@pss.com', password='password'))

# populate client data
john = Client(first_name='John', last_name='Doe', email='john.doe@pss.com', password='password')
sarah = Client(first_name='Sarah', last_name='Brown', email='sarah.brown@pss.com', password='password')
james = Client(first_name='James', last_name='Cook', email='james.cook@pss.com', password='password')
kelly = Client(first_name='Kelly', last_name='Chen', email='kelly.chen@pss.com', password='password')
db.session.add(john)
db.session.add(sarah)
db.session.add(james)
db.session.add(kelly)

# populate payment info
johns_card = Card(client_id=john.id, client=john, number='6988019516364371', name='John Doe', exp_date=datetime.date(year=2022, month=9, day=1), ccv='797')
sarahs_card = Card(client_id=sarah.id, client=sarah, number='5456141426522113', name='Sarah Brown', exp_date=datetime.date(year=2023, month=7, day=1), ccv='535')
james_card = Card(client_id=james.id, client=james, number='2302857125016344', name='James Cook', exp_date=datetime.date(year=2021, month=12, day=1), ccv='459')
kellys_card = Card(client_id=james.id, client=james, number='5215353134814512', name='James Cook', exp_date=datetime.date(year=2021, month=12, day=1), ccv='467')
db.session.add(johns_card)
db.session.add(sarahs_card)
db.session.add(james_card)
db.session.add(kellys_card)

# populate rooms
room_101 = Room(id=101)
room_102 = Room(id=102)
room_103 = Room(id=103)
room_200 = Room(id=200, special=True)
db.session.add(room_101)
db.session.add(room_102)
db.session.add(room_103)
db.session.add(room_200)

# populate meetings: all meetings will be based on week 8/9 - 8/13
m1_start_time = datetime.datetime(year=2021, month=8, day=9, hour=8)
m1_end_time = datetime.datetime(year=2021, month=8, day=9, hour=9)
m1 = Meeting(creator_id = john.id, creator=john, participants=[sarah, james, kelly], title='Monday morning meeting',
        room_id=room_101.id, room=room_101, start_time=m1_start_time, end_time=m1_end_time )

m2_start_time = datetime.datetime(year=2021, month=8, day=11, hour=12)
m2_end_time = datetime.datetime(year=2021, month=8, day=11, hour=13)
m2 = Meeting(creator_id = sarah.id, creator=sarah, participants=[john, james, kelly], title='Wednesday lunch',
        room_id=room_102.id, room=room_102, start_time=m2_start_time, end_time=m2_end_time )

m3_start_time = datetime.datetime(year=2021, month=8, day=13, hour=14)
m3_end_time = datetime.datetime(year=2021, month=8, day=13, hour=15)
m3 = Meeting(creator_id = james.id, creator=james, participants=[john, james, kelly], title='Friday afternoon meeting',
        room_id=room_103.id, room=room_103, start_time=m3_start_time, end_time=m3_end_time )

db.session.add(m1)
db.session.add(m2)
db.session.add(m3)

# commit changes
db.session.commit()
db.session.close()