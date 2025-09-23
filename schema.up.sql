CREATE SCHEMA hot_takes AUTHORIZATION csci5117

-- Create users super-class
CREATE TABLE IF NOT EXISTS hot_takes.users
(
    user_id uuid NOT NULL, -- generated session ID or auth0

    age text,
    location text,
    occupation text,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id)
)
-- Create account user table
CREATE TABLE IF NOT EXISTS hot_takes.user_accounts
(
    user_id uuid NOT NULL, -- ID given by auth0

    username text NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
-- Create session user table
CREATE TABLE IF NOT EXISTS hot_takes.session_users
(
    user_id uuid NOT NULL,

    token text NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
-- Create tags table
CREATE TABLE IF NOT EXISTS hot_takes.tags
(
    tag_id serial,

    label text,
    category text,

    PRIMARY KEY (tag_id)
)
-- Create takes table
CREATE TABLE IF NOT EXISTS hot_takes.takes
(
    take_id uuid NOT NULL DEFAULT gen_random_uuid(),

    title text NOT NULL,
    newtitle text,

    description text,
    tag_id integer NOT NULL,

    author_id uuid,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (take_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
)
-- Create take-rating table
CREATE TABLE IF NOT EXISTS hot_takes.take_ratings
(
    take_id uuid NOT NULL,
    user_id uuid NOT NULL,

    rating numeric(3, 1), -- limits to 1 decimal place

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, take_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (take_id) REFERENCES takes(take_id)
)
-- Create take-comments table
CREATE TABLE IF NOT EXISTS hot_takes.take_comments
(
    take_id uuid,
    commenter_id uuid,
    comment_id serial,

    comment text,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (take_id, commenter_id, comment_id),
    FOREIGN KEY (take_id) REFERENCES takes(take_id),
    FOREIGN KEY (commenter_id) REFERENCES users(user_id)
);
