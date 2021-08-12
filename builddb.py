import datetime
from mss import db
from mss.User.UserModels import *
from mss.Meeting.MeetingModels import *
from mss.Utility.UtilityModels import *
from mss.Ticket.TicketModels import *

from mss.User.UserController import UserController

user_controller = UserController()

# reset db
db.drop_all()
db.create_all()

# populate admin data
zach = Admin(first_name='Zachery', last_name='Smith', email='zachery.smith@pss.com', 
                password= user_controller.encryptPassword('password'))
sandy = Admin(first_name='Sandy', last_name='Lee', email='sandy.lee@pss.com', 
                password= user_controller.encryptPassword('password'))
hope = Admin(first_name='Hope', last_name='Fisher', email='hope.fisher@pss.com',
                password= user_controller.encryptPassword('password'))

db.session.add(zach)
db.session.add(sandy)
db.session.add(hope)

# populate client data
john = Client(first_name='John', last_name='Doe', email='john.doe@pss.com',
                password= user_controller.encryptPassword('password'))
sarah = Client(first_name='Sarah', last_name='Brown', email='sarah.brown@pss.com', 
                password= user_controller.encryptPassword('password'))
james = Client(first_name='James', last_name='Cook', email='james.cook@pss.com',
                password= user_controller.encryptPassword('password'))
kelly = Client(first_name='Kelly', last_name='Chen', email='kelly.chen@pss.com',
                password= user_controller.encryptPassword('password'))
db.session.add(john)
db.session.add(sarah)
db.session.add(james)
db.session.add(kelly)

# populate payment info
johns_card = Card(client_id=john.id, client=john, number='6988019516364371', name='John Doe',
                  exp_date=datetime.date(year=2022, month=9, day=1), ccv='797')
sarahs_card = Card(client_id=sarah.id, client=sarah, number='5456141426522113', name='Sarah Brown',
                   exp_date=datetime.date(year=2023, month=7, day=1), ccv='535')
james_card = Card(client_id=james.id, client=james, number='2302857125016344', name='James Cook',
                  exp_date=datetime.date(year=2021, month=12, day=1), ccv='459')
kellys_card = Card(client_id=james.id, client=james, number='5215353134814512', name='James Cook',
                   exp_date=datetime.date(year=2021, month=12, day=1), ccv='467')
db.session.add(johns_card)
db.session.add(sarahs_card)
db.session.add(james_card)
db.session.add(kellys_card)

# populate rooms
room_101 = Room(id=101)
room_102 = Room(id=102)
room_103 = Room(id=103)
room_200 = Room(id=200, special=True, cost = 100)
db.session.add(room_101)
db.session.add(room_102)
db.session.add(room_103)
db.session.add(room_200)

# populate meetings: all meetings will be based on week 8/9 - 8/13
m1_start_time = datetime.datetime(year=2021, month=8, day=9, hour=8)
m1_end_time = datetime.datetime(year=2021, month=8, day=9, hour=9)
m1_descr = 'To review the upcoming tasks for the week, and plan out who will be handling what.'
m1 = Meeting(creator_id=john.id, creator=john, participants=[sarah, james, kelly], title='Monday morning meeting',
             room_id=room_101.id, room=room_101, start_time=m1_start_time, end_time=m1_end_time, description = m1_descr)

m2_start_time = datetime.datetime(year=2021, month=8, day=11, hour=12)
m2_end_time = datetime.datetime(year=2021, month=8, day=11, hour=13)
m2_descr = 'Recurring lunch meeting at the dining area, feel free to forward to anyone else!'
m2 = Meeting(creator_id=sarah.id, creator=sarah, participants=[john, james, kelly], title='Wednesday lunch',
             room_id=room_102.id, room=room_102, start_time=m2_start_time, end_time=m2_end_time, description = m2_descr)

m3_start_time = datetime.datetime(year=2021, month=8, day=13, hour=14)
m3_end_time = datetime.datetime(year=2021, month=8, day=13, hour=15)
m3_descr = 'That last meeting of the week that everyone hates on James for making. I just want to start the weekend already'
m3 = Meeting(creator_id=james.id, creator=james, participants=[john, sarah, kelly], title='Friday afternoon meeting',
             room_id=room_103.id, room=room_103, start_time=m3_start_time, end_time=m3_end_time, description = m3_descr)

m4_start_time = datetime.datetime(year=2021, month=8, day=10, hour=9)
m4_end_time = datetime.datetime(year=2021, month=8, day=10, hour=10)
m4_descr = 'Trying to figure out whats wrong with my db relationships :['
m4 = Meeting(creator_id=james.id, creator=james, participants=[john, sarah, kelly], title='Debugging my system',
             room_id=room_103.id, room=room_103, start_time=m4_start_time, end_time=m4_end_time, description = m4_descr)



db.session.add(m1)
db.session.add(m2)
db.session.add(m3)
db.session.add(m4)

t1 = Ticket(content = "This system never freaking works! Thanks Sandy.", creator_id = john.id, creator = john)
t1.response = "Sorry it never works! We are doing our best"
t1.admin_id = sandy.id
t1.admin = sandy

t2 = Ticket(content = "This system never freaking works! Thanks Hope", creator_id = kelly.id, creator = kelly)
t2.response = "Sorry we are doing our best to fix it up"
t2.admin_id = hope.id
t2.admin = hope

t3 = Ticket(content = "This system is still broken.... Do you know how to do your job?", creator_id = james.id, creator = james)
t4 = Ticket(content = "I'm over using this app, wish we could just use Outlook like everyone else!", creator_id = sarah.id, creator = sarah)

db.session.add(t1)
db.session.add(t2)

# commit changes
db.session.commit()
db.session.close()
