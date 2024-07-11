CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS public.users;

CREATE TABLE public.users (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    display_name TEXT,
    handle TEXT,
    email TEXT,
    cognito_user_id TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp NOT NULL
);

DROP TABLE IF EXISTS public.activities;

CREATE TABLE public.activities (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_uuid UUID NOT NULL,
    message TEXT NOT NULL,
    replies_count INT DEFAULT 0,
    reposts_count INT DEFAULT 0,
    likes_count INT DEFAULT 0,
    reply_to_activity_uuid INT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT current_timestamp NOT NULL 

);