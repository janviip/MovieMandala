--______________________________________________________________________________________
-- 1. CREATE DATABASE 
--______________________________________________________________________________________
CREATE DATABASE IF NOT EXISTS movie_mandala; 
USE movie_mandala;

--______________________________________________________________________________________
-- 2. USERS TABLE (Login/Signup)
--______________________________________________________________________________________
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--______________________________________________________________________________________
-- 3. MOVIES TABLE (Dataset for ML)
--______________________________________________________________________________________
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    director VARCHAR(100),
    release_year INT,
    overview TEXT,
);

--______________________________________________________________________________________
-- 4. SEARCH HISTORY (User Activity)
--______________________________________________________________________________________
CREATE TABLE search_history (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_name VARCHAR(255),
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);



