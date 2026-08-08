import streamlit as st
from sqlalchemy import text
from database import engine
from rodape import exibir_rodape

# ---------------------------------------------------------
# CONFIGURAÇÃO GERAL
# ---------------------------------------------------------

st.set_page_config(
    page_title="Conecta Bairro",
    page_icon="🏘️",
    layout="wide",
)

# ---------------------------------------------------------
# FUNÇÃO - TESTAR CONEXÃO COM POSTGRESQL
# ---------------------------------------------------------

def testar_conexao():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return True, "PostgreSQL conectado com sucesso."

    except Exception as exc:
        return False, str(exc)


# ---------------------------------------------------------
# PÁGINA INICIAL DO CONECTA BAIRRO
# ---------------------------------------------------------

def pagina_inicio():

    # Proteção adicional
    if not st.session_state.get("logado", False):
        st.warning("Faça login para acessar o Conecta Bairro.")
        st.stop()

    # -----------------------------------------------------
    # CABEÇALHO
    # -----------------------------------------------------

    st.title("🏘️ Conecta Bairro")

    st.caption(
        "Comunidade conectada, colaborativa e mais segura."
    )

    st.write(
        f"👤 Olá, **{st.session_state['morador_nome']}**"
    )

    # -----------------------------------------------------
    # TESTE POSTGRESQL
    # -----------------------------------------------------

    ok, mensagem = testar_conexao()

    if ok:
        st.success(mensagem)
    else:
        st.error("Não foi possível conectar ao PostgreSQL.")
        st.code(mensagem)

    st.markdown("---")

    # -----------------------------------------------------
    # PRIMEIRA LINHA DE MÓDULOS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.page_link(
            "pages/1_Seguranca.py",
            label="🚨 Segurança"
        )

        st.write(
            "Alertas de suspeitos, furtos, acidentes, "
            "emergência e fotos."
        )

    with col2:

        st.page_link(
            "pages/2_Manutencao_Urbana.py",
            label="🛠️ Manutenção Urbana"
        )

        st.write(
            "Buracos, iluminação, água, vazamentos, "
            "lixo e árvores caídas."
        )

    with col3:

        st.page_link(
            "pages/3_Viagens.py",
            label="✈️ Viagens"
        )

        st.write(
            "Informe ausências e solicite apoio "
            "de vizinhos cadastrados."
        )

    with col4:

        st.page_link(
            "pages/4_Eventos.py",
            label="🎉 Eventos"
        )

        st.write(
            "Festas, esportes, passeios, mutirões "
            "e reuniões do bairro."
        )

    # -----------------------------------------------------
    # SEGUNDA LINHA DE MÓDULOS
    # -----------------------------------------------------

    col5, col6, col7, col8 = st.columns(4)

    with col5:

        st.page_link(
            "pages/5_Crianças.py",
            label="🧒 Crianças"
        )

        st.write(
            "Brincadeiras, piqueniques, esportes "
            "e campanhas educativas."
        )

    with col6:

        st.page_link(
            "pages/6_Mural_Comunitario.py",
            label="📣 Mural Comunitário"
        )

        st.write(
            "Perdidos, animais, produtos, serviços "
            "e oportunidades de emprego."
        )

    with col7:

        st.page_link(
            "pages/7_Votacoes.py",
            label="🗳️ Votações"
        )

        st.write(
            "Escolha coletiva das prioridades do bairro."
        )

    with col8:

        st.page_link(
            "pages/8_Agenda.py",
            label="📅 Agenda"
        )

        st.write(
            "Reuniões, vacinação, coleta de lixo "
            "e eventos comunitários."
        )

    st.markdown("---")

    # -----------------------------------------------------
    # INFORMAÇÕES DO USUÁRIO
    # -----------------------------------------------------

    with st.expander("👤 Minha sessão"):

        st.write(
            f"**Morador:** "
            f"{st.session_state['morador_nome']}"
        )

        st.write(
            f"**E-mail:** "
            f"{st.session_state['morador_email']}"
        )

        st.write(
            f"**Morador ID:** "
            f"{st.session_state['morador_id']}"
        )

        st.write(
            f"**Bairro ID:** "
            f"{st.session_state['bairro_id']}"
        )

        exibir_rodape()
# ---------------------------------------------------------
# DEFINIÇÃO DAS PÁGINAS DE ACESSO / CADASTRO
# ---------------------------------------------------------

pagina_login = st.Page(
    "pages/00_Login.py",
    title="Login",
    icon="🔐",
)

pagina_cadastro_bairro = st.Page(
    "pages/01_Cadastro_Bairro.py",
    title="Cadastro de Bairro",
    icon="🏘️",
)

pagina_cadastro_morador = st.Page(
    "pages/02_Cadastro_Morador.py",
    title="Cadastro de Morador",
    icon="👤",
)

# ---------------------------------------------------------
# DEFINIÇÃO DAS PÁGINAS DO CONECTA BAIRRO
# ---------------------------------------------------------

pagina_home = st.Page(
    pagina_inicio,
    title="Início",
    icon="🏠",
    default=True,
)

pagina_seguranca = st.Page(
    "pages/1_Seguranca.py",
    title="Segurança",
    icon="🚨",
)

pagina_manutencao = st.Page(
    "pages/2_Manutencao_Urbana.py",
    title="Manutenção Urbana",
    icon="🛠️",
)

pagina_viagens = st.Page(
    "pages/3_Viagens.py",
    title="Viagens",
    icon="✈️",
)

pagina_eventos = st.Page(
    "pages/4_Eventos.py",
    title="Eventos",
    icon="🎉",
)

pagina_criancas = st.Page(
    "pages/5_Crianças.py",
    title="Crianças",
    icon="🧒",
)

pagina_mural = st.Page(
    "pages/6_Mural_Comunitario.py",
    title="Mural Comunitário",
    icon="📣",
)

pagina_votacoes = st.Page(
    "pages/7_Votacoes.py",
    title="Votações",
    icon="🗳️",
)

pagina_agenda = st.Page(
    "pages/8_Agenda.py",
    title="Agenda",
    icon="📅",
)

pagina_painel = st.Page(
    "pages/9_Painel_Bairro.py",
    title="Painel do Bairro",
    icon="📊",
)

# ---------------------------------------------------------
# NAVEGAÇÃO CONFORME O LOGIN
# ---------------------------------------------------------

if st.session_state.get("logado", False):

    navegacao = st.navigation(
        {
            "🏘️ Conecta Bairro": [
                pagina_home,
                pagina_painel,
                pagina_seguranca,
                pagina_manutencao,
                pagina_viagens,
                pagina_eventos,
                pagina_criancas,
                pagina_mural,
                pagina_votacoes,
                pagina_agenda,
            ]
        }
    )

    # -----------------------------------------------------
    # USUÁRIO LOGADO NO MENU LATERAL
    # -----------------------------------------------------

    st.sidebar.markdown("---")

    st.sidebar.write(
        f"👤 **{st.session_state['morador_nome']}**"
    )

    st.sidebar.caption(
        st.session_state["morador_email"]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🚪 Sair",
        use_container_width=True,
    ):
        st.session_state.clear()
        st.rerun()

else:

    # -----------------------------------------------------
    # USUÁRIO NÃO LOGADO
    # -----------------------------------------------------

    navegacao = st.navigation(
        {
            "📝 Cadastros": [
                pagina_cadastro_bairro,
                pagina_cadastro_morador,
            ],

            "🔐 Acesso": [
                pagina_login,
            ],
        }
    )

# ---------------------------------------------------------
# EXECUTAR A PÁGINA SELECIONADA
# ---------------------------------------------------------

navegacao.run()

