drop table if exists entries;
create table entries(
  id integer primary key autoincrement,
  time datetime not null,
  note text not null
);
