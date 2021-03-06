import uvicorn
from typing import Optional
from fastapi import FastAPI, Response, status, Cookie, Form, Request, Body, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pdb # debugging

import config
from database import database, models, crud
from data_population import test_data_populator
import schemas
import api_utils

## cookie settings
ENV_PROD_COOKIE_SETTER_SETTINGS = {} if config.ENV_LOCAL_DEV else {
	"samesite": "none",
	"secure": True
}

cookie_length = 60*60*3 # express as seconds; currently set to 3 hours

## origins settings
origins = [
	"http://localhost:8080",
	"https://practical-shannon-d209d8.netlify.app",
]

## instantiate the app
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

## spin up the PostgreSQL database engine
database.base.metadata.create_all(database.db_engine)


## common helpers for the routes
def get_db_session():
	try:
		db_session = database.Session()
		yield db_session
	finally:
		db_session.close()


def return_cookie_setter(db_session: Session, response: Response, taq_user: models.TaqUser):
	'''
	Given a TaqUser object, message "Success" with a Set-Cookie for user's cookie, as per cookie settings
	Note: assumes relevant HTTP status code is set in the response object by caller
	'''
	response.set_cookie(
		key="taq_session_id", 
		value=taq_user.taq_session_id,
		expires=cookie_length,
		max_age=cookie_length,
		**ENV_PROD_COOKIE_SETTER_SETTINGS
	)
	return "Success"

#####################
## <API ENDPOINTS> ##
#####################

@app.get("/api/test_get")
def api_test_get():
	return {"message": "test success!"}

@app.get("/api/test_get_with_db")
def api_test_get(db_session: Session = Depends(get_db_session)):
	return {"message": "test with db success!"}

@app.post("/api/create_room")
def api_create_room(response: Response, room_create_form: schemas.RoomCreateForm = Depends(), db_session: Session = Depends(get_db_session)):
	
	# form validation; if error, return code 400
	error = api_utils.create_room_error(room_create_form)
	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	# if form validated, create new room and return code 201
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
	
	# form validation
	error = api_utils.join_room_error(room_join_form)
	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	# get the room by room_id, and check whether correct code given
	room = crud.get_room_from_room_id(db_session, room_join_form.room_id)
	user_type = api_utils.code_matches_room(room_join_form.code, room)
	if room and user_type:
		new_taq_user = crud.create_taq_user(db_session, taq_user_create=schemas.TaqUserCreate(user_type=user_type,**room_join_form.dict()))
		response.status_code = status.HTTP_201_CREATED
		return return_cookie_setter(db_session, response, new_taq_user)
	
	# status 401 if code does not match room_id
	response.status_code = status.HTTP_401_UNAUTHORIZED
	return "incorrect room ID and/or code"

@app.post("/api/enqueue")
def api_enqueue_user(response: Response, taq_user_enqueue_form: schemas.TaqUserEnqueueForm = Depends(), taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	
	# user & form validation
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	error = api_utils.enqueue_error(taq_user_enqueue_form, taq_user)
	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	enqueued_taq_user = crud.enqueue_taq_user(db_session, taq_user_enqueue=schemas.TaqUserEnqueue(taq_user=taq_user, **taq_user_enqueue_form.dict()))
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, enqueued_taq_user)

@app.post("/api/dequeue")
def api_dequeue_user(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	
	# user & request validation
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
	
	# user & form validation
	ta_taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	st_taq_user = crud.get_taq_user_from_user_id(db_session, attend_form.user_id)
	error = api_utils.attend_error(ta_taq_user, st_taq_user)
	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	attended_ta_taq_user = crud.attend(db_session, attend=schemas.Attend(ta_taq_user=ta_taq_user, st_taq_user=st_taq_user))
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, attended_ta_taq_user)

@app.post("/api/complete_keep")
def api_complete_keep_user(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	
	# user & request validation
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	error = api_utils.complete_error(taq_user)
	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	other_taq_user = crud.get_taq_user_from_user_id(db_session, taq_user.attending_with)
	completed_taq_user = crud.complete(db_session, complete=schemas.Complete(taq_user=taq_user, other_taq_user=other_taq_user))
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, completed_taq_user)

@app.post("/api/complete_remove")
def api_complete_remove_user(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	
	# user & request validation
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	error = api_utils.complete_error(taq_user)
	if error:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return error

	other_taq_user = crud.get_taq_user_from_user_id(db_session, taq_user.attending_with)
	completed_taq_user = crud.complete(db_session, complete=schemas.Complete(taq_user=taq_user, other_taq_user=other_taq_user))
	crud.dequeue_taq_user(db_session, other_taq_user)
	response.status_code = status.HTTP_200_OK
	return return_cookie_setter(db_session, response, completed_taq_user)

@app.post("/api/room")
def api_get_room(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	
	# user validation
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	if not taq_user:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Invalid session cookie ID"
	
	response_data = {
		**api_utils.get_queue_response_data(db_session, taq_user, db_session),
		**api_utils.get_room_info_response_data(db_session, taq_user, db_session),
		**api_utils.get_user_info_response_data(db_session, taq_user, db_session)
	}
	response.status_code = status.HTTP_200_OK
	return response_data

@app.post("/api/leave")
def api_leave_room(response: Response, taq_session_id: Optional[str] = Cookie(None), db_session: Session = Depends(get_db_session)):
	
	# user validation
	taq_user = crud.get_taq_user_from_taq_session_id(db_session, taq_session_id)
	if not taq_user:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return "You don't belong to a room to begin with"

	if not api_utils.complete_error(taq_user):
		# if the user is currently attending to someone, or being attended to, remove that association
		other_taq_user = crud.get_taq_user_from_user_id(db_session, taq_user.attending_with)
		taq_user = crud.complete(db_session, complete=schemas.Complete(taq_user=taq_user, other_taq_user=other_taq_user))
	if not api_utils.dequeue_error(taq_user):
		# if the user is currently in queue, remove from queue
		taq_user = crud.dequeue_taq_user(db_session, taq_user)
	crud.delete_taq_user(db_session, taq_user)
	response.status_code = status.HTTP_200_OK
	return "You successfully left the room"


@app.post("/api/refresh_with_test_tables")
def api_refresh_with_test_tables(response: Response):
	'''
	A cheap and dirty method to reset the database:
	1) Remove all existing data
	2) Populate the example/test database
	'''

	try:
		test_data_populator.populate()
		return "populated test data successfully"
	except Exception as e:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return f"FAILED. {str(e)}"


#######################
## </ API ENDPOINTS> ##
#######################

if __name__ == '__main__' and config.ENV_LOCAL_DEV:
	uvicorn.run(app, port=8000, host='localhost')

