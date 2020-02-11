create database digischool;

use digischool;

show tables;

drop table notes;

create table login(
username varchar(45) Not null,
password varchar(45) not null,
category varchar(45) not null,
name varchar(45) not null,
primary key(username));

create table school(
schoolUsername varchar(45) Not null,
contact int not null unique,
address varchar(45) not null,
email varchar(45) unique,
primary key(schoolUsername),
foreign key(schoolUsername) references login(username)
);


create table teacher(
teacherUsername varchar(45) not null,
schoolUsername varchar(45) not null,
biodata varchar(45),
contact int not null unique,
address varchar(45) not null,
email varchar(45) unique,
primary key(teacherUsername),
foreign key(teacherUsername) references login(username),
foreign key(schoolUsername) references school(schoolUsername));

create table parent(
parentUsername varchar(45) not null,
contact int not null unique,
address varchar(45) not null,
email varchar(45) unique,
primary key(parentUsername),
foreign key(parentUsername) references login(username));

drop table class;
create table class(
classcode varchar(45) not null,
schoolUsername varchar(45) not null,
standard varchar(10) not null,
section varchar(1) not null,
classTeacher varchar(45),
primary key(classcode,schoolUsername),
foreign key(schoolUsername) references school(schoolUsername),
foreign key(classTeacher) references teacher(teacherUsername));

create table student(
studentUsername varchar(45) not null,
classcode varchar(45) not null,
schoolUsername varchar(45) not null,
parentUsername varchar(45) not null,
primary key(studentUsername),
foreign key(schoolUsername) references school(schoolUsername),
foreign key(parentUsername) references parent(parentUsername),
foreign key(studentUsername) references login(username),
foreign key(classcode) references class(classcode));

create table schoolNews(
schoolUsername varchar(45) not null,
newsArticle varchar(100) not null,
image varchar(100) ,
foreign key(schoolUsername) references school(schoolUsername));

create table schoolComments(
schoolUsername varchar(45) not null,
comment varchar(100) not null,
commenter varchar(45) not null,
upvote int not null default 0,
downvote int not null default 0,
foreign key(schoolUsername) references school(schoolUsername),
foreign key(commenter) references login(username)
);

create table notes(
studentUsername varchar(45) not null,
teacherUsername varchar(45) not null,
subject varchar(45),
note varchar(200) not null,
signature varchar(10) not null default 'Unsigned',
foreign key(studentUsername) references student(studentUsername),
foreign key(teacherUsername) references teacher(teacherUsername)
);

create table results(
studentUsername varchar(45) not null,
exam varchar(45) not null,
subject varchar(45) not null,
marks varchar(45) not null,
primary key(studentUsername, exam, subject),
foreign key(studentUsername) references student(studentUsername));


