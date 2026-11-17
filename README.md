# Atividade Cyber — Flask + CUPP

App Flask com login de dois níveis (admin/aluno), banco SQLite e demonstração
de ataque de dicionário com wordlist do CUPP.

## Como rodar
    pip install -r requirements.txt
    python init_db.py      # cria o banco (1ª vez)
    python app.py          # http://127.0.0.1:5000

## Ataque automático
Com o servidor rodando, em outro terminal:
    python brute_force.py