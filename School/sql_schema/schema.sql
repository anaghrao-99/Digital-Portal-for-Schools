
create database digischool;
use digischool;


INSERT INTO login (username,password,category,name) VALUES ("school01","f3bc8bdd9b4ba08d97bff35a7066549da4d995afa67d97033fd9b4b46627db47d2784b15bb3396d041cb67a17c8db05b9de5a8e8851a7cc1917ac5f7e63aed42","school","Kanpur High School");
INSERT INTO school (schoolUsername,contact,address,email) VALUES ("school01","09670807106","79 civil lines kanpur","school01@gmail.com");

"school register"

insert into classStructure(classcode,schoolUsername, standard,section) values ("school011A","school01","1","A");
insert into classStructure(classcode,schoolUsername, standard,section) values ("school011B","school01","1","B");

insert into classStructure(classcode,schoolUsername, standard,section) values ("school012A","school01","2","A");
insert into classStructure(classcode,schoolUsername, standard,section) values ("school012B","school01","2","B");

insert into classStructure(classcode,schoolUsername, standard,section) values ("school013A","school01","3","A");
insert into classStructure(classcode,schoolUsername, standard,section) values ("school013B","school01","3","B");

insert into classStructure(classcode,schoolUsername, standard,section) values ("school014A","school01","4","A");
insert into classStructure(classcode,schoolUsername, standard,section) values ("school014B","school01","4","B");

insert into classStructure(classcode,schoolUsername, standard,section) values ("school015A","school01","5","A");
insert into classStructure(classcode,schoolUsername, standard,section) values ("school015B","school01","5","B");


insert into class(classcode) values ("school011A");
insert into class(classcode) values ("school011B");
insert into class(classcode) values ("school012A");
insert into class(classcode) values ("school012B");
insert into class(classcode) values ("school013A");
insert into class(classcode) values ("school013B");
insert into class(classcode) values ("school014A");
insert into class(classcode) values ("school014B");
insert into class(classcode) values ("school015A");
insert into class(classcode) values ("school015B");








create table login(
username varchar(45) Not null,
password varchar(45) not null,
category varchar(45) not null,
name varchar(45) not null,
primary key(username));

create table school(
schoolUsername varchar(45) Not null,
contact varchar(11) not null unique,
address varchar(45) not null,
email varchar(45) unique,
primary key(schoolUsername),
foreign key(schoolUsername) references login(username)
);


create table teacher(
teacherUsername varchar(45) not null,
schoolUsername varchar(45) not null,
biodata varchar(45),
contact varchar(11) not null unique,
address varchar(45) not null,
email varchar(45) unique,
verifiedby varchar(45) not null,
verified varchar(45) not null,
primary key(teacherUsername),
foreign key(teacherUsername) references login(username),
foreign key(schoolUsername) references school(schoolUsername));

create table class(
classcode varchar(90) not null,
classTeacher varchar(45),
primary key(classcode),
foreign key(classTeacher) references teacher(teacherUsername));

create table classStructure(
classcode varchar(90) not null,
schoolUsername varchar(45) not null,
standard varchar(10) not null,
section varchar(1) not null,
primary key(classcode),
foreign key(schoolUsername) references school(schoolUsername));

create table teaches(
classcode varchar(90) not null,
subject varchar(45) not null,
teacherUsername varchar(45),
foreign key(teacherUsername) references teacher(teacherUsername),
foreign key(classcode) references class(classcode));


create table parent(
parentUsername varchar(45) not null,
contact varchar(11) not null unique,
address varchar(45) not null,
email varchar(45) unique,
primary key(parentUsername),
foreign key(parentUsername) references login(username));



create table student(
studentUsername varchar(90) not null,
classcode varchar(45) not null,
schoolUsername varchar(45) not null,
parentUsername varchar(45) not null,
verifiedby varchar(45) not null,
verified varchar(45) not null,
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
	


