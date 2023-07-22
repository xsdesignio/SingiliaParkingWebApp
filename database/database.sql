CREATE TYPE user_role AS ENUM ('ADMIN', 'MANAGER', 'EMPLOYEE', 'USER');


CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    role user_role NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE zones(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    zone_responsibles INTEGER[] NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE withhelds(
    id SERIAL PRIMARY KEY NOT NULL,
    responsible_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE payment_methods(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE available_tickets(
    id SERIAL PRIMARY KEY NOT NULL,
    duration INTEGER NOT NULL UNIQUE,
    price DECIMAL NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE tickets(
    id SERIAL PRIMARY KEY NOT NULL,
    responsible_id INTEGER REFERENCES users(id),
    zone_id INTEGER REFERENCES zones(id),
    duration INTEGER NOT NULL,
    registration VARCHAR(12) NOT NULL,
    price DECIMAL NOT NULL,
    payment_method_id INTEGER REFERENCES payment_methods(id),
    paid BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE bulletins(
    id SERIAL PRIMARY KEY NOT NULL,
    responsible_id INTEGER REFERENCES users(id),
    zone_id INTEGER REFERENCES zones(id),
    duration INTEGER NOT NULL,
    registration VARCHAR(60) NOT NULL,
    price DECIMAL NOT NULL,
    payment_method_id INTEGER REFERENCES payment_methods(id),
    paid BOOLEAN NOT NULL DEFAULT false,
    brand VARCHAR(60), 
    model VARCHAR(60), 
    color VARCHAR(80), 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

