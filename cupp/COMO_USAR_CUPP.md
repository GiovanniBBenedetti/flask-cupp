# Gerando a wordlist com o CUPP

## Contexto (a história do cenário)

A "Escola Modelo SBC" contratou um teste de segurança na sua plataforma de
notas. Durante a fase de reconhecimento (OSINT), o pentester levantou nas
redes sociais e no site da escola os dados da administradora do sistema:

> **Maria Santos**, apelidada de "maria", nascida em **10/07/1985**.
> Casada com João, mãe da Sofia, tem uma cachorra chamada Mel e torce
> para o time do Corinthians. Costuma usar o nome com o ano de nascimento
> como senha "pra não esquecer".

O problema: a senha do painel de administrador é exatamente esse tipo de
combinação previsível — **`maria1985`** (nome + ano). Senhas assim NÃO
resistem a um ataque de dicionário, porque uma ferramenta como o CUPP
monta automaticamente todas as variações desses dados pessoais.

O objetivo desta etapa é reconstruir esse raciocínio: pegar os dados
levantados sobre a Maria e gerar uma wordlist que contenha a senha fraca.

## 1. Instalar o CUPP

No Kali Linux ele já vem instalado. Em outra distro, clone o repositório:

    git clone https://github.com/Mebus/cupp.git
    cd cupp
    python3 cupp.py -i

A flag `-i` abre o **modo interativo**, onde o CUPP faz perguntas sobre o alvo.

## 2. Respondendo o CUPP com os dados da história

Usando o perfil levantado sobre a Maria, responda assim:

    > First Name: Maria
    > Surname: Santos
    > Nickname: maria
    > Birthdate (DDMMYYYY): 10071985
    >
    > Partners) name: Joao
    > Partners) nickname: joao
    > Partners) birthdate (DDMMYYYY): 
    >
    > Child's name: Sofia
    > Pet's name: Mel
    > Company name: EscolaModelo
    >
    > Do you want to add some key words about the victim? Y
    >   > corinthians,sbc
    > Do you want to add special chars at the end of words? N
    > Do you want to add some random numbers at the end of words? N
    > Leet mode? N

## 3. O que o CUPP gera

A partir dessas respostas, o CUPP cria o arquivo **`maria.txt`** com centenas
de combinações cruzando nome, apelido, ano, pet, filho, etc. Entre elas:

    maria
    maria1985      <-- a senha do admin cai aqui
    maria85
    maria2008
    mariasantos
    mariasantos1985
    mel1985
    sofia2008
    joao1985
    ...

É por isso que o ataque funciona: a senha "pessoal e fácil de lembrar" da
Maria é justamente uma das milhares de variações que a ferramenta prevê.

## 4. Usando a wordlist no ataque

O arquivo gerado (`maria.txt`) é a entrada do `brute_force.py`. Nesta entrega
eu já deixei uma amostra representativa em **`../wordlist.txt`** (na raiz do
projeto), no mesmo formato do CUPP e contendo as senhas fracas do sistema.

> Para mostrar a ferramenta real na apresentação, basta substituir o
> `wordlist.txt` pelo `maria.txt` que o seu CUPP gerar — o script de brute
> force aceita qualquer wordlist.

## Observação ética

O CUPP e o `brute_force.py` só devem ser usados contra **sistemas próprios**
ou com **autorização explícita por escrito**. Aqui o alvo é a sua própria
aplicação Flask rodando em `127.0.0.1` (ambiente de laboratório controlado).