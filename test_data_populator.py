from database import db_engine, base, Session
from models import UserTypeEnum, Room, TaqUser
from test_data_example import EXAMPLE_ROOM_NAME, EXAMPLE_ROOM_ID,\
	EXAMPLE_TA_CODE, EXAMPLE_ST_CODE, STUDENT_OBJS, STUDENT_OBJS, TA_OBJS
from crud import attend_for_testing
import pdb
import random
import datetime

# tear down and restart
base.metadata.drop_all(db_engine)
base.metadata.create_all(db_engine)

base.metadata.create_all(db_engine)
db_session = Session()

# an additional, easier-to-use manual example
example_room = Room(
	room_id=EXAMPLE_ROOM_ID, 
	room_name=EXAMPLE_ROOM_NAME,
	ta_code=EXAMPLE_TA_CODE,
	st_code=EXAMPLE_ST_CODE
)

db_session.add(example_room)
db_session.commit()
students, tas = [], []
for student_obj in STUDENT_OBJS:
	taq_user = TaqUser(**student_obj)
	students.append(taq_user)
	db_session.add(taq_user)
for ta_obj in TA_OBJS:
	taq_user = TaqUser(**ta_obj)
	tas.append(taq_user)
	db_session.add(taq_user)
db_session.commit()
attend_for_testing(db_session, students[0], tas[0])
attend_for_testing(db_session, students[1], tas[1])
attend_for_testing(db_session, students[4], tas[2])



# the three params betlow must be between 1 and 99 (inclusive)
TEST_SETS = 1
TA_USERS = 2
ST_USERS = 18

assert 0 < TEST_SETS and TEST_SETS < 100
assert 0 < TA_USERS and TA_USERS < 100
assert 0 < ST_USERS and ST_USERS < 100


# some helper functions
def num_to_str(num):
	# assume 0 <= num <= 99
	res = '0' + str(num) if num < 10 else str(num)
	return res
def rand_gen(idx):
	if idx == 1:
		return True
	else:
		return bool(random.getrandbits(1))
def create_user(user_type_enum, room_num, agg_num, idx):
	user_type = user_type_enum._value_

	datetime_queued, queue_topic = None, None

	if user_type_enum == UserTypeEnum.st and rand_gen(idx):
		curr = datetime.datetime.utcnow()
		diff = datetime.timedelta(minutes=(-5*idx))
		datetime_queued = curr + diff
		queue_topic = "Queue topic for %s" % room_num

	return TaqUser(
		user_id = '%s_id_%s' % (user_type, agg_num),
		user_name = '%s user %s Name' % (user_type, agg_num),
		user_type = user_type_enum,
		room_id = 'room_%s_id' % room_num,
		taq_session_id = '%s_%s_session' % (user_type, agg_num),
		datetime_queued = datetime_queued,
		queue_topic = queue_topic
	)


# create the rows
rooms = []
users = []

for i in range(1, TEST_SETS+1):
	room_num = num_to_str(i)
	rooms.append(Room(
		room_id = 'room_%s_id' % room_num,
		room_name = 'Room %s Name' % room_num,
		ta_code = 'ta_code_%s' % room_num,
		st_code = 'st_code_%s' % room_num
	))
	for j in range(1, TA_USERS+1):
		agg_num = room_num + num_to_str(j)
		users.append(create_user(UserTypeEnum.ta, room_num, agg_num, j))
	for k in range(1, ST_USERS+1):
		agg_num = room_num + num_to_str(k)
		users.append(create_user(UserTypeEnum.st, room_num, agg_num, k))


# add the rows and commit
for room in rooms:
	db_session.add(room)
db_session.commit()
for user in users:
	db_session.add(user)
db_session.commit()

# close the session
db_session.close()

