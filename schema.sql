create table
    if not exists user (
        id integer primary key autoincrement,
        username text not null unique,
        xp float default 0,
        xp_required float default 1,
        total_xp float default 0,
        level integer default 1
    );