import datetime
from database.models import UserTypeEnum, Room, TaqUser

'''
#############################################################
NOTE:
This will break if the code and id properties (length, regex)
are changed in the models
#############################################################
'''

EXAMPLE_ROOM_NAME = 'CS 000 Example Office Hours'
EXAMPLE_ROOM_ID = 'eg_room_id'
EXAMPLE_TA_CODE = 'eg_ta_code'
EXAMPLE_ST_CODE = 'eg_st_code'


STUDENT_OBJS = [
	{
		"user_id": "st_user_01",
		"user_name": "Reon Richards",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_001",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*1)),
		"queue_topic": "Lorem ipsum dolor sit amet",
	},
	{
		"user_id": "st_user_02",
		"user_name": "Arnie Harrell",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_002",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*2)),
		"queue_topic": "consectetur adipiscing elit",
	},
	{
		"user_id": "st_user_03",
		"user_name": "Ari Greaves",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_003",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*3)),
		"queue_topic": "sed do eiusmod tempor",
	},
	{
		"user_id": "st_user_04",
		"user_name": "Ayat Delacruz",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_004",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*4)),
		"queue_topic": "incididunt ut labore et dolore magna aliqua. Ut",
	},
	{
		"user_id": "st_user_05",
		"user_name": "Marguerite Clifford",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_005",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*5)),
		"queue_topic": "minim veniam, quis nostrud exercitation",
	},
	{
		"user_id": "st_user_06",
		"user_name": "Byron Joyce",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_006",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*6)),
		"queue_topic": "ullamco laboris nisi ut aliquip ex ea commodo",
	},
	{
		"user_id": "st_user_07",
		"user_name": "Aislinn Connolly",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_007",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*7)),
		"queue_topic": "consequat. Duis aute irure dolor",
	},
	{
		"user_id": "st_user_08",
		"user_name": "Yousuf Cano",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_008",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*8)),
		"queue_topic": "in voluptate velit esse cillum",
	},
		{
		"user_id": "st_user_09",
		"user_name": "Marguerite Clifford",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_009",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*9)),
		"queue_topic": "dolore magnam aliquam quaerat",
	},
	{
		"user_id": "st_user_10",
		"user_name": "Julia Sparrow",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_010",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*10)),
		"queue_topic": "oluptatem. Ut enim ad minima ven",
	},
	{
		"user_id": "st_user_11",
		"user_name": "Samanta Lawrence",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_011",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*11)),
		"queue_topic": " quis nostrum exercitationem ullam",
	},
	{
		"user_id": "st_user_12",
		"user_name": "Lloyd Shepard",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_012",
		"attending_with": None,
		"datetime_attended": None,
		"datetime_queued": datetime.datetime.utcnow() + datetime.timedelta(minutes=(-3*12)),
		"queue_topic": "laboriosam, nisi ut aliquid ex",
	},
]

STUDENT_OBJS = list(reversed(STUDENT_OBJS))

TA_OBJS = [
	{
		"user_id": "ta_user_01",
		"user_name": "Ashanti Workman",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_t01",
		"attending_with": None,
		"datetime_attended": datetime.datetime.utcnow(),
		"datetime_queued": None,
		"queue_topic": None,
	},
	{
		"user_id": "ta_user_02",
		"user_name": "Shreya Contreras",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_t02",
		"attending_with": None,
		"datetime_attended": datetime.datetime.utcnow(),
		"datetime_queued": None,
		"queue_topic": None,
	},
	{
		"user_id": "ta_user_03",
		"user_name": "Norman Almond",
		"user_type": UserTypeEnum.st,
		"room_id": EXAMPLE_ROOM_ID,
		"taq_session_id": "taq_session_t03",
		"attending_with": None,
		"datetime_attended": datetime.datetime.utcnow(),
		"datetime_queued": None,
		"queue_topic": None,
	},
]

TA_OBJS = list(reversed(TA_OBJS))