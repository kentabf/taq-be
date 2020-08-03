from fastapi import Response
from sqlalchemy.orm import Session

import crud
import models
import schemas

def create_room_error(room_create_form: schemas.RoomCreateForm):
	if len(room_create_form.room_name) > models.ROOM_NAME_MAX_LENGTH or \
		len(room_create_form.user_name) > models.USER_NAME_MAX_LENGTH:
		return "Room name and user name can be maximum " + \
			"%s and %s characters, respectively" % (models.ROOM_NAME_MAX_LENGTH, models.USER_NAME_MAX_LENGTH)
	else:
		return None

def join_room_error(room_join_form: schemas.RoomJoinForm):
	if len(room_join_form.user_name) > models.USER_NAME_MAX_LENGTH:
		return "Room name can be maximum " + \
			"%s characters" % (models.USER_NAME_MAX_LENGTH)
	else:
		return None

def code_matches_room(code: str, room: models.Room):
	if room and (code == room.ta_code):
		return models.UserTypeEnum.ta
	elif room and (code == room.st_code):
		return models.UserTypeEnum.st
	else:
		return None

def enqueue_error(taq_user_enqueue_form: schemas.TaqUserEnqueueForm, taq_user: models.TaqUser):
	if len(taq_user_enqueue_form.queue_topic) > models.TOPIC_MAX_LENGTH:
		return "Queue topic can be maximum %s characters" % (models.TOPIC_MAX_LENGTH)
	elif not taq_user:
		return "Invalid session cookie ID"
	elif taq_user.datetime_queued:
		return "You are already in queue"
	elif taq_user.user_type != models.UserTypeEnum.st:
		return "Only students can join or leave the queue"
	else:
		return None

def dequeue_error(taq_user: models.TaqUser):
	if not taq_user:
		return "Invalid session cookie ID"
	elif not taq_user.datetime_queued:
		return "You are not in queue to begin with"
	elif taq_user.user_type != models.UserTypeEnum.st:
		return "Only students can join or leave the queue"
	else:
		return None

def attend_error(ta_taq_user: models.TaqUser, st_taq_user: models.TaqUser):
	if not ta_taq_user:
		return "Invalid session cookie ID"
	elif not st_taq_user:
		return "You tried to attend to an invalid user"
	elif ta_taq_user.user_type != models.UserTypeEnum.ta:
		return "Only TAs can can only perform this action"
	elif st_taq_user.user_type != models.UserTypeEnum.st:
		return "You can only attend to students"
	elif ta_taq_user.room_id != st_taq_user.room_id:
		return "You cannot attend to a user in a different room"
	elif ta_taq_user.attending_with:
		return "You are already currently attending to another user"
	elif st_taq_user.attending_with:
		return "The user is already being attended by someone else"
	else:
		return None

def complete_error(taq_user: models.TaqUser):
	if not taq_user:
		return "Invalid session cookie ID"
	elif not taq_user.attending_with:
		return "Cannot complete because you aren't attending with anyone"
	else:
		return None

def format_queue_row(row, idx):
	taq_user = row[0]
	attending_taq_user = row[1]
	return {
		"queueNum": idx,
		"userId": taq_user.user_id,
		"userName": taq_user.user_name,
		"datetimeQueued": str(taq_user.datetime_queued),
		"queueTopic": taq_user.queue_topic,
		"attendingWithId": taq_user.attending_with,
		"attendingWithName": None if not attending_taq_user else attending_taq_user.user_name
	}

def get_queue_response_data(response: Response, taq_user: models.TaqUser, db_session: Session):
	raw_queue_rows = crud.get_queue_from_room_id(db_session, taq_user.room_id)
	data = [
		format_queue_row(raw_queue_row, idx+1) for idx, raw_queue_row in enumerate(raw_queue_rows)
	]
	return { "queue": data }

def get_room_info_response_data(response: Response, taq_user: models.TaqUser, db_session: Session):
	room = crud.get_room_from_room_id(db_session, taq_user.room_id)
	data = {
		"roomName": room.room_name,
		"roomId": room.room_id,
	}
	if taq_user.user_type == models.UserTypeEnum.ta:
		data["taCode"] = room.ta_code
		data["stCode"] = room.st_code
	return { "roomInfo": data }

def get_user_info_response_data(response: Response, taq_user: models.TaqUser, db_session: Session):
	taq_user_attending_with = crud.get_taq_user_from_user_id(db_session, taq_user.attending_with)
	data = {
		"isTa": taq_user.user_type == models.UserTypeEnum.ta,
		"userId": taq_user.user_id,
		"userName": taq_user.user_name,
		"attendingWithId": taq_user.attending_with,
		"attendingWithName": None if not taq_user_attending_with else taq_user_attending_with.user_name,
		"datetimeQueued": taq_user.datetime_queued,
	}
	return { "userInfo": data }

def row_to_dict(row):
	d = {}
	for column in row.__table__.columns:
		d[column.name] = str(getattr(row, column.name))
	return d
