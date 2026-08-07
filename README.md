# Conecta Bairro

MVP inicial do aplicativo **Conecta Bairro**, desenvolvido em Python para Web com Streamlit e PostgreSQL.

## 1. Criar o banco PostgreSQL

Execute no PostgreSQL:

```sql
CREATE DATABASE conecta_bairro;
```

## 2. Configurar a conexão

Copie `.env.example` para `.env` e informe usuário, senha, host, porta e banco.

Exemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:minha_senha@localhost:5432/conecta_bairro
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 4. Criar/validar tabelas

```bash
python init_db.py
```

A aplicação também executa a criação das tabelas automaticamente ao iniciar.

## 5. Executar a página Web

```bash
streamlit run app.py
```

## Modelo inicial

### Entidades principais

- Bairro
- Morador
- Alerta de Segurança
- Anexo
- Ocorrência Urbana
- Viagem
- Apoio à Viagem
- Evento
- Participante de Evento
- Publicação/Mural
- Comentário
- Votação
- Opção de Votação
- Voto
- Agenda

### Relacionamentos principais

- Um bairro possui vários moradores.
- Um morador pertence a um bairro.
- Alertas e ocorrências pertencem a um morador e a um bairro.
- Uma viagem pertence a um morador e pode possuir vários vizinhos de apoio.
- Um evento pertence a um bairro e possui vários participantes.
- Uma publicação pertence a um bairro e a um morador e pode receber comentários.
- Uma votação pertence a um bairro, possui várias opções e recebe votos dos moradores.
- Cada morador pode votar apenas uma vez em cada votação.
- A agenda pertence ao bairro e pode ter um morador responsável pelo cadastro.

## Observação sobre anexos

A tabela `anexos` armazena metadados e o caminho do arquivo. Em uma próxima etapa, os arquivos poderão ser gravados em armazenamento local, PostgreSQL, MinIO, AWS S3 ou outro serviço.
# conecta_bairro
