import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

show_pages(
    [   
        Page("Projeto-site/pagina_inicial.py", "Teste de caso: Red Bull Bragantino"),
        Page("Projeto-site/similaridade_jogadores.py", "Similaridade de Jogadores", "📊", in_section=True),
        Page("Projeto-site/similaridade_multiplos_jogadores.py", "Similaridade de Múltiplos Jogadores", "🧮", in_section=True),
        Page("Projeto-site/classificacao_jogadores.py", "Classificação de Jogadores", "🏆", in_section=True),
        Page("Projeto-site/dados.py", "Dados", icon="💾", in_section=False),
    ]
)

# Adicionar logo na barra lateral
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/gcarbs1/Red-Bull-Bragantino-Projeto/main/Dados/RedBullBragantino.png" alt="Imagem do Red Bull Bragantino" style="width:70%;">
    </div>
    """,
    unsafe_allow_html=True
)

# Adicionar o título à página principal
add_page_title()

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/gcarbs1/Red-Bull-Bragantino-Projeto/main/Dados/RedBullBragantino.png" alt="Imagem do Red Bull Bragantino" style="width:50%;">
    </div>
    """,
    unsafe_allow_html=True
)

# Informações de contato destacadas (com estilo customizado)
st.markdown(
    """
    <div style="background-color: #e86868; padding: 10px; border-radius: 5px; color: black;">
        <strong>Autor</strong>: Gabriel Carbinatto<br>
        <strong>Email</strong>: <a href="mailto:gabrielcarbinatto@usp.br" style="color: black;">gabrielcarbinatto@usp.br</a><br>
        <strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/gabriel-carbinatto/" style="color: black;">Gabriel Carbinatto</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background-color: #e86868; padding: 10px; border-radius: 5px; color: black;">
        Projeto com ferramentas para análise de desempenho no futebol, incluindo métricas de similaridade entre jogadores, classificação e posteriormente irei implementar algo relacionado a visualização de dados.
    </div>
    """,
    unsafe_allow_html=True
)

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
