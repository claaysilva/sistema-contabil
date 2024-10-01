from flask import Flask, render_template, request, redirect, url_for
from babel.numbers import format_currency

app = Flask(__name__)

# Adicionar o filtro 'currency' para formatar os valores monetários
@app.template_filter('currency')
def currency_filter(value):
    return format_currency(value, 'BRL', locale='pt_BR')

# Variáveis globais para armazenar dados temporários
contas = [
    {"id": 1, "nome": "Receita de Vendas"},
    {"id": 2, "nome": "Despesas Operacionais"},
    {"id": 3, "nome": "Despesas Financeiras"},
    {"id": 4, "nome": "Ativo Circulante"},
    {"id": 5, "nome": "Passivo Circulante"},
    {"id": 6, "nome": "Ativo Não Circulante"},
    {"id": 7, "nome": "Passivo Não Circulante"},
    {"id": 8, "nome": "Patrimônio Líquido"}
]

lancamentos = []  # Lista para armazenar lançamentos temporários

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        tipo = request.form['tipo']  # 'debito' ou 'credito'
        conta_id = int(request.form['conta_id'])

        # Adicionar o lançamento na lista temporária com ID único
        lancamento_id = len(lancamentos) + 1
        lancamento = {"id": lancamento_id, "descricao": descricao, "valor": valor, "tipo": tipo, "conta_id": conta_id}
        lancamentos.append(lancamento)
        return redirect('/lancamentos')

    # Separar as contas em categorias
    contas_ativos = [c for c in contas if c['nome'] in ["Ativo Circulante", "Ativo Não Circulante"]]
    contas_passivos = [c for c in contas if c['nome'] in ["Passivo Circulante", "Passivo Não Circulante"]]
    contas_receitas = [c for c in contas if c['nome'] == "Receita de Vendas"]
    contas_despesas = [c for c in contas if c['nome'] in ["Despesas Operacionais", "Despesas Financeiras"]]

    return render_template('add.html', contas_ativos=contas_ativos, contas_passivos=contas_passivos, contas_receitas=contas_receitas, contas_despesas=contas_despesas)

@app.route('/lancamentos')
def lista_lancamentos():
    return render_template('lancamentos.html', lancamentos=lancamentos, contas=contas)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Encontrar o lançamento pelo ID
    lancamento = next((l for l in lancamentos if l['id'] == id), None)

    if not lancamento:
        return "Lançamento não encontrado", 404

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        tipo = request.form['tipo']
        conta_id = int(request.form['conta_id'])

        # Atualizar os dados do lançamento
        lancamento['descricao'] = descricao
        lancamento['valor'] = valor
        lancamento['tipo'] = tipo
        lancamento['conta_id'] = conta_id

        return redirect('/lancamentos')

    return render_template('edit.html', lancamento=lancamento, contas=contas)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    global lancamentos
    # Remover o lançamento pelo ID
    lancamentos = [l for l in lancamentos if l['id'] != id]
    return redirect('/lancamentos')

@app.route('/balancete')
def balancete():
    # Calcular débitos e créditos por descrição
    balancete_data = {}
    
    for lancamento in lancamentos:
        descricao = lancamento["descricao"]
        if descricao not in balancete_data:
            balancete_data[descricao] = {"debito": 0, "credito": 0}
        
        if lancamento["tipo"] == "debito":
            balancete_data[descricao]["debito"] += lancamento["valor"]
        else:
            balancete_data[descricao]["credito"] += lancamento["valor"]

    # Transformar o dicionário em uma lista para fácil manipulação no template
    balancete_list = [{"descricao": desc, **values} for desc, values in balancete_data.items()]

    return render_template('balancete.html', contas=balancete_list)

@app.route('/dre')
def dre():
    receitas_total = 0
    despesas_total = 0

    # Calcular total de receitas
    for lancamento in lancamentos:
        if lancamento['tipo'] == 'credito' and lancamento['conta_id'] == 1:  # Receita de Vendas
            receitas_total += lancamento['valor']
    
    # Calcular total de despesas
    for lancamento in lancamentos:
        if lancamento['tipo'] == 'debito':
            if lancamento['conta_id'] == 2:  # Despesas Operacionais
                despesas_total += lancamento['valor']
            elif lancamento['conta_id'] == 3:  # Despesas Financeiras
                despesas_total += lancamento['valor']

    # Calcular o resultado
    resultado = receitas_total - despesas_total

    return render_template('dre.html', receitas={'total': receitas_total}, despesas={'total': despesas_total}, resultado=resultado)

@app.route('/balanco_patrimonial')
def balanco_patrimonial():
    # Calcular totais de ativos circulantes e não circulantes
    ativo_circulante_total = sum([lanc["valor"] for lanc in lancamentos if lanc["conta_id"] == 4 and lanc["tipo"] == "debito"])
    ativo_nao_circulante_total = sum([lanc["valor"] for lanc in lancamentos if lanc["conta_id"] == 6 and lanc["tipo"] == "debito"])
    
    # Calcular totais de passivos circulantes, não circulantes e patrimônio líquido
    passivo_circulante_total = sum([lanc["valor"] for lanc in lancamentos if lanc["conta_id"] == 5 and lanc["tipo"] == "credito"])
    passivo_nao_circulante_total = sum([lanc["valor"] for lanc in lancamentos if lanc["conta_id"] == 7 and lanc["tipo"] == "credito"])
    patrimonio_liquido_total = sum([lanc["valor"] for lanc in lancamentos if lanc["conta_id"] == 8 and lanc["tipo"] == "credito"])

    # Calcular totais finais
    total_ativos = ativo_circulante_total + ativo_nao_circulante_total
    total_passivos = passivo_circulante_total + passivo_nao_circulante_total + patrimonio_liquido_total

    return render_template('balanco_patrimonial.html', 
                           ativo_circulante=ativo_circulante_total, 
                           ativo_nao_circulante=ativo_nao_circulante_total, 
                           passivo_circulante=passivo_circulante_total, 
                           passivo_nao_circulante=passivo_nao_circulante_total, 
                           patrimonio_liquido=patrimonio_liquido_total,
                           total_ativos=total_ativos, 
                           total_passivos=total_passivos)

@app.route('/reset', methods=['POST'])
def reset():
    global lancamentos
    lancamentos = []  # Zera a lista de lançamentos
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
