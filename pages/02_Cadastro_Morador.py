import streamlit as st
from rodape import exibir_rodape
from sqlalchemy import select

from auth import gerar_hash_senha
from database import SessionLocal
from models import Bairro, Morador


st.set_page_config(
    page_title="Cadastrar Morador | Conecta Bairro",
    page_icon="👤",
    layout="wide",
)

st.title("👤 Cadastro de Morador")
st.caption(
    "Crie sua conta para participar da comunidade."
)

st.markdown("---")

with SessionLocal() as db:
    bairros = db.scalars(
        select(Bairro)
        .where(Bairro.ativo.is_(True))
        .order_by(Bairro.nome)
    ).all()


if not bairros:

    st.warning(
        "Nenhum bairro foi cadastrado ainda."
    )

    st.page_link(
        "pages/01_Cadastro_Bairro.py",
        label="🏘️ Cadastrar primeiro bairro"
    )

    st.stop()


mapa_bairros = {
    f"{b.nome} - {b.cidade}/{b.uf}": b.id
    for b in bairros
}


with st.form("form_morador"):

    bairro_selecionado = st.selectbox(
        "Bairro",
        list(mapa_bairros.keys()),
    )

    nome = st.text_input(
        "Nome completo"
    )

    email = st.text_input(
        "E-mail"
    )

    telefone = st.text_input(
        "Telefone / WhatsApp"
    )

    col1, col2 = st.columns([4, 1])

    with col1:
        endereco = st.text_input(
            "Endereço"
        )

    with col2:
        numero = st.text_input(
            "Número"
        )

    senha = st.text_input(
        "Senha",
        type="password",
    )

    confirmar_senha = st.text_input(
        "Confirmar senha",
        type="password",
    )

    cadastrar = st.form_submit_button(
        "👤 Criar minha conta",
        use_container_width=True,
    )


if cadastrar:

    email = email.strip().lower()

    if not nome.strip():
        st.warning("Informe seu nome.")

    elif not email:
        st.warning("Informe seu e-mail.")

    elif len(senha) < 6:
        st.warning(
            "A senha deve possuir pelo menos 6 caracteres."
        )

    elif senha != confirmar_senha:
        st.warning(
            "As senhas informadas são diferentes."
        )

    else:

        try:
            with SessionLocal() as db:

                morador = Morador(
                    bairro_id=mapa_bairros[bairro_selecionado],
                    nome=nome.strip(),
                    email=email,
                    telefone=telefone.strip() or None,
                    endereco=endereco.strip() or None,
                    numero=numero.strip() or None,
                    senha_hash=gerar_hash_senha(senha),
                    ativo=True,
                )

                db.add(morador)
                db.commit()
                db.refresh(morador)

            st.success(
                f"👤 Morador {morador.nome} cadastrado com sucesso!"
            )

        except Exception as exc:
            st.error("Não foi possível cadastrar o morador.")
            st.exception(exc)

exibir_rodape()