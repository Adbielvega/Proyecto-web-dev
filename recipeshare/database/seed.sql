USE recipeshare_db;

INSERT INTO users (name, email, password_hash)
VALUES
('Ana Rivera', 'ana@example.com', 'demo_hash_1'),
('Luis Torres', 'luis@example.com', 'demo_hash_2');

INSERT INTO recipes (
    user_id,
    title,
    description,
    ingredients,
    steps,
    prep_minutes
)
VALUES
(
    1,
    'Batida de frutas',
    'Bebida simple para desayuno',
    'Guineo, fresas, leche, hielo',
    'Lavar frutas. Mezclar en licuadora. Servir frio.',
    10
),
(
    2,
    'Pasta con ajo',
    'Cena rapida con pocos ingredientes',
    'Pasta, ajo, aceite de oliva, queso',
    'Hervir pasta. Sofreir ajo. Mezclar y servir.',
    25
);

INSERT INTO recipe_likes (user_id, recipe_id)
VALUES
(1,2),
(2,1);

INSERT INTO favorites (user_id, recipe_id)
VALUES
(1,2);