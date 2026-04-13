import streamlit as st
import json
from groq import Groq


# Configuração da página Streamlit
st.set_page_config(page_title="EcoDescarte SP - Assistente Virtual", page_icon="♻️")
st.title("♻️ EcoDescarte SP")
st.subheader("Sua dúvida sobre como descartar lixo complexo, respondida por IA.")



# --- CONFIGURAÇÃO DA IA (GROQ) ---
# Em produção, use st.secrets para esconder a chave!
api_key = st.secrets["GROQ_API_KEY"] # Configurar no dashboard do Streamlit Cloud
client = Groq(api_key=api_key)

# --- CARREGAR BASE DE CONHECIMENTO ---
def carregar_dados():
    with open('dados_descarte.json', 'r', encoding='utf-8') as f:
        return json.load(f)

base_conhecimento = carregar_dados()
# Transforma o JSON em texto para o contexto da IA
contexto_banco = json.dumps(base_conhecimento, ensure_ascii=False)

# --- LÓGICA DO CHATBOT (O Cérebro) ---
def responder_usuario(pergunta_usuario):
    # System Prompt: Define o comportamento da IA
    system_prompt = f"""
    Você é o EcoDescarte SP, um assistente virtual especialista em educação ambiental e logística reversa em São Paulo.
    Seu objetivo é ajudar cidadãos a descartarem materiais complexos (como pneus, eletrônicos, móveis) corretamente para mitigar mudanças climáticas.
    Use APENAS as informações da 'Base de Conhecimento' abaixo para responder. Se a informação não estiver lá, diga educadamente que não sabe e sugira procurar o site da prefeitura.
    Seja curto, direto, gentil e educado.

    Base de Conhecimento:
    {contexto_banco}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pergunta_usuario},
        ],
        model="llama3-8b-8192", # Modelo rápido e gratuito da Groq
        temperature=0.5, # Menor criatividade, maior precisão
    )
    return chat_completion.choices[0].message.content

# --- INTERFACE DO USUÁRIO (STREAMLIT) ---
# Inicializa o histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Como descarto um pneu velho?"):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Consultando guia de descarte..."):
            resposta = responder_usuario(prompt)
            st.markdown(resposta)
    
    # Adiciona resposta da IA ao histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})

# Barra lateral com informações de extensão
with st.sidebar:
    st.markdown("### Sobre o Projeto")
    st.info("Este é um projeto de Extensão Universitária do curso de Ciência da Computação. O objetivo é promover a Educação Ambiental e o ODS 13 (Ação Climática).")