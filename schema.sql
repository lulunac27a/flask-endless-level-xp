create table
    if not exists user (
        id integer primary key autoincrement, --user id
        username text not null unique, --username
        xp float default 0, --current user XP
        xp_required float default 1, --user required XP to reach next level
        total_xp float default 0, --user total XP earned
        level integer default 1 --current user level
    );