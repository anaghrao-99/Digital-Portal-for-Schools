
use digischool;


select * from class;

update school set address="73 Cantt, Tagore Road, Kanpur, Uttar Pradesh" where schoolUsername="school01";


INSERT INTO login (username,password,category,name) VALUES ("school01","f3bc8bdd9b4ba08d97bff35a7066549da4d995afa67d97033fd9b4b46627db47d2784b15bb3396d041cb67a17c8db05b9de5a8e8851a7cc1917ac5f7e63aed42","school","Kanpur High School");
INSERT INTO school (schoolUsername,contact,address,email) VALUES ("school01","09670807106","79 civil lines kanpur","school01@gmail.com");


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





insert into teaches(classcode,subject) values ("school011A","hindi");
insert into teaches(classcode,subject) values ("school011A","english");
insert into teaches(classcode,subject) values ("school011A","maths");
insert into teaches(classcode,subject) values ("school011A","science");
insert into teaches(classcode,subject) values ("school011A","social science");
insert into teaches(classcode,subject) values ("school011B","hindi");
insert into teaches(classcode,subject) values ("school011B","english");
insert into teaches(classcode,subject) values ("school011B","maths");
insert into teaches(classcode,subject) values ("school011B","science");
insert into teaches(classcode,subject) values ("school011B","social science");
insert into teaches(classcode,subject) values ("school012A","hindi");
insert into teaches(classcode,subject) values ("school012A","english");
insert into teaches(classcode,subject) values ("school012A","maths");
insert into teaches(classcode,subject) values ("school012A","science");
insert into teaches(classcode,subject) values ("school012A","social science");
insert into teaches(classcode,subject) values ("school012B","hindi");
insert into teaches(classcode,subject) values ("school012B","english");
insert into teaches(classcode,subject) values ("school012B","maths");
insert into teaches(classcode,subject) values ("school012B","science");
insert into teaches(classcode,subject) values ("school012B","social science");
insert into teaches(classcode,subject) values ("school013A","hindi");
insert into teaches(classcode,subject) values ("school013A","english");
insert into teaches(classcode,subject) values ("school013A","maths");
insert into teaches(classcode,subject) values ("school013A","science");
insert into teaches(classcode,subject) values ("school013A","social science");
insert into teaches(classcode,subject) values ("school013B","hindi");
insert into teaches(classcode,subject) values ("school013B","english");
insert into teaches(classcode,subject) values ("school013B","maths");
insert into teaches(classcode,subject) values ("school013B","science");
insert into teaches(classcode,subject) values ("school013B","social science");
insert into teaches(classcode,subject) values ("school014A","hindi");
insert into teaches(classcode,subject) values ("school014A","english");
insert into teaches(classcode,subject) values ("school014A","maths");
insert into teaches(classcode,subject) values ("school014A","science");
insert into teaches(classcode,subject) values ("school014A","social science");
insert into teaches(classcode,subject) values ("school014B","hindi");
insert into teaches(classcode,subject) values ("school014B","english");
insert into teaches(classcode,subject) values ("school014B","maths");
insert into teaches(classcode,subject) values ("school014B","science");
insert into teaches(classcode,subject) values ("school014B","social science");
insert into teaches(classcode,subject) values ("school015A","hindi");
insert into teaches(classcode,subject) values ("school015A","english");
insert into teaches(classcode,subject) values ("school015A","maths");
insert into teaches(classcode,subject) values ("school015A","science");
insert into teaches(classcode,subject) values ("school015A","social science");
insert into teaches(classcode,subject) values ("school015B","hindi");
insert into teaches(classcode,subject) values ("school015B","english");
insert into teaches(classcode,subject) values ("school015B","maths");
insert into teaches(classcode,subject) values ("school015B","science");
insert into teaches(classcode,subject) values ("school015B","social science");
