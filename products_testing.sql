--view all products
SELECT * FROM "Products_Testing" ORDER BY "ID" ASC 


--dummy data insertion
INSERT INTO products_testing ("Name", "Price", "Date", "Inventory", "Sale")
VALUES 
    ('MacBook Pro', 1999, NOW()::time, 5, false),
    ('PlayStation 5', 499, NOW()::time, 12, true),
    ('Nintendo Switch 2', 399, NOW()::time, 8, false),
    ('Pixel Watch', 299, NOW()::time, 15, true),
    ('AirPods Pro', 249, NOW()::time, 20, false);