from mss.Meeting.MeetingController import MeetingController
from flask import json, url_for, redirect,  jsonify,  session
from flask_login import  login_required
from datetime import datetime 

from mss import app, db

meeting_controller = MeetingController()

# Request room data form client side
@app.route('/getmeetingdata/<id>', methods=['GET'])
@login_required
def getMeetingData(id):
    dictionary = meeting_controller.getMeetingData(id)
    return jsonify(dictionary)

# Request room cost from client side 
@app.route('/getroomcost/<id>', methods=['GET'])
@login_required
def getRoomCost(id):
    cost = meeting_controller.getRoomCostData(id)
    return jsonify(cost)

# Store meeting id in cookie for edit meeting rendering
@app.route('/dashboard/editmeeting/<id>', methods=['GET'])
@login_required
def editmeetingredirect(id):
    session['messages'] = id  
    return redirect(url_for('editmeeting'))
