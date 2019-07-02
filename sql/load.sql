GRANT ALL PRIVILEGES ON *.* TO 'dbadmin'@'%' IDENTIFIED BY 'dbadmin' WITH GRANT OPTION;
create database tvshows ;
use tvshows ;
CREATE TABLE tvshows (id INT not null AUTO_INCREMENT, name VARCHAR (30) not null , finale VARCHAR (100), image VARCHAR (30), PRIMARY KEY (id));
insert into tvshows  values (0, 'breaking bad','brother in law turns to be a dealer','');
insert into tvshows  values (0, 'game of thrones','lord of the knight is hired to refresh spain','');
insert into tvshows  values (0, 'friends','ross marries rachel','');
