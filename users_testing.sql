SELECT * FROM public.users ORDER BY ID;

INSERT INTO users (first_name, last_name, email, password)
VALUES 
    ('John', 'Doe', 'john.doe@example.com', '$2b$12$eA3VfG...fakehash1'),
    ('Jane', 'Smith', 'jane.smith@example.com', '$2b$12$eA3VfG...fakehash2'),
    ('Alex', 'Jones', 'alex.jones@example.com', '$2b$12$eA3VfG...fakehash3'),
    ('Emily', 'Brown', 'emily.b@example.com', '$2b$12$eA3VfG...fakehash4'),
    ('Michael', 'Green', 'm.green@example.com', '$2b$12$eA3VfG...fakehash5')
RETURNING *;