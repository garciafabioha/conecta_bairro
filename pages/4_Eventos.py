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
    page_title="Eventos | Conecta Bairro",
    page_icon="🎉",
    layout="wide",
)

st.title("🎉 Eventos")
st.caption(
    "Organize eventos e atividades para os moradores do bairro."
)

st.markdown("---")

with st.form("form_evento"):

    st.subheader("Dados do evento")

    criado_por = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )

    categoria = st.selectbox(
        "Categoria do evento",
        [
            "Festa",
            "Campeonato esportivo",
            "Passeio ciclístico",
            "Mutirão de limpeza",
            "Reunião do bairro",
            "Atividade infantil",
            "Evento cultural",
            "Outro",
        ],
    )

    titulo = st.text_input(
        "Título do evento",
        placeholder="Ex.: Festa Junina do Bairro",
    )

    descricao = st.text_area(
        "Descrição",
        placeholder="Descreva o evento, programação e informações importantes...",
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

    publico_infantil = st.checkbox(
        "Evento destinado ou adequado ao público infantil"
    )

    adicionar_criador_como_participante = st.checkbox(
        "Adicionar o responsável como participante",
        value=True,
    )

    enviar = st.form_submit_button(
        "🎉 Criar evento",
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
        st.warning("Informe o título do evento.")

    elif not local:
        st.warning("Informe o local do evento.")

    elif fim_em <= inicio_em:
        st.warning(
            "A data/hora de término deve ser posterior à data/hora de início."
        )

    else:

        try:
            with SessionLocal() as db:

                evento = Evento(
                    bairro_id=int(bairro_id),
                    criado_por=int(criado_por),
                    categoria=categoria,
                    titulo=titulo,
                    descricao=descricao or None,
                    local=local,
                    inicio_em=inicio_em,
                    fim_em=fim_em,
                    publico_infantil=publico_infantil,
                )

                db.add(evento)
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
                f"🎉 Evento nº {evento_id} criado com sucesso!"
            )

        except Exception as exc:
            st.error("Não foi possível criar o evento.")
            st.exception(exc)

exibir_rodape()