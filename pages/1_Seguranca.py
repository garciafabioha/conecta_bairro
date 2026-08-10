import streamlit as st
from rodape import exibir_rodape
from datetime import datetime

from database import SessionLocal
from models import AlertaSeguranca
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.set_page_config(
    page_title="Segurança | Conecta Bairro",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 Segurança")
st.caption("Registre alertas de segurança para a comunidade.")

st.markdown("---")

with st.form("form_seguranca"):

    morador_id = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )

    tipo_alerta = st.selectbox(
        "Tipo do alerta",
        [
            "Pessoa suspeita",
            "Furto",
            "Roubo",
            "Acidente",
            "Emergência",
            "Movimentação suspeita",
            "Outro",
        ],
    )

    titulo = st.text_input(
        "Título do alerta",
        placeholder="Ex.: Motocicleta suspeita circulando pelo bairro",
    )

    descricao = st.text_area(
        "Descrição",
        placeholder="Descreva o que aconteceu...",
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

    urgencia = st.selectbox(
        "Nível de urgência",
        [
            "Baixa",
            "Média",
            "Alta",
            "Emergência",
        ],
    )

    foto = st.file_uploader(
        "Foto",
        type=["jpg", "jpeg", "png"],
    )

    compartilhar_identificacao = st.checkbox(
        "Permitir que outros moradores vejam minha identificação"
    )

    enviar = st.form_submit_button(
        "🚨 Registrar alerta",
        use_container_width=True,
    )


if enviar:

    if not titulo:
        st.warning("Informe o título do alerta.")

    elif not descricao:
        st.warning("Informe a descrição do alerta.")

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

                alerta = AlertaSeguranca(
                    morador_id=int(morador_id),
                    bairro_id=int(bairro_id),
                    tipo=tipo_alerta,
                    titulo=titulo,
                    descricao=descricao,
                    localizacao=localizacao,
                    emergencia=(urgencia == "Emergência"),
                    status="aberto",
                )

                db.add(alerta)
                db.commit()
                db.refresh(alerta)

            st.success(
                f"🚨 Alerta nº {alerta.id} registrado com sucesso!"
            )

        except Exception as exc:
            st.error("Não foi possível registrar o alerta.")
            st.exception(exc)

exibir_rodape()