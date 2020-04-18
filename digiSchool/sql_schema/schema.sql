
create database digischool;
use digischool;

select * from teacher;

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
primary key(classcode,subject),
foreign key(teacherUsername) references teacher(teacherUsername),
foreign key(classcode) references class(classcode));
SET SQL_SAFE_UPDATES = 0;
update teaches set subject="social_science" where subject="social science";
select * from teaches;

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
id int auto_increment not null,
schoolUsername varchar(45) not null,
newsArticle varchar(100) not null,
image varchar(100) ,
primary key(id),
foreign key(schoolUsername) references school(schoolUsername));


delete from schoolNews where id=4;

create table schoolComments(
id int auto_increment,
schoolUsername varchar(45) not null,
comment varchar(512) not null,
commenter varchar(45) not null,
upvote int not null,
downvote int not null,
primary key(id),
foreign key(schoolUsername) references school(schoolUsername),
foreign key(commenter) references login(username)
);


create table likes(
id int not null,
user varchar(45) not null,
vote int not null,
primary key(id,user),
foreign key(id) references schoolComments(id),
foreign key(user) references login(username)
);

create table notes(
id int auto_increment,
studentUsername varchar(45) not null,
teacherUsername varchar(45) not null,
subject varchar(45),
note varchar(200) not null,
signature varchar(10) not null default 'Unsigned',
primary key(id),
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
	
select * from notes;
select * from student;

