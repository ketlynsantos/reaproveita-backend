# Reaproveita Backend

Backend em Python para a plataforma **Reaproveita**, responsável por:

* Gerenciar posts do blog
* Receber e salvar mensagens de contato

O servidor utiliza **HTTPServer** da biblioteca padrão do Python e conecta-se a um banco **Oracle Database** para persistência de dados.

---

## Tecnologias

* Python 3.x
* Oracle Database (via `oracledb`)
* Bibliotecas padrão: `http.server`, `json`, `smtplib` (opcional para envio de e-mails)
* `python-dotenv` para variáveis de ambiente

---

## Estrutura do projeto

```
reaproveita-backend/
│
├─ blog.py            # Funções para manipular posts do blog
├─ contact.py         # Funções para manipular formulário de contato
├─ db_connection.py   # Conexão com o banco Oracle
├─ server.py          # Servidor HTTP principal
├─ script.sql         # Script SQL para criar as tabelas
├─ .env               # Variáveis de ambiente
└─ README.md
```

---

## Configuração de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
PORT=8080

DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_DSN=host:porta/service_name

EMAIL_USER=seu_email@gmail.com        # opcional
EMAIL_PASSWORD=sua_senha              # opcional
EMAIL_TO=destinatario@gmail.com       # opcional
```

> **Nota:** O envio de e-mails não é utilizado atualmente na API principal, mas a configuração está pronta para uso futuro.

---

## Rotas da API

| Rota       | Método | Descrição                                |
| ---------- | ------ | ---------------------------------------- |
| `/blog`    | GET    | Retorna todos os posts do blog em JSON   |
| `/contact` | POST   | Recebe dados de contato e salva no banco |

### Exemplo de requisição `/contact`:

```bash
curl -X POST http://127.0.0.1:8080/contact \
  -H "Content-Type: application/json" \
  -d '{
        "name": "João Silva",
        "email": "joao@gmail.com",
        "message": "Olá, gostaria de mais informações."
      }'
```

Resposta:

```json
{
  "status": "success",
  "message": "Mensagem enviada com sucesso!"
}
```

### Exemplo de requisição `/blog`:

```bash
curl http://127.0.0.1:8080/blog
```

Resposta (exemplo resumido):

```json
[
  {
    "id": 1,
    "img": "https://link-da-imagem.jpg",
    "alt_text": "Descrição da imagem",
    "title": "Título do post",
    "description": "Resumo do post",
    "content": "Conteúdo completo do post",
    "category": "Sustentabilidade",
    "author": "Autor do post",
    "post_date": "2025-11-16",
    "read_time": "5 min"
  }
]
```

---

## Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/ketlynsantos/reaproveita-backend.git
cd reaproveita-backend
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o arquivo `.env` com suas credenciais do banco e, se desejar, informações de e-mail.

4. Execute o servidor:

```bash
python server.py
```

5. O servidor estará disponível em `http://127.0.0.1:8080`.

---

## Observações

* O servidor já permite **CORS** apenas para o frontend hospedado em `https://reaproveita-react.vercel.app`.
* As tabelas do banco devem existir com a seguinte estrutura mínima:

**Tabela CONTACTS**

* id (NUMBER, PK)
* name (VARCHAR2)
* email (VARCHAR2)
* message (CLOB)

**Tabela POSTS**

* id (NUMBER, PK)
* img (VARCHAR2)
* alt_text (VARCHAR2)
* title (VARCHAR2)
* description (VARCHAR2)
* content (CLOB)
* category (VARCHAR2)
* author (VARCHAR2)
* post_date (DATE)
* read_time (VARCHAR2)

* Para enviar e-mails, use a função `handle_contact(name, email, message)` em `contact.py`.
