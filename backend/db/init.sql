DROP TABLE IF EXISTS "emprestimos";
DROP TABLE IF EXISTS "livros";

CREATE TABLE "livros" (
    "id" SERIAL PRIMARY KEY,
    "titulo" VARCHAR(255) NOT NULL,
    "autor" VARCHAR(255) NOT NULL,
    "ano" INTEGER NOT NULL,
    "genero" VARCHAR(255),
    "quantidade" INTEGER NOT NULL
);

CREATE TABLE "emprestimos" (
    "id" SERIAL PRIMARY KEY, 
    "id_livro" INT NOT NULL,
    "nome_usuario" VARCHAR(255) NOT NULL,
    "data_emprestimo" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "data_devolucao" TIMESTAMP
);

INSERT INTO "livros" ("titulo", "autor", "ano", "genero", "quantidade")  VALUES ('Harry Potter e a Pedra Filosofal', 'J.K. Rowling', 1997, 'Fantasia', 5);
INSERT INTO "livros" ("titulo", "autor", "ano", "genero", "quantidade")  VALUES ('Orgulho e Preconceito', 'Jane Austen', 1813, 'Romance', 3);
INSERT INTO "livros" ("titulo", "autor", "ano", "genero", "quantidade")  VALUES ('O Senhor dos Anéis', 'J.R.R. Tolkien', 1954, 'Fantasia', 2);
INSERT INTO "livros" ("titulo", "autor", "ano", "genero", "quantidade")  VALUES ('Os Bridgertons', 'Julia Quinn', 2000, 'Romance', 5);
INSERT INTO "livros" ("titulo", "autor", "ano", "genero", "quantidade")  VALUES ('Para Todos os Garotos Que Já Amei', 'Jenny Han', 2014, 'Romance', 3);
INSERT INTO "livros" ("titulo", "autor", "ano", "genero", "quantidade")  VALUES ('The Witcher', 'Andrzej Sapkowski', 1992, 'Fantasia', 2);
