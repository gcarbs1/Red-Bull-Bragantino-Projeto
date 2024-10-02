import streamlit as st

# Inserir o CSS diretamente no código usando st.markdown
st.markdown("""
    <style>
    /* Estilos para o bloco de informações */
    .info-box {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        font-size: 16px;
        color: #333;
    }
    .info-header {
        font-size: 20px;
        font-weight: bold;
        color: #000;
    }
    /* Estilos para botões */
    button[type=submit] {
        background-color: #af1e1e;
        color: #fedbdb;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 1.5rem;
    }

    button[type=submit]:hover {
        background-color: #d81d1d;
    }

    /* Estilo para imagens */
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# Adicionar logo com estilo centralizado
st.image("https://raw.githubusercontent.com/gcarbs1/Red-Bull-Bragantino-Projeto/main/Dados/RedBullBragantino.png")

# Adicionar o bloco de informações com o estilo personalizado
st.markdown("""
<div class="info-box">
    <p class="info-header">Autor: Gabriel Carbinatto</p>
    <p>Email: <a href="mailto:gabrielcarbinatto@usp.br">gabrielcarbinatto@usp.br</a></p>
    <p>LinkedIn: <a href="https://www.linkedin.com/in/gabriel-carbinatto/">Gabriel Carbinatto</a></p>
</div>
""", unsafe_allow_html=True)

# Outro bloco de informações
st.markdown("""
<div class="info-box">
    Projeto com ferramentas para análise de desempenho no futebol, incluindo métricas de similaridade entre jogadores, classificação e posteriormente irei implementar algo relacionado a visualização de dados.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### 📋 Sobre as ferramentas

- ⚙️ **Similaridade de Jogadores**: Compare a performance entre jogadores com base em métricas estatísticas detalhadas.
- 🧮 **Similaridade de Múltiplos Jogadores**: Compare simultaneamente o desempenho de vários jogadores.
- 🏆 **Classificação de Jogadores**: Organize e classifique jogadores de acordo com suas métricas de performance.

### 📓 Requisitos

Para tirar o máximo proveito das ferramentas, é recomendado ter conhecimentos básicos em análise de dados e familiaridade com métricas de performance no futebol.

### 👨‍🏫 Contato

Caso tenha dúvidas ou sugestões, entre em contato comigo por email ou LinkedIn.
   
""", unsafe_allow_html=True)

# Esconder o menu e o rodapé padrão do Streamlit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
