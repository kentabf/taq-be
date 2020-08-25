from fastapi import Form
from pydantic import BaseModel

from database import models

class RoomCreateForm(BaseModel):
	room_name: str
	user_name: str

	def __init__(
		self, 
		roomName: str = Form(...), 
		userName: str = Form(...)
	):
		super().__init__(room_name=roomName, user_name=userName)

class RoomJoinForm(BaseModel):
	room_id: str
	code: str
	user_name: str

	def __init__(
		self, 
		roomId: str = Form(...), 
		code: str = Form(...), 
		userName: str = Form(...)
	):
		super().__init__(room_id=roomId, code=code, user_name=userName)

class RoomCreate(BaseModel):
	room_name: str

class TaqUserCreate(BaseModel):
	user_name: str
	user_type: models.UserTypeEnum
	room_id: str

class TaqUserEnqueueForm(BaseModel):
	queue_topic: str

	def __init__(
		self, 
		queueTopic: str = Form(...)
	):
		super().__init__(queue_topic=queueTopic)

class TaqUserEnqueue(BaseModel):
	queue_topic: str
	taq_user: models.TaqUser

	class Config:
		arbitrary_types_allowed = True

class AttendForm(BaseModel):
	user_id: str

	def __init__(
		self, 
		userId: str = Form(...)
	):
		super().__init__(user_id=userId)

class Attend(BaseModel):
	ta_taq_user: models.TaqUser
	st_taq_user: models.TaqUser

	class Config:
		arbitrary_types_allowed = True

class Complete(BaseModel):
	taq_user: models.TaqUser
	other_taq_user: models.TaqUser
	
	class Config:
		arbitrary_types_allowed = True

