CREATE DATABASE if NOT EXISTS dbron;
USE dbron;

DROP TABLE if EXISTS diagnosis;
DROP TABLE if EXISTS suspension;
DROP TABLE if EXISTS doctors;
DROP TABLE if EXISTS medical_institution;
DROP TABLE if EXISTS check_health;
DROP TABLE if EXISTS activity;
DROP TABLE if EXISTS user_from;
DROP TABLE if EXISTS user_pass;
DROP TABLE if EXISTS user;

CREATE TABLE user(
	userID INT NOT NULL AUTO_INCREMENT,
	affiliation VARCHAR(50) NOT NULL,
	user_code VARCHAR(20) NOT NULL,
	l_name VARCHAR(30) NOT NULL,
	f_name VARCHAR(30) NOT NULL,
	l_name_kana VARCHAR(30) NOT NULL,
	f_name_kana VARCHAR(30) NOT NULL,
	birthday DATE NOT NULL,
	lustupdate DATETIME,
	PRIMARY KEY(userID)
)
;

CREATE TABLE user_from(
	user_fromID INT NOT NULL AUTO_INCREMENT,
	userID INT NOT NULL,
	return_home BOOL DEFAULT FALSE,
	post_num VARCHAR(8) NOT NULL,
	prefecture VARCHAR(10),
	city VARCHAR(30),
	AREA VARCHAR(50),
	phone VARCHAR(11),
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY (user_fromID),
	FOREIGN KEY(userID)
		REFERENCES user(userID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

create TABLE user_pass(
	user_passID INT NOT NULL AUTO_INCREMENT,
	userID INT NOT NULL,
	permission INT NOT NULL,
	user_name VARCHAR(50) NOT NULL,
	password VARCHAR(20) NOT NULL,
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY (user_passID),
	FOREIGN KEY(userID)
		REFERENCES user(userID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;
CREATE TABLE check_health(
	check_healthID INT NOT NULL AUTO_INCREMENT,
	userID INT NOT NULL,
	input_date DATE NOT NULL,
	am_pm BOOL NOT NULL,
	body_temp FLOAT NOT NULL DEFAULT FALSE,
	pain BOOL NOT NULL DEFAULT FALSE,
	washedout_feeling BOOL NOT NULL DEFAULT FALSE,
	headache BOOL NOT NULL DEFAULT FALSE,
	sore_throat BOOL NOT NULL DEFAULT FALSE,
	breathless BOOL NOT NULL DEFAULT FALSE,
	cough BOOL NOT NULL DEFAULT FALSE,
	vomiting BOOL NOT NULL DEFAULT FALSE,
	diarrhea BOOL NOT NULL DEFAULT FALSE,
	taste_disorder BOOL NOT NULL DEFAULT FALSE,
	olfactory_disorder BOOL NOT NULL DEFAULT FALSE,
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(check_healthID),
	FOREIGN KEY(userID)
		REFERENCES user(userID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

CREATE TABLE activity(
	check_activityID INT NOT NULL AUTO_INCREMENT,
	userID INT NOT NULL,
	went_date DATE NOT NULL,
	went_time TIME NOT NULL,
	return_time TIME NOT NULL,
	location VARCHAR(50) NOT NULL,
	move_method VARCHAR(20) NOT NULL,
	departure VARCHAR(100) NOT NULL,
	arrival VARCHAR(100) NOT NULL,
	comp_NY BOOL DEFAULT FALSE,
	comp_num VARCHAR(50),
	sp_mention VARCHAR(100),
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(check_activityID),
	FOREIGN KEY(userID)
		REFERENCES user(userID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

CREATE TABLE suspension(
	suspensionID INT NOT NULL AUTO_INCREMENT,
	userID INT NOT NULL,
	susp_school BOOL DEFAULT FALSE,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	reason VARCHAR(200),
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(suspensionID),
	FOREIGN KEY(userID)
		REFERENCES user(userID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

CREATE TABLE medical_institution(
	medical_institutionID INT NOT NULL AUTO_INCREMENT,
	institution_name VARCHAR(50) NOT NULL,
	post_num VARCHAR(8) NOT NULL,
	prefecture VARCHAR(10),
	city VARCHAR(30),
	area VARCHAR(50),
	phone VARCHAR(11),
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(medical_institutionID)
)
;

CREATE TABLE doctors(
	doctorsID INT NOT NULL AUTO_INCREMENT,
	medical_institutionID INT NOT NULL,
	doctor_l_name VARCHAR(30) NOT NULL,
	doctor_f_name VARCHAR(30) NOT NULL,
	doctor_l_name_kana VARCHAR(30) NOT NULL,
	doctor_f_name_kana VARCHAR(30) NOT NULL,
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(doctorsID),
	FOREIGN KEY(medical_institutionID)
		REFERENCES medical_institution(medical_institutionID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

CREATE TABLE diagnosis(
	diagnosisID INT NOT NULL AUTO_INCREMENT,
	suspensionID INT NOT NULL,
	medical_institution VARCHAR(50) NOT NULL,
	doctor VARCHAR(50) NOT NULL,
	diag_date DATE NOT NULL,
	close_contact BOOL DEFAULT FALSE,
	test_results BOOL DEFAULT FALSE,
	location VARCHAR(50),
	mention VARCHAR(200),
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(diagnosisID),
	FOREIGN KEY(suspensionID)
		REFERENCES suspension(suspensionID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

DESC user;
DESC user_from;
DESC user_pass;
DESC check_health;
DESC activity;
DESC suspension;
DESC medical_institution;
DESC doctors;
DESC diagnosis;
