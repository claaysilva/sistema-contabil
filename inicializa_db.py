import psycopg2
import os

# Cria o banco de dados e as tabelas
def init_db():
    # Conexão com o banco de dados PostgreSQL
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),    # Host do banco de dados
        database=os.environ.get('DB_NAME'), # Nome do banco de dados
        user=os.environ.get('DB_USER'),     # Nome do usuário
        password=os.environ.get('DB_PASSWORD')  # Senha
    )
    c = conn.cursor()

    # Cria as tabelas
    c.execute('''
    CREATE TABLE IF NOT EXISTS contas (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS lancamentos (
        id SERIAL PRIMARY KEY,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        tipo TEXT NOT NULL,  -- 'debito' ou 'credito'
        conta_id INTEGER,
        FOREIGN KEY (conta_id) REFERENCES contas (id)
    )
    ''')

    # Inserir as contas iniciais
    c.execute('''
        INSERT INTO contas (nome) VALUES 
        ('Receita de Vendas'), 
        ('Despesas Operacionais'), 
        ('Despesas Financeiras'), 
        ('Ativo Circulante'), 
        ('Passivo Circulante') 
        ON CONFLICT (nome) DO NOTHING;
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
