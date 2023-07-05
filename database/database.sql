CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    role VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE tickets(
    id SERIAL PRIMARY KEY NOT NULL,
    responsible_id INTEGER REFERENCES users(id),
    location VARCHAR(120) NOT NULL,
    duration INTEGER NOT NULL,
    registration VARCHAR(12) NOT NULL,
    price DECIMAL NOT NULL,
    paid BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE bulletins(
    id SERIAL PRIMARY KEY NOT NULL,
    responsible_id INTEGER REFERENCES users(id),
    location VARCHAR(120) NOT NULL,
    duration INTEGER NOT NULL,
    registration VARCHAR(60) NOT NULL,
    price DECIMAL NOT NULL,
    paid BOOLEAN NOT NULL DEFAULT false,
    brand VARCHAR(60), /* added */
    model VARCHAR(60), /* added */
    signature VARCHAR(80) NOT NULL, /* added */
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);