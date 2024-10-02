import streamlit as st

# Adicionando CSS para justificar o texto
st.markdown("""
    <style>
    .justificado {
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="justificado">

## 💾 Dados de Futebol Obtidos via Web Scraping

Os dados utilizados neste projeto foram obtidos por meio de scraping em fontes confiáveis e amplamente reconhecidas na área de estatísticas esportivas. A coleta dos dados visa enriquecer as análises e proporcionar uma visão mais aprofundada das métricas relacionadas ao desempenho dos jogadores e equipes de futebol. As fontes de onde os dados foram extraídos incluem:

* [FBref](https://fbref.com/pt/) — Um dos principais bancos de dados de estatísticas de futebol, oferecendo métricas detalhadas sobre desempenho individual e de equipe.
* [Fotmob](https://www.fotmob.com/pt-BR) — Plataforma amplamente utilizada para estatísticas de futebol em tempo real, com dados sobre jogos, jogadores e campeonatos ao redor do mundo.
* [WhoScored](https://1xbet.whoscored.com/) — Site conhecido por suas análises detalhadas de jogos e estatísticas avançadas, com foco em avaliações de desempenho baseadas em dados objetivos.
* [SofaScore](https://www.sofascore.com/) — Oferece dados em tempo real, estatísticas de jogadores e times, além de classificações e gráficos de desempenho.
* [Transfermarkt](https://www.transfermarkt.com.br/) — Fonte de informações sobre valores de mercado de jogadores, transferências, histórico de jogos e dados de desempenho.

A metodologia de scraping respeita os termos de uso de cada site, e os dados são processados e normalizados para garantir a integridade e qualidade das análises subsequentes.

---

### Observações

Este projeto visa o uso educativo e analítico dos dados, respeitando as políticas de uso de dados e scraping de cada fonte. As métricas extraídas são transformadas e organizadas para facilitar a análise estatística e a visualização dos resultados, oferecendo insights relevantes no campo da ciência esportiva.

</div>
""", unsafe_allow_html=True)
