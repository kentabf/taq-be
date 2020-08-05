# CRUD methods for checking, creating, and deleting sessions

from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import exists
from sqlalchemy.sql.expression import or_, and_
from datetime import datetime
import pdb # debugging

import models
import schemas
import data_generator

def create_room(db_session: Session, room_create: schemas.RoomCreate):
	new_room_id = data_generator.generate_new_room_id(db_session)
	new_ta_code, new_st_code = data_generator.generate_codes()
	new_room = models.Room(
		room_id = new_room_id,
		ta_code = new_ta_code,
		st_code = new_st_code,
		**room_create.dict()
	)
	db_session.add(new_room)
	db_session.commit()
	return new_room

def create_taq_user(db_session: Session, taq_user_create: schemas.TaqUserCreate):
	new_taq_session_id = data_generator.generate_new_taq_session_id(db_session)
	new_user_id = data_generator.generate_new_user_id(db_session)
	new_taq_user = models.TaqUser(
		taq_session_id = new_taq_session_id,
		user_id = new_user_id, 
		**taq_user_create.dict()
	)
	db_session.add(new_taq_user)
	db_session.commit()
	return new_taq_user	

def get_room_from_room_id(db_session: Session, room_id: str):
	return db_session.query(models.Room).filter(models.Room.room_id == room_id).first()

def get_taq_user_from_taq_session_id(db_session: Session, taq_session_id: str):
	return db_session.query(models.TaqUser).filter(models.TaqUser.taq_session_id == taq_session_id).first()

def get_taq_user_from_user_id(db_session: Session, user_id: str):
	return db_session.query(models.TaqUser).filter(models.TaqUser.user_id == user_id).first()

def enqueue_taq_user(db_session: Session, taq_user_enqueue: schemas.TaqUserEnqueue):
	taq_user = taq_user_enqueue.taq_user
	taq_user.datetime_queued = datetime.utcnow()
	taq_user.queue_topic = taq_user_enqueue.queue_topic
	db_session.commit()
	return taq_user

def dequeue_taq_user(db_session: Session, taq_user: models.TaqUser):
	taq_user.datetime_queued = None
	taq_user.queue_topic = None
	db_session.commit()
	return taq_user

def attend(db_session: Session, attend: schemas.Attend):
	ta_taq_user = attend.ta_taq_user
	st_taq_user = attend.st_taq_user
	curr_datetime = datetime.utcnow()
	ta_taq_user.attending_with = st_taq_user.user_id
	st_taq_user.attending_with = ta_taq_user.user_id
	ta_taq_user.datetime_attended = curr_datetime
	st_taq_user.datetime_attended = curr_datetime
	db_session.commit()
	return ta_taq_user

def complete(db_session: Session, complete: schemas.Complete):
	taq_user = complete.taq_user
	other_taq_user = complete.other_taq_user
	taq_user.attending_with = None
	other_taq_user.attending_with = None
	taq_user.datetime_attended = None
	other_taq_user.datetime_attended = None
	db_session.commit()
	return taq_user

def get_queue_from_room_id(db_session: Session, room_id: str):
	TaqUserAliasAttendedBy = aliased(models.TaqUser)

	return db_session.query(models.TaqUser,TaqUserAliasAttendedBy).\
		filter(models.TaqUser.room_id == room_id, models.TaqUser.datetime_queued != None).\
		outerjoin(TaqUserAliasAttendedBy, models.TaqUser.attending_with == TaqUserAliasAttendedBy.user_id).\
		order_by(models.TaqUser.datetime_queued).\
		all()

def delete_taq_user(db_session: Session, taq_user: models.TaqUser):
	db_session.delete(taq_user)
	db_session.commit()
	return None

def check_room_id_exists(db_session: Session, room_id: str):
	return db_session.query(exists().where(models.Room.room_id == room_id)).scalar()

def check_user_id_exists(db_session: Session, user_id: str):
	return db_session.query(exists().where(models.TaqUser.user_id == user_id)).scalar()

def check_taq_session_id_exists(db_session: Session, taq_session_id: str):
	return db_session.query(exists().where(models.TaqUser.taq_session_id == taq_session_id)).scalar()

def attend_for_testing(db_session: Session, ta_taq_user: models.TaqUser, st_taq_user: models.TaqUser):
	curr_datetime = datetime.utcnow()
	ta_taq_user.attending_with = st_taq_user.user_id
	st_taq_user.attending_with = ta_taq_user.user_id
	ta_taq_user.datetime_attended = curr_datetime
	st_taq_user.datetime_attended = curr_datetime
	db_session.commit()



