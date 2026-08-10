import streamlit as st
from decimal import Decimal, InvalidOperation
from rodape import exibir_rodape
from database import SessionLocal
from models import Publicacao
from datetime import datetime
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.set_page_config(
    page_title="Mural Comunitário | Conecta Bairro",
    page_icon="📣",
    layout="wide",
)

st.title("📣 Mural Comunitário")
st.caption(
    "Publique avisos, itens perdidos, animais, produtos, serviços "
    "e oportunidades para os moradores do bairro."
)

st.markdown("---")


with st.form("form_mural_comunitario"):

    st.subheader("Nova publicação")

    morador_id = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )
    categoria = st.selectbox(
        "Categoria",
        [
            "Achados e perdidos",
            "Animal perdido",
            "Animal encontrado",
            "Produto para venda",
            "Produto para doação",
            "Serviço oferecido",
            "Serviço procurado",
            "Oportunidade de emprego",
            "Aviso comunitário",
            "Outro",
        ],
    )

    titulo = st.text_input(
        "Título da publicação",
        placeholder="Ex.: Cachorro perdido próximo à praça",
    )

    descricao = st.text_area(
        "Descrição",
        placeholder="Informe os detalhes da publicação...",
        height=160,
    )

    col3, col4 = st.columns(2)

    with col3:
        contato = st.text_input(
            "Contato",
            placeholder="Telefone, WhatsApp ou e-mail",
        )

    with col4:
        valor_texto = st.text_input(
            "Valor (opcional)",
            placeholder="Ex.: 150,00",
        )

    ativo = st.checkbox(
        "Publicação ativa",
        value=True,
    )

    enviar = st.form_submit_button(
        "📣 Publicar no mural",
        use_container_width=True,
    )


if enviar:

    if not titulo:
        st.warning("Informe o título da publicação.")

    elif not descricao:
        st.warning("Informe a descrição da publicação.")

    else:

        valor = None

        if valor_texto.strip():

            try:
                valor_normalizado = (
                    valor_texto
                    .replace(".", "")
                    .replace(",", ".")
                )

                valor = Decimal(valor_normalizado)

                if valor < 0:
                    st.warning("O valor não pode ser negativo.")
                    st.stop()

            except InvalidOperation:
                st.warning(
                    "Informe um valor válido. Exemplo: 150,00"
                )
                st.stop()

        try:
            with SessionLocal() as db:

                publicacao = Publicacao(
                    bairro_id=int(bairro_id),
                    morador_id=int(morador_id),
                    categoria=categoria,
                    titulo=titulo,
                    descricao=descricao,
                    valor=valor,
                    contato=contato or None,
                    ativo=ativo,
                )

                db.add(publicacao)
                db.commit()
                db.refresh(publicacao)

                publicacao_id = publicacao.id

            st.success(
                f"📣 Publicação nº {publicacao_id} criada com sucesso!"
            )

        except Exception as exc:
            st.error("Não foi possível criar a publicação.")
            st.exception(exc)

exibir_rodape()