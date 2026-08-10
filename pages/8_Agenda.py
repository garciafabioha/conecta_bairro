import streamlit as st
from datetime import datetime, date, time
from rodape import exibir_rodape
from database import SessionLocal
from models import Agenda
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.set_page_config(
    page_title="Agenda | Conecta Bairro",
    page_icon="📅",
    layout="wide",
)

st.title("📅 Agenda")
st.caption(
    "Cadastre reuniões, vacinação, coleta de lixo, eventos "
    "e outros compromissos importantes do bairro."
)

st.markdown("---")

with st.form("form_agenda"):

    st.subheader("Novo compromisso")

    criado_por = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )
    tipo = st.selectbox(
        "Tipo de compromisso",
        [
            "Reunião do bairro",
            "Vacinação",
            "Coleta de lixo",
            "Coleta seletiva",
            "Evento comunitário",
            "Mutirão",
            "Manutenção programada",
            "Aviso público",
            "Outro",
        ],
    )

    titulo = st.text_input(
        "Título",
        placeholder="Ex.: Reunião mensal dos moradores",
    )

    descricao = st.text_area(
        "Descrição",
        placeholder="Informe os detalhes do compromisso...",
        height=140,
    )

    local = st.text_input(
        "Local",
        placeholder="Ex.: Salão comunitário",
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
            value=time(8, 0),
        )

    with col4:
        data_fim = st.date_input(
            "Data de término",
            value=agora_brasilia.date(),
        )

        hora_fim = st.time_input(
            "Hora de término",
            value=time(9, 0),
        )

    recorrencia = st.selectbox(
        "Recorrência",
        [
            "Não se repete",
            "Diária",
            "Semanal",
            "Quinzenal",
            "Mensal",
            "Anual",
        ],
    )

    enviar = st.form_submit_button(
        "📅 Adicionar à agenda",
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
        st.warning("Informe o título do compromisso.")

    elif not local:
        st.warning("Informe o local.")

    elif fim_em <= inicio_em:
        st.warning(
            "A data/hora de término deve ser posterior "
            "à data/hora de início."
        )

    else:

        try:
            with SessionLocal() as db:

                compromisso = Agenda(
                    bairro_id=int(bairro_id),
                    criado_por=int(criado_por),
                    tipo=tipo,
                    titulo=titulo,
                    descricao=descricao or None,
                    local=local,
                    inicio_em=inicio_em,
                    fim_em=fim_em,
                    recorrencia=(
                        None
                        if recorrencia == "Não se repete"
                        else recorrencia
                    ),
                )

                db.add(compromisso)
                db.commit()
                db.refresh(compromisso)

                compromisso_id = compromisso.id

            st.success(
                f"📅 Compromisso nº {compromisso_id} "
                "adicionado à agenda com sucesso!"
            )

        except Exception as exc:
            st.error(
                "Não foi possível adicionar o compromisso à agenda."
            )
            st.exception(exc)

exibir_rodape()