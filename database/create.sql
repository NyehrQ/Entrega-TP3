CREATE DATABASE empresa_quimica;

CREATE TABLE wishlist (
    id INT(11) NOT NULL AUTO_INCREMENT,
    usuario_id INT(11) NOT NULL,
    producto_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    KEY (usuario_id),
    KEY (producto_id)
);

INSERT INTO wishlist (id, usuario_id, producto_id) VALUES
(5, 2, 1),
(3, 2, 2),
(4, 2, 3),
(1, 2, 4),
(6, 2, 8),
(9, 2, 11),
(10, 2, 14),
(11, 2, 15),
(12, 2, 19),
(13, 2, 20),
(2, 3, 2);