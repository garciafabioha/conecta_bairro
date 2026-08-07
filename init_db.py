from database import Base, engine
import models  # noqa: F401


def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas do Conecta Bairro criadas/validadas com sucesso.")


if __name__ == "__main__":
    criar_tabelas()
