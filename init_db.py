import sqlite3
from werkzeug.security import generate_password_hash

DB = "escola.db"


def criar_banco():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS notas;
        DROP TABLE IF EXISTS alunos;
        DROP TABLE IF EXISTS usuarios;

        CREATE TABLE usuarios (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT UNIQUE NOT NULL,
            senha     TEXT NOT NULL,          -- hash da senha
            role      TEXT NOT NULL,          -- 'admin' ou 'aluno'
            aluno_id  INTEGER                 -- vincula login de aluno ao cadastro
        );

        CREATE TABLE alunos (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            nome             TEXT NOT NULL,
            data_nascimento  TEXT NOT NULL,
            endereco         TEXT NOT NULL,
            celular          TEXT NOT NULL
        );

        CREATE TABLE notas (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id  INTEGER NOT NULL,
            materia   TEXT NOT NULL,
            nota      REAL NOT NULL,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id)
        );
        """
    )

    alunos = [
        ("Maria Silva",  "2008-03-14", "Rua das Flores, 120 - SBC/SP",  "(11) 94455-1020"),
        ("Joao Pereira", "2007-11-02", "Av. Brasil, 870 - Santo Andre", "(11) 93311-4567"),
        ("Ana Souza",    "2008-07-25", "Rua Minas Gerais, 45 - SBC/SP", "(11) 98822-7788"),
    ]
    cur.executemany(
        "INSERT INTO alunos (nome, data_nascimento, endereco, celular) VALUES (?, ?, ?, ?)",
        alunos,
    )

    notas = [
        (1, "Matematica", 7.5), (1, "Portugues", 8.0), (1, "Historia", 6.0),
        (2, "Matematica", 5.5), (2, "Portugues", 9.0), (2, "Geografia", 7.0),
        (3, "Matematica", 8.5), (3, "Biologia", 9.5), (3, "Ingles", 6.5),
    ]
    cur.executemany(
        "INSERT INTO notas (aluno_id, materia, nota) VALUES (?, ?, ?)", notas
    )

    # SENHAS FRACAS DE PROPOSITO (formato que o CUPP gera: nome + ano)
    #   admin -> maria1985   |   maria (aluna) -> maria2008
    usuarios = [
        ("admin", generate_password_hash("maria1985"), "admin", None),
        ("maria", generate_password_hash("maria2008"), "aluno", 1),
    ]
    cur.executemany(
        "INSERT INTO usuarios (username, senha, role, aluno_id) VALUES (?, ?, ?, ?)",
        usuarios,
    )

    conn.commit()
    conn.close()
    print(f"[ok] Banco '{DB}' criado.")
    print("     admin -> usuario: admin | senha: maria1985")
    print("     aluno -> usuario: maria | senha: maria2008")


if __name__ == "__main__":
    criar_banco()