import psycopg2 as ps

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

# inicia a  conexão com o banco de dados
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
