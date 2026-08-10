import streamlit as st
from datetime import date,datetime
from rodape import exibir_rodape
from database import SessionLocal,engine
from models import Viagem, ApoioViagem
from sqlalchemy import text
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.set_page_config(
    page_title="Viagens | Conecta Bairro",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ Viagens")
st.caption(
    "Informe o período em que estará ausente e solicite apoio de um vizinho."
)

st.markdown("---")

with st.form("form_viagens"):

    st.subheader("Dados da viagem")

    morador_id = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )

    sql_vizinhos = text("""
        SELECT
            id,
            nome
        FROM moradores
        WHERE bairro_id = :bairro_id
        AND ativo = TRUE
        AND id <> :morador_id
        ORDER BY nome
    """)

    with engine.connect() as conn:
        vizinhos = conn.execute(
            sql_vizinhos,
            {
                "bairro_id": bairro_id,
                "morador_id": morador_id,
            }
        ).mappings().all()

    if not vizinhos:
        st.warning(
            "Não existem outros moradores ativos "
            "cadastrados neste bairro para prestar apoio."
        )
        st.stop()

    opcoes_vizinhos = {
        vizinho["id"]: vizinho["nome"]
        for vizinho in vizinhos
    }

    vizinho_selecionado = st.selectbox(
        "👥 Vizinho que dará apoio",
        options=list(opcoes_vizinhos.keys()),
        format_func=lambda id_vizinho: opcoes_vizinhos[id_vizinho],
    )

    if vizinho_selecionado is None:
        st.warning("Selecione um vizinho para dar apoio.")
        st.stop()

    vizinho_id = int(vizinho_selecionado)

    col3, col4 = st.columns(2)

    with col3:
        data_inicio = st.date_input(
            "Data de saída",
            value=agora_brasilia.date(),
        )

    with col4:
        data_fim = st.date_input(
            "Data de retorno",
            value=agora_brasilia.date(),
        )

    observacoes = st.text_area(
        "Observações",
        placeholder=(
            "Ex.: Estarei viajando entre os dias 10 e 18. "
            "Caso perceba alguma movimentação estranha, por favor me avise."
        ),
        height=120,
    )

    st.markdown("### Apoio solicitado ao vizinho")

    observar_movimentacao = st.checkbox(
        "Observar movimentações estranhas"
    )

    recolher_correspondencia = st.checkbox(
        "Recolher correspondências"
    )

    avisar_ocorrencias = st.checkbox(
        "Avisar caso algo aconteça",
        value=True,
    )

    enviar = st.form_submit_button(
        "✈️ Registrar viagem",
        use_container_width=True,
    )


if enviar:

    if data_fim < data_inicio:
        st.warning(
            "A data de retorno não pode ser anterior à data de saída."
        )

    elif morador_id == vizinho_id:
        st.warning(
            "O morador e o vizinho responsável pelo apoio não podem ser a mesma pessoa."
        )

    elif not (
        observar_movimentacao
        or recolher_correspondencia
        or avisar_ocorrencias
    ):
        st.warning(
            "Selecione pelo menos uma opção de apoio para o vizinho."
        )

    else:

        try:
            with SessionLocal() as db:

                viagem = Viagem(
                    morador_id=int(morador_id),
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    observacoes=observacoes or None,
                    ativa=True,
                )

                db.add(viagem)

                # Precisamos do ID da viagem antes de criar o apoio.
                db.flush()

                apoio = ApoioViagem(
                    viagem_id=viagem.id,
                    vizinho_id=int(vizinho_id),
                    observar_movimentacao=observar_movimentacao,
                    recolher_correspondencia=recolher_correspondencia,
                    avisar_ocorrencias=avisar_ocorrencias,
                    confirmado=False,
                )

                db.add(apoio)
                db.commit()

                viagem_id = viagem.id

            st.success(
                f"✈️ Viagem nº {viagem_id} registrada com sucesso!"
            )

            st.info(
                "O apoio do vizinho foi registrado como pendente de confirmação."
            )

        except Exception as exc:
            st.error("Não foi possível registrar a viagem.")
            st.exception(exc)

exibir_rodape()