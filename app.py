from flask import Flask, render_template, request, redirect
import psycopg2
from babel.numbers import format_currency
import os


app = Flask(__name__)

# Conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),  # Host do banco de dados
        database=os.environ.get('DB_NAME'),  # Nome do banco de dados
        user=os.environ.get('DB_USER'),  # Nome do usuário
        password=os.environ.get('DB_PASSWORD')  # Senha
    )
    return conn

  
@app.template_filter('currency')
def currency_filter(value):
    return format_currency(value, 'BRL', locale='pt_BR')

# Inicializa o banco de dados (zera e cria as tabelas)
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Criar as tabelas
    c.execute('''
    CREATE TABLE IF NOT EXISTS contas (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS lancamentos (
        id INTEGER,
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


# Chama a função de inicialização ao iniciar a aplicação
init_db()

# Rota para a página inicial
@app.route('/')
def index():
    conn = get_db_connection()
    contas = conn.execute('SELECT * FROM contas').fetchall()
    conn.close()
    return render_template('index.html', contas=contas)

# Rota para inserir um lançamento
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        id_operacao = request.form['id']  # Captura o ID manual do formulário
        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = request.form['tipo']  # Débito ou Crédito
        conta_id = request.form['conta_id']

        conn = get_db_connection()
        conn.execute('INSERT INTO lancamentos (id, descricao, valor, tipo, conta_id) VALUES (?, ?, ?, ?, ?)',
                     (id_operacao, descricao, valor, tipo, conta_id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn = get_db_connection()
    contas = conn.execute('SELECT * FROM contas').fetchall()
    conn.close()
    return render_template('add.html', contas=contas)


@app.route('/lancamentos')
def lancamentos():
    conn = get_db_connection()
    lancamentos = conn.execute('''
        SELECT lancamentos.id, lancamentos.descricao, lancamentos.valor, lancamentos.tipo, contas.nome as conta_nome
        FROM lancamentos
        JOIN contas ON lancamentos.conta_id = contas.id
    ''').fetchall()
    conn.close()
    return render_template('lancamentos.html', lancamentos=lancamentos)


# Rota para o balancete de verificação
@app.route('/balancete')
def balancete():
    conn = get_db_connection()
    contas = conn.execute('''
        SELECT 
            contas.nome, 
            lancamentos.descricao, 
            SUM(CASE WHEN lancamentos.tipo = "debito" THEN lancamentos.valor ELSE 0 END) as debito, 
            SUM(CASE WHEN lancamentos.tipo = "credito" THEN lancamentos.valor ELSE 0 END) as credito 
        FROM lancamentos 
        JOIN contas ON lancamentos.conta_id = contas.id 
        GROUP BY contas.id, lancamentos.descricao
    ''').fetchall()
    
    # Calcular a soma total de débitos e créditos
    total_debitos = sum([conta['debito'] for conta in contas])
    total_creditos = sum([conta['credito'] for conta in contas])

    conn.close()
    return render_template('balancete.html', contas=contas, total_debitos=total_debitos, total_creditos=total_creditos)



# Rota para a Demonstração de Resultados
@app.route('/dre')
def dre():
    conn = get_db_connection()
    
    # Consulta para receitas e despesas
    receitas = conn.execute('SELECT SUM(valor) AS total FROM lancamentos WHERE conta_id = 1 AND tipo="credito"').fetchone()
    despesas = conn.execute('SELECT SUM(valor) AS total FROM lancamentos WHERE conta_id IN (2,3) AND tipo="debito"').fetchone()
    
    # Verificar se as receitas e despesas são None e substituir por 0 se necessário
    receitas_total = receitas['total'] if receitas['total'] is not None else 0
    despesas_total = despesas['total'] if despesas['total'] is not None else 0
    
    # Calcular o resultado
    resultado = receitas_total - despesas_total

    conn.close()
    return render_template('dre.html', receitas={'total': receitas_total}, despesas={'total': despesas_total}, resultado=resultado)



# Rota para o Balanço Patrimonial
@app.route('/balanco_patrimonial')
def balanco_patrimonial():
    conn = get_db_connection()

    # Consultar os totais de ativos e passivos
    ativos = conn.execute('SELECT SUM(valor) AS total FROM lancamentos WHERE conta_id = 4 AND tipo="debito"').fetchone()
    passivos = conn.execute('SELECT SUM(valor) AS total FROM lancamentos WHERE conta_id = 5 AND tipo="credito"').fetchone()
    
    # Verificar se os valores são None e substituí-los por 0, se necessário
    ativos_total = ativos['total'] if ativos['total'] is not None else 0
    passivos_total = passivos['total'] if passivos['total'] is not None else 0
    
    # Calcular o patrimônio líquido
    patrimonio = ativos_total - passivos_total

    conn.close()
    
    return render_template('balanco_patrimonial.html', ativos=ativos, passivos=passivos, patrimonio=patrimonio)
  
@app.route('/reset', methods=['POST'])
def reset():
    conn = get_db_connection()
    conn.execute('DELETE FROM lancamentos')  # Apaga todos os lançamentos
    conn.commit()
    conn.close()
    return redirect('/')
  
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    # Certifique-se de deletar pelo ID específico e talvez incluir mais critérios se necessário
    conn.execute('DELETE FROM lancamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    # Seleciona pelo ID da operação
    lancamento = conn.execute('SELECT * FROM lancamentos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = request.form['tipo']
        conta_id = request.form['conta_id']

        conn.execute('UPDATE lancamentos SET descricao = ?, valor = ?, tipo = ?, conta_id = ? WHERE id = ?',
                     (descricao, valor, tipo, conta_id, id))
        conn.commit()
        conn.close()
        return redirect('/')
    
    conn.close()
    return render_template('edit.html', lancamento=lancamento)

if __name__ == '__main__':
    app.run(debug=True)
