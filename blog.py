from db_connection import connect_to_db


def get_all_posts():
    """
    Retorna todos os posts cadastrados no banco Oracle.
    Cada registro é convertido em um dicionário Python.
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Consulta todos os posts ordenados pela data (mais recentes primeiro)
        cursor.execute(
            """
            SELECT
                id,
                img,
                alt_text,
                title,
                description,
                content,
                category,
                author,
                TO_CHAR(post_date, 'YYYY-MM-DD') AS post_date,
                read_time
            FROM posts
            ORDER BY post_date DESC
        """
        )

        # Converte cada linha em dicionário
        columns = [col[0].lower() for col in cursor.description]
        rows = cursor.fetchall()

        posts = []
        for row in rows:
            post = {}
            for col, val in zip(columns, row):
                # Se for CLOB, converte para string
                if hasattr(val, "read"):
                    val = val.read()
                post[col] = val
            posts.append(post)

        return posts
    except Exception as error:
        print("Erro ao buscar posts:", error)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_post_by_id(post_id):
    """
    Busca um único post pelo ID.
    Retorna um dicionário com os dados ou None se não encontrado.
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                img,
                alt_text,
                title,
                description,
                content,
                category,
                author,
                TO_CHAR(post_date, 'YYYY-MM-DD') AS post_date,
                read_time
            FROM posts
            WHERE id = :id
        """,
            {"id": post_id},
        )

        row = cursor.fetchone()
        if not row:
            return None

        columns = [col[0].lower() for col in cursor.description]
        post = dict(zip(columns, row))
        return post

    except Exception as error:
        print("Erro ao buscar post por ID:", error)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_post(post):
    """
    Insere um novo post no banco de dados.
    Espera um dicionário com as mesmas chaves do JSON (img, title, etc).
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO posts (
                img, alt_text, title, description, content,
                category, author, post_date, read_time
            ) VALUES (
                :img, :alt, :title, :description, :content,
                :category, :author, TO_DATE(:post_date, 'YYYY-MM-DD'), :read_time
            )
        """,
            {
                "img": post.get("img"),
                "alt": post.get("alt"),
                "title": post.get("title"),
                "description": post.get("description"),
                "content": post.get("content"),
                "category": post.get("category"),
                "author": post.get("author"),
                "post_date": post.get("post_date"),
                "read_time": post.get("read_time"),
            },
        )

        conn.commit()
        print("Novo post inserido com sucesso!")

    except Exception as error:
        print("Erro ao inserir post:", error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
