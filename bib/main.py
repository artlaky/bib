import psycopg2 as ps
import typer as tp
from uuid import uuid1

# TODO:  estruturação de código

# conexão com o banco de dados
def cone():
    '''
        Start the conection with postgress database
    '''
    conn = ps.connect(host='localhost',
                    dbname='postgres',
                    user='postgres',
                    password='Lucaskaua-10',
                    port=5432)

    return conn


# criando tabela no banco de dados.
def initialize_database():
    '''
        Initialize the postgresql database
    '''
    conn = ps.connect(host='localhost',
                    dbname='postgres',
                    user='postgres',
                    password='Lucaskaua-10',
                    port=5432)

    cur = conn.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            status BOOLEAN
        );
        '''
)

    conn.commit()
    cur.close()
    conn.close()



app = tp.Typer()
b_id = str(uuid1())


# adiciono um livro ao banco de dados com um id aleatório
@app.command(name='add', help='add a book into the library')
def add_book(title:str, author:str):

    '''
        add a book into the library
    '''
    global bid

    bid = str(uuid1())
    conn = cone()

    cur = conn.cursor()

    cur.execute(
        '''
            INSERT INTO books (id, title, author, status) VALUES (%s, %s, %s, %s)
        ''',(bid, title, author, False)
    )


    conn.commit()
    cur.close()
    conn.close()

    tp.echo(f'book { title } added into your library')


# removo um livro do bando de dados apartir do id criado
@app.command(name='rm', help='Delete a book from the library')
def delete_boook(boid: str):
    '''
        Delete a book from the library
    '''
    conn = cone()
    cur = conn.cursor()

    cur.execute(
        '''
            DELETE FROM books WHERE id=%s
        ''', (boid, )
    )

    conn.commit()
    cur.close()
    conn.close()

    print('book removed from your library')


# Listo todos os livros que estão armazenados no meu banco de dados
@app.command(name='ls', help='List all the books that you have in your library')
def list_books():
    '''
        List all the books that you have in your library
    '''
    conn = cone()
    cur = conn.cursor()

    cur.execute(
        '''
            SELECT * FROM books
        '''
    )

    books = cur.fetchall()
    if books:
        print('=-=-=-=-=- BOOKS =-=-=-=-=-')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        for b in books:
            bok_id, title, author, status = b
            if status is False:
                read_or_not = 'not read'
            else:
                read_or_not = 'read'
            print(f'Id: { bok_id }')
            print(f'Title: { title }')
            print(f'Author: { author }')
            print(f'READ? { read_or_not }')
            print('--------------------------')

    conn.commit()
    cur.close()
    conn.close()


# Marco um livro como lido no banco de dados, i.e atualizo o valor de false para true
@app.command(name='read', help='mark a book in your library as read')
def read_book(title: str):
    '''
        mark a book in your library as read
    '''
    conn = cone()
    cur = conn.cursor()

    cur.execute(
        '''
            UPDATE books SET title=%s, status=true WHERE title=%s AND status=false
        ''', (title, title)
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f'book { title } is now Readed')


# inicilizando banco de dados e o aplicativo cli.
if __name__ == "__main__":
    initialize_database()
    app()
