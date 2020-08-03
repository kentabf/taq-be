-- create a domain of char: alphanumeric, length 8, upper/lower case
DO $$
	BEGIN
		CREATE DOMAIN alphanum_us_10 AS CHAR(10) CHECK (VALUE ~* '^[A-Z0-9_]+$');
	EXCEPTION
		WHEN OTHERS THEN
			NULL;
	END;
$$;

DO $$
	BEGIN
		CREATE TYPE usertype AS ENUM ('st', 'ta');
	EXCEPTION
		WHEN OTHERS THEN
			NULL;
	END;
$$;

DROP TABLE IF EXISTS taq_user;
DROP TABLE IF EXISTS room CASCADE;
 
-- room 
CREATE TABLE IF NOT EXISTS room (
	room_id alphanum_us_10 PRIMARY KEY,
	name VARCHAR (50) NOT NULL,
	ta_code alphanum_us_10 NOT NULL,
	student_code alphanum_us_10 NOT NULL,
	CONSTRAINT student_ta_different_codes CHECK (ta_code <> student_code)
);

-- user
CREATE TABLE IF NOT EXISTS taq_user (
	user_id alphanum_us_10 PRIMARY KEY,
	name VARCHAR (50) NOT NULL,
	user_type usertype NOT NULL,
	room_id alphanum_us_10 NOT NULL,
	-- TODO: update the datatype of session_id here
	session_id CHAR(04) UNIQUE NOT NULL,
	CONSTRAINT room_id_fkey FOREIGN KEY (room_id) 
		REFERENCES room (room_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 3212313910

INSERT INTO room VALUES ('room_01_id', 'Room 01 Name', 'ta_code_01', 'st_code_01');
INSERT INTO room VALUES ('room_02_id', 'Room 02 Name', 'ta_code_02', 'st_code_02');
INSERT INTO room VALUES ('room_03_id', 'Room 03 Name', 'ta_code_03', 'st_code_03');



INSERT INTO taq_user VALUES ('ta_id_0101', 'ta user 0101 Name', 'ta', 'room_01_id', 'ta_0101_session');
INSERT INTO taq_user VALUES ('st_id_0101', 'st user 0101 Name', 'st', 'room_01_id', 'st_0101_session');
INSERT INTO taq_user VALUES ('st_id_0102', 'st user 0102 Name', 'st', 'room_01_id', 'st_0102_session');

INSERT INTO taq_user VALUES ('ta_id_0201', 'ta user 0201 Name', 'ta', 'room_02_id', 'ta_0201_session');
INSERT INTO taq_user VALUES ('st_id_0201', 'st user 0201 Name', 'st', 'room_02_id', 'st_0201_session');
INSERT INTO taq_user VALUES ('st_id_0202', 'st user 0202 Name', 'st', 'room_02_id', 'st_0202_session');

INSERT INTO taq_user VALUES ('ta_id_0301', 'ta user 0301 Name', 'ta', 'room_03_id', 'ta_0301_session');
INSERT INTO taq_user VALUES ('st_id_0301', 'st user 0301 Name', 'st', 'room_03_id', 'st_0301_session');
INSERT INTO taq_user VALUES ('st_id_0302', 'st user 0302 Name', 'st', 'room_03_id', 'st_0302_session');

/*

-- room queue
CREATE TABLE {room_id_queue} (
	student_id alphanum8 PRIMARY KEY,
	place integer UNIQUE NOT NULL,
	CONSTRAINT student_id_fkey FOREIGN KEY (student_id
		REFERENCES student (student_id) ON DELETE CASCADE,
	CONSTRAINT place_positive CHECK (place > 0)
);
*/


