from flask import url_for, redirect,  jsonify,  session
from flask_login import  login_required
from datetime import datetime 

from mss import app, db
from mss.Meeting.MeetingModels import Meeting, Room


@app.route('/getmeetingdata/<index_no>', methods=['GET'])
@login_required
def getMeetingData(index_no):
    # find the selected meeting
    meeting = Meeting.query.filter_by(id=index_no).first()

    # Formatting time to H:M pm/am
    start_formatted = datetime.strptime(f'{meeting.start_time.hour:02d}:{meeting.start_time.minute:02d}',
                                        '%H:%M').strftime('%I:%M %p')
    end_formatted = datetime.strptime(f'{meeting.end_time.hour:02d}:{meeting.end_time.minute:02d}', '%H:%M').strftime(
        '%I:%M %p')

    # Create json "like" object
    meeting_json = {'title': meeting.title,
                    'start': start_formatted,
                    'end': end_formatted,
                    'description': meeting.description}

    return jsonify(meeting_json)


@app.route('/getroomcost/<room_no>', methods=['GET'])
@login_required
def getRoomCost(room_no):
    room = Room.query.filter_by(id=room_no).first()

    if room.special:
        cost = {'cost': '$' + str(room.cost)}
    else:
        cost = {'cost': '-'}

    return jsonify(cost)


@app.route('/dashboard/editmeeting/<id>', methods=['GET'])
@login_required
def editmeetingredirect(id):
    session['messages'] = id  
    return redirect(url_for('editmeeting'))
