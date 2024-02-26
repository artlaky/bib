import typer as tp
from server.server import cone
from uuid import uuid1

b_id = str(uuid1())


class App():
    app = tp.Typer()

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


    # atualiza o nome e o author de um livro na biblioteca pelo seu id.
    @app.command(name='up', help='Update informations of a book in your library')
    def update_title(bid: str, 
                    title: str = tp.Option('', '--title', '-t', help='update the book title'), 
                    author: str = tp.Option('', '--auhtor', '-a', help='up   date the books author')):
        '''
            Update informations of a book in your library
        '''

        conn = cone()
        cur = conn.cursor()

        # update de  title 
        if title and author:
            cur.execute(
                '''
                    UPDATE books SET title=%s, author=%s WHERE id=%s
                ''', (title, author, bid)
            )
            print(f'Books title updated for { title }')
            print(f'Books autor updated for { author }')

        elif title:
            cur.execute(
                '''
                    UPDATE books SET title=%s WHERE id=%s
                ''', (title, bid)
            )
            
            print(f'Books title updated for { title }')
        elif author:
            cur.execute(
                '''
                    UPDATE books SET author=%s WHERE id=%s
                ''', (author, bid)
            )
            
            print(f'Books autor updated for { author }')

        
        
        conn.commit()
        cur.close()
        conn.close()
        

    @app.command(name='sr', help='search a book in your library by his title or author.')
    def search_book(
        title: str = tp.Option('', '--title', '-t', help='Search book from his title'),
        author: str  = tp.Option('', '--author', '-a', help='search all books of a author')
    ):
        conn = cone()
        cur = conn.cursor()

        # busca por titulo
        if title:
            cur.execute(
                f'''
                    SELECT * FROM books WHERE LOWER(title)='{title.lower()}'
                '''
            )

            response = cur.fetchall()
            if response:
                print('=-=-=-=-=- BOOKS =-=-=-=-=-')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
                for book in response:
                    bok_id, title, author, status = book
                    if status is False:
                        read_or_not = 'not read'
                    else:
                        read_or_not = 'read'
                    print(f'Id: { bok_id }')
                    print(f'Title: { title }')
                    print(f'Author: { author }')
                    print(f'READ? { read_or_not }')
                    print('--------------------------')
            else:            
                print('Book not founded in you library. Check if the title is correct')
                print('Or try add command for add this book in your library')

                App.list_books()

        # busca por author
        elif author:
            cur.execute(
                f'''
                    SELECT * FROM books WHERE LOWER(author)='{author.lower()}'
                ''', (author)
            )

            response = cur.fetchall()
            if response:
                print('=-=-=-=-=- BOOKS =-=-=-=-=-')
                print('=-=-=-=-=-=-=-=-=-=-=-=-=-=')
                for book in response:
                    bok_id, title, author, status = book
                    if status is False:
                        read_or_not = 'not read'
                    else:
                        read_or_not = 'read'
                    print(f'Id: { bok_id }')
                    print(f'Title: { title }')
                    print(f'Author: { author }')
                    print(f'READ? { read_or_not }')
                    print('--------------------------')
            else:            
                print('No books by the author was founded in your library')


        conn.commit()
        cur.close()
        conn.close()
