import streamlit as st
import pandas as pd
import os
import base64

# --- Configurações Iniciais ---
st.set_page_config(layout="centered", page_title="Formulário de Feedback - Ômega Academy")

# Nome do arquivo da imagem e de dados
LOGO_FILE_NAME = "omega_academy.png" 
FILE_NAME = 'feedback_data.csv'

# --- Função para Salvar os Dados (Armazenamento em CSV) ---
def save_data(data):
    new_data = pd.DataFrame([data])
    
    if os.path.exists(FILE_NAME):
        existing_data = pd.read_csv(FILE_NAME)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data
        
    updated_data.to_csv(FILE_NAME, index=False)
    return True

# --- Variável de Estado para Controle do Formulário ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def form_callback():
    st.session_state.submitted = True

# --- CSS MINIMALISTA (Para garantir centralização e cor do botão) ---
st.markdown("""
<style>
.stButton>button {
    background-color: #004D99 !important; /* Azul escuro corporativo no botão */
    color: white !important;
}
/* Aumenta a margem inferior para dar mais espaço entre as perguntas */
div[data-testid="stForm"] > div > div > div:nth-child(even) {
    margin-bottom: 30px; 
}
</style>
""", unsafe_allow_html=True)
# Fim do CSS

# --- CABEÇALHO COM IMAGEM GRANDE E CENTRALIZADA ---
try:
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{base64.b64encode(open(LOGO_FILE_NAME, "rb").read()).decode()}" 
                 style="max-width: 700px; height: auto; margin: auto; display: block;">
        </div>
        """,
        unsafe_allow_html=True
    )
except Exception:
    st.warning(f"Aviso: Não foi possível carregar a imagem '{LOGO_FILE_NAME}'. Verifique o nome e o local.")


st.title("Avaliação do Evento - Ômega Academy") # H1
st.markdown("Por favor, preencha o formulário abaixo para nos ajudar a melhorar o próximo evento.")

# Lista de opções de 0 a 10 para as escalas
opcoes_escala_0_a_10 = [str(i) for i in range(11)] 

# --- Formulário Principal (st.form) ---
with st.form(key='feedback_form', clear_on_submit=True):
    # Coleta dos dados
    
    # 1. Classificação Geral
    st.subheader('De 0 a 10 como você classificaria o evento de maneira geral?') # Título simples
    classificacao_geral = st.radio(
        '1. Classificação Geral:', # Label usado para coleta de dados
        opcoes_escala_0_a_10, 
        index=None, 
        horizontal=True, 
        label_visibility="collapsed", # Oculta o label '1. Classificação Geral:'
        help="0 = Muito Ruim, 10 = Excelente"
    )
    
    # 2. Maior Impacto
    st.subheader('Qual foi o momento que MAIS te impactou no evento?') # Título simples
    momento_impacto = st.text_area(
        '2. Maior Impacto:', # Label usado para coleta de dados
        height=100, 
        placeholder="Descreva o momento, palestra ou atividade que mais chamou sua atenção."
    )
    
    # 3. Treinamento Fábio Guerreiro
    st.subheader('O treinamento com o Fábio Guerreiro (Bombril) atendeu às suas expectativas?') # Título simples
    opcoes_treinamento = ['Superou muito minhas expectativas', 'Atendeu totalmente', 'Atendeu parcialmente', 'Não atendeu', 'Não gostei']
    treinamento_fabio = st.radio(
        '3. Treinamento Fábio Guerreiro:', 
        opcoes_treinamento,
        index=None
    )
    
    # 4. Conteúdo e Metas
    st.subheader('O conteúdo da Bombril vai te ajudar a bater suas metas?') # Título simples
    opcoes_metas = ['Com certeza sim', 'Provavelmente sim', 'Talvez', 'Provavelmente não', 'Não']
    metas_bombril = st.radio(
        '4. Conteúdo e Metas:', 
        opcoes_metas,
        index=None
    )
    
    # 5. Organização Geral
    st.subheader('Como você avalia a organização geral do evento?') # Título simples
    organizacao_geral = st.radio(
        '5. Organização Geral:', 
        opcoes_escala_0_a_10, 
        index=None, 
        horizontal=True, 
        label_visibility="collapsed",
        help="0 = Muito Desorganizado, 10 = Perfeitamente Organizado"
    )
    
    # 6. Palestra Carlos Ferreira
    st.subheader('O que você achou da palestra do Carlos Ferreira?') # Título simples
    opcoes_carlos = ['Excelente', 'Muito boa', 'Boa', 'Regular', 'Fraca']
    palestra_carlos = st.radio(
        '6. Palestra Carlos Ferreira:', 
        opcoes_carlos,
        index=None
    )
    
    # 7. Tour pelo Castelão
    st.subheader('Em relação ao tour pelo Castelão, qual foi a sua experiência?') # Título simples
    opcoes_tour = ['Sensacional', 'Muito boa', 'Boa', 'Regular', 'Não gostei']
    tour_castelao = st.radio(
        '7. Tour pelo Castelão:', 
        opcoes_tour,
        index=None
    )
    
    # 8. Parceria Ômega + Bombril
    st.subheader('O que você achou da parceria Ômega + Bombril durante o evento?') # Título simples
    parceria_avaliacao = st.text_area(
        '8. Parceria Ômega + Bombril:', 
        placeholder="Avalie a sinergia e os benefícios percebidos na parceria."
    )
    
    # 9. Sugestão de Melhoria
    st.subheader('Se você pudesse destacar UMA melhoria para o próximo evento, qual seria?') # Título simples
    melhoria_proximo = st.text_area(
        '9. Sugestão de Melhoria:', 
        placeholder="Seja específico sobre o que pode ser aprimorado."
    )
    
    # 10. Mensagem Final
    st.subheader('Deixe sua mensagem final sobre o Ômega Academy. Algo marcou você?') # Título simples
    mensagem_final = st.text_area(
        '10. Mensagem Final:', 
        placeholder="Sua mensagem, agradecimento ou reflexão final."
    )
    
    st.markdown("---")
    
    submit_button = st.form_submit_button(label='Finalizar Avaliação e Enviar', on_click=form_callback)

# --- Lógica de Processamento Após o Envio ---
if st.session_state.submitted:
    # Coleta e Salva os dados
    dados = {
        "1. Classificacao Geral": classificacao_geral,
        "2. Momento de Impacto": momento_impacto,
        "3. Treinamento Fabio Guerreiro": treinamento_fabio,
        "4. Conteudo Bombril/Metas": metas_bombril,
        "5. Organizacao Geral": organizacao_geral,
        "6. Palestra Carlos Ferreira": palestra_carlos,
        "7. Tour Castelao": tour_castelao,
        "8. Avaliacao Parceria": parceria_avaliacao,
        "9. Sugestao de Melhoria": melhoria_proximo,
        "10. Mensagem Final": mensagem_final
    }
    
    save_data(dados) 
    
    st.success("🎉 Formulário enviado com sucesso! Obrigado pelo seu feedback!")
    st.balloons()
    
    st.session_state.submitted = False