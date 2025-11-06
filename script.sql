create table posts (
   id          number generated always as identity primary key,
   img         varchar2(255),
   alt_text    varchar2(255),
   title       varchar2(150),
   description clob,
   content     clob,
   category    varchar2(80),
   author      varchar2(80),
   post_date   date,
   read_time   varchar2(20)
)

create table contacts (
   id      number generated always as identify primary key,
   name    varchar2(100),
   email   varchar2(100),
   message clob
)