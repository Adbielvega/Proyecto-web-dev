CREATE DATABASE IF NOT EXISTS recipeshare_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE recipeshare_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description VARCHAR(300) NOT NULL,
    ingredients TEXT NOT NULL,
    steps TEXT NOT NULL,
    prep_minutes INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_recipes_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_prep_minutes
        CHECK (prep_minutes > 0)
);

CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_favorites_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_favorites_recipe
        FOREIGN KEY (recipe_id)
        REFERENCES recipes(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_user_recipe_favorite
        UNIQUE(user_id, recipe_id)
);

CREATE TABLE recipe_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_likes_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_likes_recipe
        FOREIGN KEY (recipe_id)
        REFERENCES recipes(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_user_recipe_like
        UNIQUE(user_id, recipe_id)
);

CREATE INDEX idx_recipes_created_at
ON recipes(created_at);

CREATE INDEX idx_recipes_user_id
ON recipes(user_id);

CREATE INDEX idx_likes_recipe_id
ON recipe_likes(recipe_id);

CREATE INDEX idx_favorites_user_id
ON favorites(user_id);