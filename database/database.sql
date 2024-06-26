CREATE TYPE user_role AS ENUM ('ADMIN', 'MANAGER', 'EMPLOYEE');
CREATE TYPE payment_method_type AS ENUM ('CASH', 'CARD');


CREATE TABLE available_tickets(
    id SERIAL PRIMARY KEY NOT NULL,
    duration VARCHAR(40) NOT NULL UNIQUE,
    duration_minutes INTEGER NOT NULL DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE available_bulletins(
    id SERIAL PRIMARY KEY NOT NULL,
    duration VARCHAR(40) NOT NULL UNIQUE,
    duration_minutes INTEGER NOT NULL DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE zones(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL UNIQUE,
    identifier VARCHAR(2) DEFAULT 'AA' NOT NULL UNIQUE, 
    tickets INTEGER NOT NULL DEFAULT 0,
    bulletins INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    role user_role NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    withheld DECIMAL(10, 2) NOT NULL DEFAULT 0,
    associated_zone_id INTEGER REFERENCES zones(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE tickets(
    id VARCHAR(8) PRIMARY KEY NOT NULL CONSTRAINT chk_id_format CHECK (id ~ '^[A-Z]{2}/\d{5}$'),
    responsible_id INTEGER REFERENCES users(id),
    zone_id INTEGER REFERENCES zones(id),
    duration VARCHAR(60) NOT NULL,
    registration VARCHAR(12) NOT NULL DEFAULT "-",
    price DECIMAL(10, 2) NOT NULL,
    payment_method payment_method_type NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE bulletins(
    id VARCHAR(8) PRIMARY KEY NOT NULL CONSTRAINT chk_id_format CHECK (id ~ '^[A-Z]{2}/\d{5}$'),
    responsible_id INTEGER REFERENCES users(id),
    zone_id INTEGER REFERENCES zones(id),
    duration VARCHAR(60),
    registration VARCHAR(12) NOT NULL DEFAULT "-",
    price DECIMAL(10, 2),
    payment_method payment_method_type,
    paid BOOLEAN NOT NULL DEFAULT false,
    precept VARCHAR(255) NOT NULL DEFAULT 'Estacionar sin ticket de aparcamiento',
    brand VARCHAR(60), 
    model VARCHAR(60), 
    color VARCHAR(80), 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- SCHEDULE

/* 
CREATE TABLE openSpan (
    id SERIAL PRIMARY KEY NOT NULL,
    openTime TIME NOT NULL,
    closeTime TIME NOT NULL
); */

/* 
CREATE TABLE dailyOpenTimes(
    id SERIAL PRIMARY KEY NOT NULL,
    dailyScheduleId INTEGER REFERENCES dailySchedule(id) NOT NULL,
    openSpanId INTEGER REFERENCES openSpan(id) NOT NULL,
);
 */
 
 
CREATE TYPE openSpan AS (
    openTime TIME,
    closeTime TIME
);

CREATE TABLE dailySchedule(
    id SERIAL PRIMARY KEY NOT NULL,
    openSpans openSpan[]
);


CREATE TABLE weekSchedule(
    id SERIAL PRIMARY KEY NOT NULL,
    monday INTEGER REFERENCES dailySchedule(id),
    tuesday INTEGER REFERENCES dailySchedule(id),
    wednesday INTEGER REFERENCES dailySchedule(id),
    thursday INTEGER REFERENCES dailySchedule(id),
    friday INTEGER REFERENCES dailySchedule(id),
    saturday INTEGER REFERENCES dailySchedule(id),
    sunday INTEGER REFERENCES dailySchedule(id)
);


