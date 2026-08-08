import bcrypt
import streamlit as st
from rodape import exibir_rodape

from sqlalchemy import select

from database import SessionLocal
from models import Morador

st.set_page_config(
    page_title="Login | Conecta Bairro",
    page_icon="🏘️",
    layout="centered",
)


# ---------------------------------------------------------
# Se já estiver logado, encaminha para o sistema
# ---------------------------------------------------------

if st.session_state.get("logado"):
    st.switch_page("app.py")


# ---------------------------------------------------------
# TELA
# ---------------------------------------------------------

st.title("🏘️ Conecta Bairro")

st.caption(
    "Entre com seus dados para acessar a comunidade."
)

st.markdown("---")


with st.form("form_login"):

    email = st.text_input(
        "E-mail",
        placeholder="seuemail@email.com",
    )

    senha = st.text_input(
        "Senha",
        type="password",
    )

    entrar = st.form_submit_button(
        "🔐 Entrar",
        use_container_width=True,
    )


# ---------------------------------------------------------
# AUTENTICAÇÃO
# ---------------------------------------------------------

if entrar:

    email = email.strip().lower()

    if not email:
        st.warning("Informe o e-mail.")

    elif not senha:
        st.warning("Informe a senha.")

    else:

        try:

            with SessionLocal() as db:

                morador = db.scalar(
                    select(Morador).where(
                        Morador.email == email
                    )
                )

                if morador is None:

                    st.error(
                        "E-mail ou senha inválidos."
                    )

                elif not morador.ativo:

                    st.error(
                        "Este usuário está inativo."
                    )

                elif not morador.senha_hash:

                    st.error(
                        "Este usuário ainda não possui senha cadastrada."
                    )

                else:

                    senha_correta = bcrypt.checkpw(
                        senha.encode("utf-8"),
                        morador.senha_hash.encode("utf-8"),
                    )

                    if not senha_correta:

                        st.error(
                            "E-mail ou senha inválidos."
                        )

                    else:

                        # Guarda os dados do usuário logado
                        st.session_state["logado"] = True
                        st.session_state["morador_id"] = morador.id
                        st.session_state["morador_nome"] = morador.nome
                        st.session_state["morador_email"] = morador.email

                        st.session_state["bairro_id"] = morador.bairro_id
                        st.session_state["bairro_nome"] = morador.bairro.nome

                        st.success(
                            f"Bem-vindo, {morador.nome}!"
                        )

                        st.rerun()

        except Exception as exc:

            st.error(
                "Não foi possível realizar o login. Tente novamente."
            )

            st.exception(exc)

exibir_rodape()