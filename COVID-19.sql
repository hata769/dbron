CREATE DATABASE if NOT EXISTS dbron;
USE dbron;

DROP TABLE if EXISTS answertbl;
DROP TABLE if EXISTS suspension;
DROP TABLE if EXISTS check_health;
DROP TABLE if EXISTS suspension;
DROP TABLE if EXISTS check_health;
DROP TABLE if EXISTS activity;
DROP TABLE if EXISTS user_from;
DROP TABLE if EXISTS user_pass;
DROP TABLE if EXISTS user;
DROP TABLE if EXISTS department;
DROP TABLE if EXISTS school;

CREATE TABLE school (
    schoolID INT NOT NULL AUTO_INCREMENT,
    school_name VARCHAR(100) NOT NULL,
    post_num VARCHAR(8) NOT NULL,
    prefecture VARCHAR(10),
    city VARCHAR(30),
    area VARCHAR(50),
    lastupdate DATETIME,
    PRIMARY KEY (schoolID)
);

CREATE TABLE department (
    officeID INT NOT NULL AUTO_INCREMENT,
    schoolID INT NOT NULL,
    department_name VARCHAR(50) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    delflag BOOL DEFAULT FALSE,
    lastupdate DATETIME,
    PRIMARY KEY (officeID),
    FOREIGN KEY (schoolID)
        REFERENCES school(schoolID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE user(
	userID INT NOT NULL AUTO_INCREMENT,
	schoolID INT NOT NULL,
	affiliation VARCHAR(50) NOT NULL,
	user_code VARCHAR(20) NOT NULL,
	l_name VARCHAR(30) NOT NULL,
	f_name VARCHAR(30) NOT NULL,
	l_name_kana VARCHAR(30) NOT NULL,
	f_name_kana VARCHAR(30) NOT NULL,
	gender BOOL NOT NULL,
	birthday DATE NOT NULL,
	delflag BOOL DEFAULT FALSE,
	lastupdate DATETIME,
	PRIMARY KEY(userID),
	FOREIGN KEY (schoolID)
        REFERENCES school(schoolID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
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
	userID INT NOT NULL unique,
	permission INT NOT NULL,
	user_name VARCHAR(50) NOT NULL,
	password VARCHAR(100) NOT NULL,
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
	activityID INT NOT NULL AUTO_INCREMENT,
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
	PRIMARY KEY(activityID),
	FOREIGN KEY(userID)
		REFERENCES user(userID)
		ON DELETE CASCADE
		ON UPDATE CASCADE
)
;

CREATE TABLE suspension (
    suspensionID INT NOT NULL AUTO_INCREMENT,
    userID INT NOT NULL,
    susp_school BOOL DEFAULT FALSE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason VARCHAR(200),
    institution_name VARCHAR(50),
    doctor_name VARCHAR(50),
    status INT NOT NULL COMMENT '感染=0, 未感染=1, 濃厚接触=2',
    mention VARCHAR(200),
    delflag BOOL DEFAULT FALSE,
    lastupdate DATETIME,
    PRIMARY KEY (suspensionID),
    FOREIGN KEY (userID)
        REFERENCES user(userID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE answertbl (
    answertblID INT NOT NULL AUTO_INCREMENT,
    userID INT NOT NULL,
    question VARCHAR(300),
    answer VARCHAR(300),
    delflag BOOL DEFAULT FALSE,
    lastupdate DATETIME,
    PRIMARY KEY (answertblID),
    FOREIGN KEY (userID)
        REFERENCES user(userID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DESC school;
DESC department;
DESC user;
DESC user_from;
DESC user_pass;
DESC check_health;
DESC activity;
DESC suspension;
DESC answertbl;
