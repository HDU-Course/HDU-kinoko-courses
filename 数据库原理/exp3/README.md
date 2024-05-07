# 实验三 T-SQL 语句操作（二）

## Step

初始化要求里的几张表

```SQL
CREATE TABLE tab_institute(
	instno char(4) NOT NULL PRIMARY KEY,
	instname varchar(50) NULL,
	address varchar(50) NULL);

CREATE TABLE tab_majoy(
	majoyno char(4) NOT NULL PRIMARY KEY,
	majoyname varchar(50) NULL,
	instno char(4) NULL REFERENCES tab_institute(instno));

CREATE TABLE tab_teacher(
	tno char(4) NOT NULL PRIMARY KEY,
	tname varchar(50) NULL,
	tsex char(2) NULL CHECK(tsex='男' or tsex='女'),
	title varchar(10) NULL,
	instno char(4) NULL REFERENCES tab_institute(instno));

CREATE TABLE tab_course(
	cno char(4) NOT NULL PRIMARY KEY,
	cname varchar(50) NULL,
	ctype varchar(10) NULL CHECK(ctype IN ('必修','限选','任选')),
	credit tinyint NULL,
	term tinyint NULL,
	majoyno char(4) NULL REFERENCES tab_majoy(majoyno));

CREATE TABLE tab_student(
	sno char(4) NOT NULL PRIMARY KEY,
	sname varchar(50) NULL,
	ssex char(2) NULL CHECK(ssex='男' or ssex='女'),
	birthday datetime NULL,
	age AS YEAR(GETDATE())-YEAR(birthday),
	class varchar(10) NULL,
	grade tinyint NULL,
	majoyno char(4) NULL REFERENCES tab_majoy(majoyno));

CREATE TABLE tab_score(
	sno char(4) NOT NULL,
	cno char(4) NOT NULL,
	tno char(4) NOT NULL,
	score smallint NULL,
	CONSTRAINT PK_score_1 PRIMARY KEY(sno,cno,tno),
	CONSTRAINT FK_score_student FOREIGN KEY(sno) REFERENCES tab_student(sno),
	CONSTRAINT FK_score_course FOREIGN KEY(cno) REFERENCES tab_course(cno),
	CONSTRAINT FK_score_teacher FOREIGN KEY(tno) REFERENCES tab_teacher(tno));
```

