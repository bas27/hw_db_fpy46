create table if not exists collection (
id_collection serial primary key,
name_collection varchar(100) not null,
release_year numeric(4) not null
);

create table if not exists album (
    id_album serial primary key,
    album_name varchar(40) not null,
    release_year numeric(4) not null
);

create table if not exists track (
    id_track serial primary key,
    track_name varchar(100) not null,
    duration numeric (6),
    id_album integer references album(id_album)
);

create table if not exists albumtrackcollection (
    id serial primary key,
    id_track integer references track(id_track),
    id_collection integer references collection(id_collection)
);

create table if not exists executor (
    id_executor serial primary key,
    executor_name varchar(40) not null,
	surname varchar(100) not null,
	alias varchar(100) unique
);

create table if not exists executoralbum (
    id serial primary key,
    id_executor integer references executor(id_executor),
    id_album integer references album(id_album)
);

create table if not exists genre (
    id_genre serial primary key,
    genre_name varchar(40) not null unique
);

create table if not exists executorgenre (
    id serial primary key,
    id_executor integer references executor(id_executor),
    id_genre integer references genre(id_genre)
);