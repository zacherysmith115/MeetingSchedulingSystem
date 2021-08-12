from mss.Meeting.MeetingController import MeetingController
from flask import url_for, redirect,  jsonify,  session
from flask_login import  login_required

from mss import app

meeting_controller = MeetingController()

# Request room data form client side
@app.route('/getmeetingdata/<id>', methods=['GET'])
@login_required
def getMeetingData(id: "str"):
    dictionary = meeting_controller.getMeetingData(id)
    return jsonify(dictionary)

# Request room cost from client side 
@app.route('/getroomcost/<id>', methods=['GET'])
@login_required
def getRoomCost(id: "str"):
    cost = meeting_controller.getRoomCostData(id)
    return jsonify(cost)

# Store meeting id in cookie for edit meeting rendering
@app.route('/dashboard/editmeeting/<id>', methods=['GET'])
@login_required
def editMeetingredirect(id: "str"):
    session['messages'] = id  
    return redirect(url_for('editmeeting'))
