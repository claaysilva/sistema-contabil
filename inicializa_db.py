import sqlite3

# Cria o banco de dados e as tabelas
def init_db():
    conn = sqlite3.connect('db_contabil.db')
    c = conn.cursor()

    # Cria as tabelas
    c.execute('''
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS lancamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        tipo TEXT NOT NULL,  -- 'debito' ou 'credito'
        conta_id INTEGER,
        FOREIGN KEY (conta_id) REFERENCES contas (id)
    )
    ''')

    # Inserir as contas iniciais
    c.execute('INSERT INTO contas (nome) VALUES ("Receita de Vendas"), ("Despesas Operacionais"), ("Despesas Financeiras"), ("Ativo Circulante"), ("Passivo Circulante")')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()