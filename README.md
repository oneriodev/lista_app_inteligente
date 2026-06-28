# 🛒 Lista Inteligente de Compras com IA

Uma aplicação web desenvolvida com **Streamlit**, **SQLite** e **Google Gemini**, capaz de analisar o histórico de compras do usuário, sugerir automaticamente os produtos que precisam ser comprados e importar notas fiscais utilizando Inteligência Artificial.

---

## 📌 Sobre o Projeto

O objetivo deste projeto é automatizar o gerenciamento de compras domésticas.

A aplicação registra o histórico de compras, calcula a frequência média de aquisição de cada produto e informa quais itens provavelmente precisam ser comprados novamente.

Além disso, o sistema utiliza o modelo **Gemini 3.1 Flash Lite** para extrair automaticamente informações de notas fiscais em formatos **PDF**, **PNG** e **JPG**, eliminando a necessidade de digitação manual.

---

# Funcionalidades

* Login com conta Google
* Controle de acesso por e-mail
* Cadastro manual de produtos
* Importação de histórico via CSV
* Importação automática de notas fiscais com IA
* Armazenamento em SQLite
* Sugestão inteligente de compras baseada no histórico
* Interface web desenvolvida com Streamlit

---

# Tecnologias Utilizadas

* Python
* Streamlit
* Pandas
* SQLAlchemy
* SQLite
* Google Gemini API
* Google AI Studio
* Google Cloud
* VS Code

---

# Arquitetura

```
Usuário
    │
    ▼
Streamlit
    │
    ├──────── Cadastro Manual
    │
    ├──────── Importação CSV
    │
    └──────── Nota Fiscal
                 │
                 ▼
          Google Gemini
                 │
                 ▼
         JSON Estruturado
                 │
                 ▼
             SQLite
                 │
                 ▼
       Consulta SQL Inteligente
                 │
                 ▼
      Sugestão de Compras
```

---

# Estrutura do Projeto

```
📦 lista-inteligente
│
├── main.py
├── gen_ai.py
├── query_inteligente.sql
├── prompt_template.md
├── resposta_template.json
├── requirements.txt
├── data.db
├── .env
└── README.md
```

---

# Funcionamento

## Cadastro Manual

Permite adicionar novos produtos manualmente.

---

## Importação de Histórico

Permite importar arquivos CSV contendo o histórico de compras.

Exemplo:

```csv
dt_compra,produto,valor_produto
2025-01-05,Arroz,29.90
```

---

## Importação Inteligente de Nota Fiscal

O usuário envia uma imagem ou PDF da nota fiscal.

A aplicação envia o documento para o modelo Gemini, que extrai automaticamente:

* Produto
* Valor unitário
* Data da compra

A resposta é recebida em JSON e apresentada ao usuário para conferência antes da gravação no banco.

---

# Inteligência da Aplicação

A consulta SQL calcula automaticamente:

* último dia de compra
* média de preço
* intervalo médio entre compras
* dias desde a última compra

Com essas informações, o sistema estima quais produtos provavelmente precisam ser comprados novamente.

---

# Segurança

As informações sensíveis são armazenadas em variáveis de ambiente.

```
.env
```

Exemplo:

```
GEMINI_API_KEY=xxxxxxxxxxxxxxxx
EMAIL_BLOCKED=email@gmail.com
```

Esse arquivo não deve ser publicado no GitHub.

---

# Como Executar

Clone o projeto

```bash
git clone https://github.com/seuusuario/lista-inteligente.git
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env`

Execute

```bash
streamlit run main.py
```

---

# Melhorias Futuras

* Dashboard de gastos
* Evolução de preços
* Comparação entre supermercados
* Histórico por categoria
* Alertas de inflação
* Exportação para Excel
* Aplicativo Mobile
* Login multiusuário
* Banco PostgreSQL
* Deploy em Streamlit Community Cloud

---

# Autor

**Onerio Ramos**

Estudante de Matemática • Ciência de Dados • Inteligência Artificial

LinkedIn: *(adicione seu perfil)*

GitHub: *(adicione seu perfil)*
