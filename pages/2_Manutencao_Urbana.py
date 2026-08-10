import streamlit as st
from datetime import datetime
from rodape import exibir_rodape
from database import SessionLocal
from models import OcorrenciaUrbana
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)


st.set_page_config(
    page_title="Manutenção Urbana | Conecta Bairro",
    page_icon="🛠️",
    layout="wide",
)

st.title("🛠️ Manutenção Urbana")
st.caption("Registre problemas urbanos para acompanhamento da comunidade.")

st.markdown("---")

with st.form("form_manutencao_urbana"):

    morador_id = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )

    tipo_ocorrencia = st.selectbox(
        "Tipo do problema",
        [
            "Buraco na rua",
            "Poste apagado",
            "Falta de água",
            "Vazamento de água",
            "Lixo acumulado",
            "Árvore caída",
            "Problema em calçada",
            "Problema de sinalização",
            "Outro",
        ],
    )

    titulo = st.text_input(
        "Título da ocorrência",
        placeholder="Ex.: Poste sem iluminação na Rua Principal",
    )

    descricao = st.text_area(
        "Descrição",
        placeholder="Descreva o problema encontrado...",
        height=150,
    )

    col1, col2 = st.columns(2)

    with col1:
        endereco = st.text_input(
            "Endereço ou local"
        )

    with col2:
        referencia = st.text_input(
            "Ponto de referência"
        )

    col3, col4 = st.columns(2)

    with col3:
        data_ocorrencia = st.date_input(
            "Data",
        value=agora_brasilia.date(),
    )

    with col4:
        hora_ocorrencia = st.time_input(
        "Hora",
        value=agora_brasilia.time(),
    )

    prioridade = st.selectbox(
        "Prioridade",
        [
            "Baixa",
            "Média",
            "Alta",
            "Urgente",
        ],
    )

    # enviar_prefeitura = st.checkbox(
    #     "Solicitar encaminhamento para a prefeitura"
    # )

    foto = st.file_uploader(
        "Foto",
        type=["jpg", "jpeg", "png"],
    )

    enviar = st.form_submit_button(
        "🛠️ Registrar ocorrência",
        use_container_width=True,
    )


if enviar:

    if not titulo:
        st.warning("Informe o título da ocorrência.")

    elif not descricao:
        st.warning("Informe a descrição do problema.")

    elif not endereco:
        st.warning("Informe o endereço ou local.")

    else:
        data_hora = datetime.combine(
            data_ocorrencia,
            hora_ocorrencia,
        )

        localizacao = endereco

        if referencia:
            localizacao += f" - Referência: {referencia}"

        try:
            with SessionLocal() as db:

                ocorrencia = OcorrenciaUrbana(
                    morador_id=int(morador_id),
                    bairro_id=int(bairro_id),
                    tipo=tipo_ocorrencia,
                    descricao=descricao,
                    endereco=localizacao,
                    status="aberto",
                    #enviado_prefeitura=enviar_prefeitura,
                )

                db.add(ocorrencia)
                db.commit()
                db.refresh(ocorrencia)

            st.success(
                f"🛠️ Ocorrência nº {ocorrencia.id} registrada com sucesso!"
            )

        except Exception as exc:
            st.error("Não foi possível registrar a ocorrência.")
            st.exception(exc)

exibir_rodape()