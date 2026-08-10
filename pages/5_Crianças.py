import streamlit as st
from datetime import datetime, date, time
from rodape import exibir_rodape
from database import SessionLocal
from models import Evento, ParticipanteEvento
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.set_page_config(
    page_title="Crianças | Conecta Bairro",
    page_icon="🧒",
    layout="wide",
)

st.title("🧒 Crianças")
st.caption(
    "Organize brincadeiras, piqueniques, atividades esportivas "
    "e ações educativas para as crianças do bairro."
)

st.markdown("---")


with st.form("form_criancas"):

    st.subheader("Dados da atividade")

    criado_por = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )
    categoria = st.selectbox(
        "Tipo de atividade",
        [
            "Brincadeiras na praça",
            "Piquenique",
            "Atividade esportiva",
            "Campanha educativa",
            "Atividade cultural",
            "Recreação",
            "Passeio",
            "Outro",
        ],
    )

    titulo = st.text_input(
        "Título da atividade",
        placeholder="Ex.: Tarde de brincadeiras na praça",
    )

    descricao = st.text_area(
        "Descrição",
        placeholder=(
            "Informe os detalhes da atividade, materiais necessários, "
            "orientações aos responsáveis etc."
        ),
        height=140,
    )

    local = st.text_input(
        "Local",
        placeholder="Ex.: Praça Central do Bairro",
    )

    st.markdown("### Data e horário")

    col3, col4 = st.columns(2)

    with col3:
        data_inicio = st.date_input(
            "Data de início",
            value=agora_brasilia.date(),
        )

        hora_inicio = st.time_input(
            "Hora de início",
            value=time(9, 0),
        )

    with col4:
        data_fim = st.date_input(
            "Data de término",
            value=agora_brasilia.date(),
        )

        hora_fim = st.time_input(
            "Hora de término",
            value=time(12, 0),
        )

    st.markdown("### Informações adicionais")

    faixa_etaria = st.selectbox(
        "Faixa etária recomendada",
        [
            "Todas as idades",
            "Até 5 anos",
            "6 a 8 anos",
            "9 a 12 anos",
            "13 anos ou mais",
        ],
    )

    acompanhamento_responsavel = st.checkbox(
        "Necessário acompanhamento de pai, mãe ou responsável",
        value=True,
    )

    adicionar_criador_como_participante = st.checkbox(
        "Adicionar o responsável pela atividade como participante",
        value=True,
    )

    enviar = st.form_submit_button(
        "🧒 Criar atividade infantil",
        use_container_width=True,
    )


if enviar:

    inicio_em = datetime.combine(
        data_inicio,
        hora_inicio,
    )

    fim_em = datetime.combine(
        data_fim,
        hora_fim,
    )

    if not titulo:
        st.warning("Informe o título da atividade.")

    elif not local:
        st.warning("Informe o local da atividade.")

    elif fim_em <= inicio_em:
        st.warning(
            "A data/hora de término deve ser posterior "
            "à data/hora de início."
        )

    else:

        descricao_completa = descricao or ""

        descricao_completa += (
            f"\n\nFaixa etária: {faixa_etaria}."
        )

        if acompanhamento_responsavel:
            descricao_completa += (
                "\nNecessário acompanhamento de responsável."
            )
        else:
            descricao_completa += (
                "\nAcompanhamento de responsável não obrigatório."
            )

        try:
            with SessionLocal() as db:

                evento = Evento(
                    bairro_id=int(bairro_id),
                    criado_por=int(criado_por),
                    categoria=categoria,
                    titulo=titulo,
                    descricao=descricao_completa,
                    local=local,
                    inicio_em=inicio_em,
                    fim_em=fim_em,

                    # Esta é a diferença principal
                    # dos eventos infantis.
                    publico_infantil=True,
                )

                db.add(evento)

                # Obter o ID antes do commit.
                db.flush()

                if adicionar_criador_como_participante:

                    participante = ParticipanteEvento(
                        evento_id=evento.id,
                        morador_id=int(criado_por),
                        status="confirmado",
                    )

                    db.add(participante)

                db.commit()

                evento_id = evento.id

            st.success(
                f"🧒 Atividade infantil nº {evento_id} "
                "criada com sucesso!"
            )

        except Exception as exc:
            st.error(
                "Não foi possível criar a atividade infantil."
            )
            st.exception(exc)

exibir_rodape()