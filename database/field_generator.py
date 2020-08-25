from sqlalchemy.orm import Session
import random

from . import crud, models

def randcom_char_from_str(possible_chars: str):
	return random.choice(possible_chars)

def random_n_chars_from_str(n: int, possible_chars: str):
	return ''.join([randcom_char_from_str(possible_chars) for i in range(n)])

def generate_new_data(db_session: Session, n: int, possible_chars: str, check_function):
	data = random_n_chars_from_str(n, possible_chars)
	while (check_function(db_session, data)):
		data = random_n_chars_from_str(n, possible_chars)
	return data

def generate_new_room_id(db_session: Session):
	return generate_new_data(
		db_session, 
		models.ROOM_ID_LENGTH, 
		models.ALPHA_NUM_US_STRING,
		crud.check_room_id_exists
	)

def generate_new_user_id(db_session: Session):
	return generate_new_data(
		db_session, 
		models.USER_ID_LENGTH, 
		models.ALPHA_NUM_US_STRING,
		crud.check_user_id_exists
	)

def generate_new_taq_session_id(db_session: Session):
	return generate_new_data(
		db_session, 
		models.TAQ_SESSION_ID_LENGTH, 
		models.ALPHA_NUM_US_STRING,
		crud.check_taq_session_id_exists
	)

def generate_codes():
	code1 = random_n_chars_from_str(models.CODE_LENGTH, models.ALPHA_NUM_US_STRING)
	code2 = random_n_chars_from_str(models.CODE_LENGTH, models.ALPHA_NUM_US_STRING)
	while (code1 == code2):
		code2 = random_n_chars_from_str(models.CODE_LENGTH, models.ALPHA_NUM_US_STRING)
	return (code1, code2)

