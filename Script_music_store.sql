create table if not exists executor (
	id serial primary key, 
	executor_name varchar(40) not null,
	surname varchar(100) not null,
	alias varchar(100) unique
);

create table if not exists album (
	id serial primary key, 
	album_name varchar(40) not null,
	release_year numeric(4) not null,
	id_executor integer references executor(id)
);

create table if not exists track (
	id serial primary key, 
	track_name varchar(40) not null,
	duration numeric (6),
	id_album integer references album(id)
);

create table if not exists genre (
	id serial primary key, 
	genre_name varchar(40) not null unique
);

alter table executor add column genre_id integer references genre(id);
	
