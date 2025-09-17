
/*
 * Create users table
 */
CREATE TABLE IF NOT EXISTS users
(
    user_id uuid, -- generated session ID or auth0

    age text,
    location text,
    occupation text,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS user_accounts
(
    user_id uuid, -- ID given by auth0
    auth0_token text,

    username text,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS session_users
(
    user_id uuid,

    token text,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

/*
 * Create takes table
 */
CREATE TABLE IF NOT EXISTS takes
(
    take_id uuid DEFAULT gen_random_uuid(),

    title text,
    newtitle text,

    description text,
    tag text,

    author_id uuid,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (take_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

/*
 * Create user_take_ratings table
 */
CREATE TABLE IF NOT EXISTS user_take_ratings
(
    user_id uuid,
    take_id uuid,

    rating numeric(3, 1), -- limits to 1 decimal place

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, take_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (take_id) REFERENCES takes(take_id)
);

/*
 * Create comments table
 */
CREATE TABLE IF NOT EXISTS comments
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
