import streamlit as st
from datetime import datetime

from database import SessionLocal
from models import AlertaSeguranca


st.set_page_config(
    page_title="Segurança | Conecta Bairro",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 Segurança")
st.caption("Registre alertas de segurança para a comunidade.")

st.markdown("---")


with st.form("form_seguranca"):

    col_id1, col_id2 = st.columns(2)

    with col_id1:
        morador_id = st.number_input(
            "Código do morador",
            min_value=1,
            step=1,
        )

    with col_id2:
        bairro_id = st.number_input(
            "Código do bairro",
            min_value=1,
            step=1,
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
            "Data"
        )

    with col4:
        hora_ocorrencia = st.time_input(
            "Hora"
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