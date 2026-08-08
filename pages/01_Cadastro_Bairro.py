import streamlit as st
from rodape import exibir_rodape
from sqlalchemy import select

from database import SessionLocal
from models import Bairro


st.set_page_config(
    page_title="Cadastrar Bairro | Conecta Bairro",
    page_icon="🏘️",
    layout="wide",
)

st.title("🏘️ Cadastro de Bairro")
st.caption(
    "Cadastre o bairro que utilizará o Conecta Bairro."
)

st.markdown("---")


with st.form("form_bairro"):

    nome = st.text_input(
        "Nome do bairro",
        placeholder="Ex.: Jardim Araxá"
    )

    cidade = st.text_input(
        "Cidade",
        placeholder="Ex.: Umuarama"
    )

    uf = st.text_input(
        "UF",
        max_chars=2,
        placeholder="PR"
    )

    cadastrar = st.form_submit_button(
        "🏘️ Cadastrar bairro",
        use_container_width=True,
    )


if cadastrar:

    nome = nome.strip()
    cidade = cidade.strip()
    uf = uf.strip().upper()

    if not nome:
        st.warning("Informe o nome do bairro.")

    elif not cidade:
        st.warning("Informe a cidade.")

    elif len(uf) != 2:
        st.warning("Informe a UF com 2 caracteres.")

    else:

        try:
            with SessionLocal() as db:

                existente = db.scalar(
                    select(Bairro).where(
                        Bairro.nome == nome,
                        Bairro.cidade == cidade,
                        Bairro.uf == uf,
                    )
                )

                if existente:
                    st.warning(
                        "Este bairro já está cadastrado."
                    )

                else:
                    bairro = Bairro(
                        nome=nome,
                        cidade=cidade,
                        uf=uf,
                        ativo=True,
                    )

                    db.add(bairro)
                    db.commit()
                    db.refresh(bairro)

                    st.success(
                        f"🏘️ Bairro nº {bairro.id} "
                        "Cadastrado com sucesso!"
                    )

        except Exception as exc:
            st.error(
                "Não foi possível cadastrar o bairro."
            )
            st.exception(exc)

exibir_rodape()