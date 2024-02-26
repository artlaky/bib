from server.server import initialize_database
from app.app import App


# iniciando o banco de dados
initialize_database()

App.add_book()

# inicilizando banco de dados e o aplicativo cli.
if __name__ == "__main__":

    initialize_database()
    App()
