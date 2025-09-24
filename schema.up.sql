-- Add schema for user
CREATE SCHEMA hot_takes AUTHORIZATION csci5117;

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
);
-- Create account user table
CREATE TABLE IF NOT EXISTS hot_takes.user_accounts
(
    user_id uuid NOT NULL, -- ID given by auth0

    username text NOT NULL,

    FOREIGN KEY (user_id) REFERENCES hot_takes.users(user_id)
);
-- Create session user table
CREATE TABLE IF NOT EXISTS hot_takes.session_users
(
    user_id uuid NOT NULL,

    token text NOT NULL,

    FOREIGN KEY (user_id) REFERENCES hot_takes.users(user_id)
);
-- Add category type for tags
CREATE TYPE hot_takes.category AS ENUM (
  '🎬 Entertainment',
  '🏆 Sports',
  '🍔 Food & Lifestyle',
  '💻 Tech & Business',
  '🌍 Society & Current Events',
  '📚 Academics'
);
-- Create tags table
CREATE TABLE IF NOT EXISTS hot_takes.tags
(
    tag_id serial NOT NULL,

    label text NOT NULL,
    category hot_takes.category NOT NULL,

    PRIMARY KEY (tag_id)
);
-- Create takes table
CREATE TABLE IF NOT EXISTS hot_takes.takes
(
    take_id uuid NOT NULL DEFAULT gen_random_uuid(),

    title text NOT NULL,
    new_title text,

    description text,
    tag_id integer NOT NULL,

    author_id uuid,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (take_id),
    FOREIGN KEY (tag_id) REFERENCES hot_takes.tags(tag_id),
    FOREIGN KEY (author_id) REFERENCES hot_takes.users(user_id)
);
-- Create take-rating table
CREATE TABLE IF NOT EXISTS hot_takes.take_ratings
(
    take_id uuid NOT NULL,
    user_id uuid NOT NULL,

    -- limit to 1 decimal place
    rating numeric(3, 1) NOT NULL,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, take_id),
    FOREIGN KEY (user_id) REFERENCES hot_takes.users(user_id),
    FOREIGN KEY (take_id) REFERENCES hot_takes.takes(take_id)
);
-- Create take-comments table
CREATE TABLE IF NOT EXISTS hot_takes.take_comments
(
    take_id uuid NOT NULL,
    commenter_id uuid NOT NULL,
    comment_id serial NOT NULL,

    comment text,

    created_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamptz(0) DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (take_id, commenter_id, comment_id),
    FOREIGN KEY (take_id) REFERENCES hot_takes.takes(take_id),
    FOREIGN KEY (commenter_id) REFERENCES hot_takes.users(user_id)
);

INSERT INTO tags (category, value)
VALUES
  ('🎬 Entertainment', 'movies'),
  ('🎬 Entertainment', 'tv-shows'),
  ('🎬 Entertainment', 'pop-culture'),
  ('🎬 Entertainment', 'celebrities'),
  ('🎬 Entertainment', 'books'),
  ('🎬 Entertainment', 'anime'),
  ('🎬 Entertainment', 'cartoons'),
  ('🎬 Entertainment', 'award-shows'),
  ('🎬 Entertainment', 'memes'),
  ('🎬 Entertainment', 'video-games'),

  ('🏆 Sports', 'sports'),
  ('🏆 Sports', 'nfl'),
  ('🏆 Sports', 'nba'),
  ('🏆 Sports', 'nhl'),
  ('🏆 Sports', 'olympics'),

  ('🍔 Food & Lifestyle', 'food'),
  ('🍔 Food & Lifestyle', 'fast-food'),
  ('🍔 Food & Lifestyle', 'restaurants'),
  ('🍔 Food & Lifestyle', 'cooking'),
  ('🍔 Food & Lifestyle', 'relationships'),
  ('🍔 Food & Lifestyle', 'dating'),
  ('🍔 Food & Lifestyle', 'fashion'),
  ('🍔 Food & Lifestyle', 'travel'),
  ('🍔 Food & Lifestyle', 'health'),
  ('🍔 Food & Lifestyle', 'animals'),
  ('🍔 Food & Lifestyle', 'pets'),

  ('💻 Tech & Business', 'social-media'),
  ('💻 Tech & Business', 'ai'),
  ('💻 Tech & Business', 'hardware'),
  ('💻 Tech & Business', 'finance'),
  ('💻 Tech & Business', 'technology'),

  ('🌍 Society & Current Events', 'climate-change'),
  ('🌍 Society & Current Events', 'current-events'),
  ('🌍 Society & Current Events', 'news'),
  ('🌍 Society & Current Events', 'geography'),
  ('🌍 Society & Current Events', 'history'),

  ('📚 Academics', 'science'),
  ('📚 Academics', 'math');
