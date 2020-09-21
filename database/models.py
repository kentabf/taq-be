import enum
import string
from sqlalchemy import Column, CheckConstraint, ForeignKeyConstraint, String, Integer, Enum, types

from . import database

# exact length of IDs and code
ROOM_ID_LENGTH = 10
USER_ID_LENGTH = 10
CODE_LENGTH=10
TAQ_SESSION_ID_LENGTH = 15

# max length
ROOM_NAME_MAX_LENGTH = 30
USER_NAME_MAX_LENGTH = 30
TOPIC_MAX_LENGTH=70

# for simplicity, all id and code will be composed of alphanumeric characters and underscore
ALPHA_NUM_US_REGEX = """[a-zA-Z0-9_]"""
ALPHA_NUM_US_STRING = string.ascii_letters + string.digits + "_"


def room_id_domain_checkconstraint_creator(col_name):
	return CheckConstraint(
		""" %s SIMILAR TO '%s{%s}' """ % (col_name, ALPHA_NUM_US_REGEX, ROOM_ID_LENGTH),
		name = "id domain: %s" % col_name
	)
def user_id_domain_checkconstraint_creator(col_name):
	return CheckConstraint(
		""" %s SIMILAR TO '%s{%s}' """ % (col_name, ALPHA_NUM_US_REGEX, USER_ID_LENGTH),
		name = "id domain: %s" % col_name
	)

def code_domain_checkconstraint_creator(col_name):
	return CheckConstraint(
		""" %s SIMILAR TO '%s{%s}' """ % (col_name, ALPHA_NUM_US_REGEX, CODE_LENGTH),
		name = "code domain: %s" % col_name
	)

def taq_session_id_domain_checkconstraint_creator(col_name):
	return CheckConstraint(
		""" %s SIMILAR TO '%s{%s}' """ % (col_name, ALPHA_NUM_US_REGEX, TAQ_SESSION_ID_LENGTH),
		name = "id domain: %s" % col_name
	)

# Enum data definition for user_type
class UserTypeEnum(str, enum.Enum):
	st = "st" # Students
	ta = "ta" # Teaching assistants

class Room(database.base):
	__tablename__ = "room"

	room_id = Column(types.String(length=ROOM_ID_LENGTH), primary_key=True) 
	room_name = Column(types.String(length=ROOM_NAME_MAX_LENGTH), nullable=False)
	ta_code = Column(types.String(length=CODE_LENGTH), nullable=False)
	st_code = Column(types.String(length=CODE_LENGTH), nullable=False)

	# table level constraints
	__table_args__ = (
		room_id_domain_checkconstraint_creator("room_id"),
		CheckConstraint("""ta_code <> st_code""", name="ta_code and st_code must be different"),
		code_domain_checkconstraint_creator("ta_code"),
		code_domain_checkconstraint_creator("st_code"),
	)

class TaqUser(database.base):
	__tablename__ = "taq_user"

	user_id = Column(types.String(length=USER_ID_LENGTH), primary_key=True)
	user_name = Column(types.String(length=USER_NAME_MAX_LENGTH), nullable=False)
	user_type = Column(Enum(UserTypeEnum), nullable=False)
	room_id = Column(types.String(length=ROOM_ID_LENGTH), nullable=False)
	taq_session_id = Column(types.String(length=TAQ_SESSION_ID_LENGTH), unique=True, nullable=False)

	attending_with = Column(types.String(length=USER_ID_LENGTH), unique=True) # Note: unique but nullable
	datetime_attended = Column(types.DateTime()) # UTC time
	datetime_queued = Column(types.DateTime()) # UTC time
	queue_topic = Column(types.String(length=TOPIC_MAX_LENGTH))

	# table level constraints
	__table_args__ = (
		user_id_domain_checkconstraint_creator("user_id"),
		ForeignKeyConstraint(["room_id"], ["room.room_id"]),
		taq_session_id_domain_checkconstraint_creator("taq_session_id"),

		ForeignKeyConstraint(["attending_with"], ["taq_user.user_id"]),

		# user_type is TA -> datetime_queued is null. Use logical equivalence: P->Q <=> ~P V Q
		CheckConstraint(""" (user_type <> '%s') OR (datetime_queued IS NULL) """ % UserTypeEnum.ta._value_, "ta can't be queued"),
	)



