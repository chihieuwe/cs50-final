CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    name TEXT NOT NULL, 
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 100.00
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE service (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER,
    image_path TEXT,
    service TEXT,
    name TEXT,
    age TEXT,
    cash_spent NUMERIC,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
