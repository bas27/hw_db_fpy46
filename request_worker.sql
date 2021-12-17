create table if not exists worker (
	id serial primary key,
	worker_name varchar(40) not null,
	worker_surname varchar(70) not null
);

create table if not exists unit (
	id serial primary key,
	unit_name varchar(70) not null,
	chief integer references worker(id)
);