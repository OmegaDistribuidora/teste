import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
import time
from sqlalchemy import text

st.set_page_config(layout="centered", page_title="Formulário de Feedback - Ômega Academy")

LOGO_FILE_NAME = "omega_academy.png"
TABLE_NAME = "feedback_omega"

SUPABASE_URL = (
    "postgresql://postgres.zxcwlfzgsuzmyhmmohsh:"
    "rhomeg%40123456712"
    "@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"
)

def initialize_database():
    try:
        conn = st.connection("supabase", type="sql", url=SUPABASE_URL)

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS public.{TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            classificacao_geral TEXT,
            momento_impacto TEXT,
            treinamento_fabio TEXT,
            conteudo_metas TEXT,
            organizacao_geral TEXT,
            palestra_carlos TEXT,
            tour_castelao TEXT,
            avaliacao_parceria TEXT,
            sugestao_melhoria TEXT,
            mensagem_final TEXT,
            timestamp TIMESTAMP WITH TIME ZONE
        );
        """

        with conn.session as session:
            session.execute(text(create_table_sql))
            session.commit()

        return True

    except Exception as e:
        st.error("❌ Falha na conexão com o Supabase.")
        st.exception(e)
        return False

if "db_initialized" not in st.session_state:
    if initialize_database():
        st.session_state.db_initialized = True
        time.sleep(0.5)
    else:
        st.session_state.db_initialized = False
        st.stop()

def save_data_to_supabase(data):
    try:
        conn = st.connection("supabase", type="sql", url=SUPABASE_URL)

        data_mapped = {
            "classificacao_geral": data.get("1. Classificacao Geral"),
            "momento_impacto": data.get("2. Momento de Impacto"),
            "treinamento_fabio": data.get("3. Treinamento Fabio Guerreiro"),
            "conteudo_metas": data.get("4. Conteudo Bombril/Metas"),
            "organizacao_geral": data.get("5. Organizacao Geral"),
            "palestra_carlos": data.get("6. Palestra Carlos Ferreira"),
            "tour_castelao": data.get("7. Tour Castelao"),
            "avaliacao_parceria": data.get("8. Avaliacao Parceria"),
            "sugestao_melhoria": data.get("9. Sugestao de Melhoria"),
            "mensagem_final": data.get("10. Mensagem Final"),
            "timestamp": datetime.now()
        }

        columns = ", ".join(data_mapped.keys())
        placeholders = ", ".join([f":{col}" for col in data_mapped.keys()])

        sql_insert = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})"

        with conn.session as session:
            session.execute(text(sql_insert), data_mapped)
            session.commit()

        return True

    except Exception as e:
        st.error("❌ Erro ao salvar os dados no Supabase.")
        st.exception(e)
        return False

if "submitted" not in st.session_state:
    st.session_state.submitted = False

def form_callback():
    st.session_state.submitted = True

try:
    with open(LOGO_FILE_NAME, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{encoded_string}" style="max-width:700px;">
        </div>
        """,
        unsafe_allow_html=True
    )
except:
    st.warning(f"❗ Não foi possível carregar a imagem '{LOGO_FILE_NAME}'.")

st.title("Avaliação do Evento - Ômega Academy")
st.write("Por favor, preencha o formulário abaixo:")

opcoes_0_a_10 = [str(i) for i in range(11)]

with st.form("feedback_form", clear_on_submit=True):

    classificacao_geral = st.radio("1. Classificação Geral", opcoes_0_a_10, horizontal=True, index=None)
    momento_impacto = st.text_area("2. Momento de Impacto")
    treinamento_fabio = st.radio(
        "3. Treinamento Fábio Guerreiro",
        ["Superou muito", "Atendeu totalmente", "Parcialmente", "Não atendeu", "Ruim"],
        index=None
    )
    metas = st.radio(
        "4. O conteúdo Bombril vai te ajudar nas metas?",
        ["Com certeza", "Provavelmente", "Talvez", "Provavelmente não", "Não"],
        index=None
    )
    organizacao = st.radio("5. Organização Geral", opcoes_0_a_10, horizontal=True, index=None)
    palestra_carlos = st.radio(
        "6. Palestra Carlos Ferreira",
        ["Excelente", "Muito boa", "Boa", "Regular", "Fraca"],
        index=None
    )
    tour = st.radio(
        "7. Tour Castelão",
        ["Sensacional", "Muito boa", "Boa", "Regular", "Não gostei"],
        index=None
    )
    parceria = st.text_area("8. Avaliação da Parceria")
    melhoria = st.text_area("9. Sugestão de Melhoria")
    mensagem = st.text_area("10. Mensagem Final")

    enviado = st.form_submit_button("Enviar", on_click=form_callback)

if st.session_state.submitted:

    dados = {
        "1. Classificacao Geral": classificacao_geral,
        "2. Momento de Impacto": momento_impacto,
        "3. Treinamento Fabio Guerreiro": treinamento_fabio,
        "4. Conteudo Bombril/Metas": metas,
        "5. Organizacao Geral": organizacao,
        "6. Palestra Carlos Ferreira": palestra_carlos,
        "7. Tour Castelao": tour,
        "8. Avaliacao Parceria": parceria,
        "9. Sugestao de Melhoria": melhoria,
        "10. Mensagem Final": mensagem
    }

    if save_data_to_supabase(dados):
        st.success("🎉 Feedback enviado com sucesso!")
        st.balloons()

    st.session_state.submitted = False
