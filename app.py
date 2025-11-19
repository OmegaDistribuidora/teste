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
            "classificacao_geral": data.get("1"),
            "momento_impacto": data.get("2"),
            "treinamento_fabio": data.get("3"),
            "conteudo_metas": data.get("4"),
            "organizacao_geral": data.get("5"),
            "palestra_carlos": data.get("6"),
            "tour_castelao": data.get("7"),
            "avaliacao_parceria": data.get("8"),
            "sugestao_melhoria": data.get("9"),
            "mensagem_final": data.get("10"),
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

    p1 = st.radio(
        "1️ - De 0 a 10 como você classificaria o evento de maneira geral?",
        opcoes_0_a_10,
        horizontal=True,
        index=None
    )

    p2 = st.text_area(
        "2 - Qual foi o momento que MAIS te impactou no evento?",
        placeholder="Descreva o momento que mais chamou sua atenção."
    )

    p3 = st.radio(
        "3 - O treinamento com o Fábio Guerreiro (Bombril) atendeu às suas expectativas?",
        [
            "Superou muito minhas expectativas",
            "Atendeu totalmente",
            "Atendeu parcialmente",
            "Não atendeu",
            "Não gostei"
        ],
        index=None
    )

    p4 = st.radio(
        "4 - O conteúdo da Bombril vai te ajudar a bater suas metas?",
        [
            "Com certeza sim",
            "Provavelmente sim",
            "Talvez",
            "Provavelmente não",
            "Não"
        ],
        index=None
    )

    p5 = st.radio(
        "5 - Como você avalia a organização geral do evento?",
        opcoes_0_a_10,
        horizontal=True,
        index=None
    )

    p6 = st.radio(
        "6 - O que você achou da palestra do Carlos Ferreira?",
        ["Excelente", "Muito boa", "Boa", "Regular", "Fraca"],
        index=None
    )

    p7 = st.radio(
        "7 - Em relação ao tour pelo Castelão, qual foi a sua experiência?",
        ["Sensacional", "Muito boa", "Boa", "Regular", "Não gostei"],
        index=None
    )

    p8 = st.text_area(
        "8 - O que você achou da parceria Ômega + Bombril durante o evento?"
    )

    p9 = st.text_area(
        "9 - Se você pudesse destacar UMA melhoria para o próximo evento, qual seria?"
    )

    p10 = st.text_area(
        "10 - Deixe sua mensagem final sobre o Ômega Academy. Algo marcou você?"
    )

    enviado = st.form_submit_button("Enviar", on_click=form_callback)

if st.session_state.submitted:

    dados = {
        "1": p1,
        "2": p2,
        "3": p3,
        "4": p4,
        "5": p5,
        "6": p6,
        "7": p7,
        "8": p8,
        "9": p9,
        "10": p10
    }

    if save_data_to_supabase(dados):
        st.success("🎉 Feedback enviado com sucesso!")
        st.balloons()

    st.session_state.submitted = False
