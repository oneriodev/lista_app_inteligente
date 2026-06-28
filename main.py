import streamlit as st
import pandas as pd
import sqlalchemy
import datetime
import json
import time

import os
import dotenv
dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_BLOCKED = os.getenv("EMAIL_BLOCKED", "").strip().lower()

from gen_ai import generate

engine = sqlalchemy.create_engine("sqlite:///data.db")

with open("query_inteligente.sql") as query_file:
    query = query_file.read()

with open("prompt_template.md") as prompt_file:
    prompt = prompt_file.read()

with open("resposta_template.json") as resposta_file:
    resposta = json.load(resposta_file)

@st.cache_resource(ttl='10min')
def process_nf(prompt, resposta_template, produtos, img_file):
    st.image(open_img)

    prompt_exec = prompt.format(produtos="\n".join(produtos), resposta=resposta_template)
    resp = generate(prompt_exec, open_img.getvalue(), img_file.type)
    df = pd.DataFrame(json.loads(resp.text()))
    return df

def get_produtos(engine):
    try:
        query = "SELECT DISTINCT produto FROM compras"
        df = pd.read_sql_query(query, engine)
        return df["produto"].sort_values().tolist()
    except Exception as err:
        print(err)
        return []
    
def show_df_compra(df:pd.DataFrame):

    df = df.sort_values (["comprar", "dias_desde_ultima_compra"], ascending=False)
    mostrar_tudo = st.checkbox("Mostrar todos os produtos")
    if not mostrar_tudo:
        df = df[df["comprar"]]

    columns_config = {
        "produto": st.column_config.TextColumn(label="Produto"),
        "dt_ultima_compra": st.column_config.DateColumn(label="Última Compra"),
        "media_valor": st.column_config.NumberColumn(label="Valor Médio", format="R$%.2f"),
        "avg_dias_entre_compras": st.column_config.NumberColumn(label="Intervalo Entre Compras", format="%d"),
        "dias_desde_ultima_compra": st.column_config.NumberColumn(label="Dias Desde Última Compra"),
        "comprar": st.column_config.CheckboxColumn(label="Comprar?"),
    }
    st.dataframe(df, column_config=columns_config, hide_index=True)

    if df["comprar"].max() == 0:
        st.success(f"Não há produtos a serem comprados.")


st.set_page_config(page_title="Lista Inteligente")

if not st.user.is_logged_in:
    if st.button("Faça Login"):
        st.login()
    st.stop()

email_logado = st.user.email.strip().lower()

if email_logado == EMAIL_BLOCKED:
    st.warning("Este e-mail não está autorizado a acessar a aplicação.")
    st.stop()

else:
    st.markdown("# Lista Inteligente")
    produtos = get_produtos(engine)

    try:

        col, _ = st.columns(2)

        numero_dias_adiante = col.number_input("Dias se voltar ao mercado adiante",
                                            min_value=0,
                                            max_value=60,
                                            step=1)
        df_stats = pd.read_sql_query(query, engine)
        df_stats["comprar"] = df_stats["dias_desde_ultima_compra"] + numero_dias_adiante > df_stats["avg_dias_entre_compras"]

    except Exception as err:
        print(err)
        df_stats = pd.DataFrame()

    if df_stats.empty:
        st.warning("Não há dados disponíveis no banco de dados.")

    else:
        show_df_compra(df_stats)

    st.markdown("## Adicionar Compras")

    tab_produto, tab_historico, tab_nota_fiscal = st.tabs(["Adicionar Produto", "Importar Histórico", "Importar Nota Fiscal"])

    with tab_produto:

        st.markdown("### Adicionar Produto")
        produto = st.selectbox("Produto", options=["Novo Produto"]+produtos)

        if produto == "Novo Produto":
            produto_novo = st.text_input("Digite o nome do Produto")
            produto = produto_novo

        valor = st.number_input("valor", min_value=0.01)

        if st.button("Registrar Produto"):
            data = {
                "dt_compra": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "produto": produto.title(),
                "valor_produto": valor,
            }

            df_insert = pd.DataFrame([data])
            df_insert.to_sql("compras", engine, if_exists="append", index=False)
            st.success("Produto registrado com sucesso!")

    with tab_historico:
        st.markdown("### Importar Histórico")

        open_file = st.file_uploader("Anexar arquivo de histórico", type=["csv", "xlsx"])

        if open_file:
            df = pd.read_csv(open_file)
            df = st.data_editor(df)

            if st.button("Salvar Dados"):
                df.to_sql("compras", engine, if_exists="append", index=False)
                st.success("Os dados foram salvos com sucesso!")

    with tab_nota_fiscal:
        st.markdown("### Importar Nota Fiscal")

        open_img = st.file_uploader("Anexe um arquivo de Nota Fiscal", type=["png", "jpg", "jpeg", "pdf"])

        if open_img:
            df = process_nf(prompt=prompt, resposta_template=resposta, produtos=produtos, img_file=open_img)
            df = st.data_editor(df)
            if st.button("Salvar Dados"):
                df.to_sql("compras", engine, if_exists="append", index=False)
                st.success("Os dados foram salvos com sucesso!")
        
    if st.button("Log Out"):
        st.logout()
