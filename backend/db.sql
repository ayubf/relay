CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username VARCHAR(255) NOT NULL,
    pwd TEXT 
);

CREATE TABLE meetings (
    id SERIAL PRIMARY KEY, 
    meeting_name VARCHAR(255) NOT NULL, 
    code TEXT, 
    expiration_time TIMESTAMP NOT NULL
);