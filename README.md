# Sistema Contábil com Flask

## Descrição

Este é um sistema contábil desenvolvido para facilitar a gestão financeira de pequenas empresas. Ele permite a inclusão de lançamentos contábeis e gera automaticamente relatórios financeiros, como o **Balancete de Verificação**, a **Demonstração do Resultado do Exercício (DRE)** e o **Balanço Patrimonial**. O sistema foi desenvolvido utilizando **Python** com **Flask** e uma interface minimalista e responsiva com **HTML/CSS**.

## Funcionalidades

- **Cadastro de Lançamentos Contábeis**: Inclua, edite e exclua lançamentos contábeis com descrição, valor, tipo e conta.
- **Relatórios Financeiros**:
  - Balancete de Verificação
  - Demonstração do Resultado do Exercício (DRE)
  - Balanço Patrimonial
- **Design Responsivo**: Interface adaptável para web e dispositivos móveis.

## Tecnologias Utilizadas

- **Flask**: Framework para desenvolvimento web em Python.
- **HTML/CSS**: Estrutura e estilo da interface do usuário.
- **JavaScript**: Interatividade na aplicação.
- **Python**: Linguagem de programação principal do projeto.

## Como Executar o Projeto

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/seu_usuario/sistema-contabil.git
   ```

2. Navegue até a pasta do projeto:

   ```bash
   cd sistema-contabil
   ```

3. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv env
   ```

4. Ative o ambiente virtual:

   - No Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - No macOS/Linux:

     ```bash
     source env/bin/activate
     ```

5. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

6. Execute o script `app.py`:

   ```bash
   python app.py
   ```

7. Acesse o sistema no navegador através do endereço:

   ```
   http://127.0.0.1:5000/
   ```

## Estrutura do Projeto

sistema-contabil/
├── app.py # Código principal da aplicação Flask
├── templates/ # Templates HTML para renderização
│ ├── index.html # Página inicial do sistema
│ ├── add.html # Página para adicionar lançamentos
│ ├── balancete.html # Página do Balancete de Verificação
│ ├── dre.html # Página da Demonstração do Resultado do Exercício
│ ├── balanco_patrimonial.html # Página do Balanço Patrimonial
│ └── edit.html # Página para editar lançamentos
├── static/ # Arquivos estáticos como CSS e JavaScript
│ └── css/ # Pasta de estilos CSS
│ └── style.css # Arquivo de estilos CSS
├── db_contabil.db # Banco de dados SQLite (pode ser excluído se não necessário)
├── README.md # Documentação do projeto
└── .gitignore # Arquivos e pastas ignorados pelo Git

## Melhorias Futuras

- Implementar autenticação de usuários para permitir múltiplos usuários acessando o sistema.
- Adicionar gráficos para melhor visualização dos relatórios financeiros.
- Implementar suporte a exportação dos relatórios em PDF ou Excel.

## Contribuição

Sinta-se à vontade para contribuir com melhorias para o projeto. Faça um **fork** do repositório, crie um novo branch e envie um **pull request** com suas alterações!

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.
