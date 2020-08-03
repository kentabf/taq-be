import uvicorn
from typing import Optional
from fastapi import FastAPI, Response, status, Cookie, Form, Request, Body, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pdb # debugging

import database
import crud
import schemas
import models
import api_utils

app = FastAPI()

origins = [
	"http://localhost:8080"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

database.base.metadata.create_all(database.db_engine)

def get_db_session():
	try:
		db_session = database.Session()
		yield db_session
	finally:
		db_session.close()


#####################
## <API ENDPOINTS> ##
#####################

def return_cookie_setter(db_session: Session, response: Response, taq_user: models.TaqUser):
	response.set_cookie(key="taq_session_id", value=taq_user.taq_session_id, httponly=True)
	return "Success"

# @app.post("/api/create_room")
# def tester(response: Response, room_create_form: schemas.RoomCreateForm = Depends(), db_session: Session = Depends(get_db_session)):
# 	# pdb.set_trace()
# 	x=1
# 	y=2
# 	return x + y


@app.post("/api/create_room")
def api_create_room(response: Response, room_create_form: schemas.RoomCreateForm = Depends(), db_session: Session = Depends(get_db_session)):
	print("does this print?")
	error = api_utils.create_room_error(room_create_form) # form validation

	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	new_room = crud.create_room(db_session, room_create=schemas.RoomCreate(**room_create_form.dict()))
	new_taq_user = crud.create_taq_user(db_session, 
		taq_user_create=schemas.TaqUserCreate(
			user_type=models.UserTypeEnum.ta, 
			room_id=new_room.room_id, 
			**room_create_form.dict()
		)
	)
	response.status_code = status.HTTP_201_CREATED
	return return_cookie_setter(db_session, response, new_taq_user)

@app.post("/api/join_room")
def api_join_room(response: Response, room_join_form: schemas.RoomJoinForm = Depends(), db_session: Session = Depends(get_db_session)):
	error = api_utils.join_room_error(room_join_form) # form validation

	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	room = crud.get_room_from_room_id(db_session, room_join_form.room_id)
	user_type = api_utils.code_matches_room(room_join_form.code, room)

	if room and user_type:
		new_taq_user = crud.create_taq_user(db_session, taq_user_create=schemas.TaqUserCreate(user_type=user_type,**room_join_form.dict()))
		response.status_code = status.HTTP_201_CREATED
		return return_cookie_setter(db_session, response, new_taq_user)
	

	response.status_code = status.HTTP_401_UNAUTHORIZED
	return "incorrect room ID and/or code"

@app.post("/api/enqueue")
def api_enqueue_user(response: Response, taq_user_enqueue_form: schemas.TaqUserEnqueueForm = Depends(), taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	error = api_utils.enqueue_error(taq_user_enqueue_form, taq_user) # form & user validation

	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	
	enqueued_taq_user = crud.enqueue_taq_user(db_session, taq_user_enqueue=schemas.TaqUserEnqueue(taq_user=taq_user, **taq_user_enqueue_form.dict()))
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, enqueued_taq_user)

@app.post("/api/dequeue")
def api_dequeue_user(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	error = api_utils.dequeue_error(taq_user)

	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	dequeued_taq_user = crud.dequeue_taq_user(db_session, taq_user)
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, dequeued_taq_user)

@app.post("/api/attend")
def api_attend_user(response: Response, attend_form: schemas.AttendForm = Depends(), taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	ta_taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	st_taq_user = crud.get_taq_user_from_user_id(db_session, attend_form.user_id)
	error = api_utils.attend_error(ta_taq_user, st_taq_user)

	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	attended_ta_taq_user = crud.attend(db_session, attend=schemas.Attend(ta_taq_user=ta_taq_user, st_taq_user=st_taq_user))
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, attended_ta_taq_user)

@app.post("/api/complete")
def api_complete_user(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	error = api_utils.complete_error(taq_user)

	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	other_taq_user = crud.get_taq_user_from_user_id(db_session, taq_user.attending_with)
	completed_taq_user = crud.complete(db_session, complete=schemas.Complete(taq_user=taq_user, other_taq_user=other_taq_user))
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, completed_taq_user)

@app.post("/api/room")
def get_room(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	if taq_user:
		response_data = {
			**api_utils.get_queue_response_data(db_session, taq_user, db_session),
			**api_utils.get_room_info_response_data(db_session, taq_user, db_session),
			**api_utils.get_user_info_response_data(db_session, taq_user, db_session)
		}
		response.status_code = status.HTTP_200_OK
		return response_data
	else:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Invalid session cookie ID"

@app.post("/api/leave")
def leave_room(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	if taq_user:
		if not api_utils.complete_error(taq_user):
			other_taq_user = crud.get_taq_user_from_user_id(db_session, taq_user.attending_with)
			taq_user = crud.complete(db_session, complete=schemas.Complete(taq_user=taq_user, other_taq_user=other_taq_user))
		if not api_utils.dequeue_error(taq_user):
			taq_user = crud.dequeue_taq_user(db_session, taq_user)
		crud.delete_taq_user(db_session, taq_user)
		response.status_code = status.HTTP_200_OK
		return "User successfully left the room"
	else:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return "You don't belong to a room to begin with"

#######################
## </ API ENDPOINTS> ##
#######################

if __name__ == '__main__':
	uvicorn.run(app, port=8000, host='localhost')

