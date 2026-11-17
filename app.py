import sqlite3
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, abort,
)
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "chave-secreta-da-atividade-cyber"
DB = "escola.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)  # aluno tentando area de admin
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("admin" if session["role"] == "admin" else "aluno"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        senha = request.form.get("senha", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM usuarios WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["senha"], senha):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["aluno_id"] = user["aluno_id"]
            return redirect(url_for("admin" if user["role"] == "admin" else "aluno"))

        flash("Usuario ou senha invalidos.", "erro")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
@admin_required
def admin():
    conn = get_db()
    alunos = conn.execute("SELECT * FROM alunos ORDER BY nome").fetchall()
    dados = []
    for aluno in alunos:
        notas = conn.execute(
            "SELECT * FROM notas WHERE aluno_id = ? ORDER BY materia", (aluno["id"],)
        ).fetchall()
        dados.append({"aluno": aluno, "notas": notas})
    conn.close()
    return render_template("admin.html", dados=dados, usuario=session["username"])


@app.route("/admin/nota/<int:nota_id>", methods=["POST"])
@login_required
@admin_required
def atualizar_nota(nota_id):
    try:
        nova_nota = float(request.form.get("nota", ""))
    except ValueError:
        flash("Nota invalida. Use um numero (ex: 7.5).", "erro")
        return redirect(url_for("admin"))

    if not (0 <= nova_nota <= 10):
        flash("A nota precisa estar entre 0 e 10.", "erro")
        return redirect(url_for("admin"))

    conn = get_db()
    conn.execute("UPDATE notas SET nota = ? WHERE id = ?", (nova_nota, nota_id))
    conn.commit()
    conn.close()
    flash("Nota atualizada com sucesso.", "ok")
    return redirect(url_for("admin"))


@app.route("/aluno")
@login_required
def aluno():
    if session["role"] == "admin":
        return redirect(url_for("admin"))

    conn = get_db()
    aluno = conn.execute(
        "SELECT * FROM alunos WHERE id = ?", (session["aluno_id"],)
    ).fetchone()
    notas = conn.execute(
        "SELECT * FROM notas WHERE aluno_id = ? ORDER BY materia", (session["aluno_id"],)
    ).fetchall()
    conn.close()
    # Tela SOMENTE LEITURA: nao existe rota de alteracao para o aluno.
    return render_template("aluno.html", aluno=aluno, notas=notas)


@app.errorhandler(403)
def proibido(_e):
    return render_template(
        "login.html", bloqueio="Acesso negado: area restrita ao administrador."
    ), 403


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)