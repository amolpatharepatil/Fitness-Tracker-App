drop database if exists fitness_tracker;
create database fitness_tracker;
use fitness_tracker;


drop table if exists `Users` ;
create table  if not exists `Users`(
    `Name` varchar(50) not null,	
	`Password` varchar(50) not null,
	`Email` varchar(50) not null
);

drop table if exists `Trainer` ;
create table  if not exists `Trainer`(
    `Name` varchar(50) not null,	
	`Password` varchar(50) not null,
	`Email` varchar(50) not null
);

drop table if exists `weightLog` ;
create table if not exists `weightLog` (
`Email` varchar(50) NOT NULL, 
`Timestamp` varchar(50) not null,
`Weight`  varchar(50) not null
);

drop table if exists `Goals` ;
create table if not exists `Goals` (
`Email` varchar(50) not null,
`Intensity` varchar(50) default null, 
`Current Weight` varchar(50) default null,
`Target Weight`  varchar(50) default null
);


drop table if exists `Workout Plans` ;
create table if not exists `Exercise Plans` (
`PlanID` varchar(50) not null, 
`Plan Name`  varchar(50) not null,
`Creator` varchar(50) not null
);

insert into `Exercise Plans` values("001","Beginner", "Default");
insert into `Exercise Plans` values("002","Intermediate", "Default");
insert into `Exercise Plans` values("003","Advanced", "Default");

drop table if exists `Exercises` ;
create table if not exists `Exercises` (
`ExerciseID` varchar(50) not null, 
`PlanID`  varchar(50) not null,
`Exercise` varchar(50) not null
);
