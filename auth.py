import bcrypt
import streamlit as st


def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")

    hash_bytes = bcrypt.hashpw(
        senha_bytes,
        bcrypt.gensalt()
    )

    return hash_bytes.decode("utf-8")


def verificar_senha(
    senha: str,
    senha_hash: str
) -> bool:

    return bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash.encode("utf-8"),
    )


def registrar_sessao(
    morador_id: int,
    bairro_id: int,
    nome: str,
    email: str,
):
    st.session_state["autenticado"] = True
    st.session_state["morador_id"] = morador_id
    st.session_state["bairro_id"] = bairro_id
    st.session_state["morador_nome"] = nome
    st.session_state["morador_email"] = email


def logout():
    for chave in [
        "autenticado",
        "morador_id",
        "bairro_id",
        "morador_nome",
        "morador_email",
    ]:
        st.session_state.pop(chave, None)


def exigir_login():
    if not st.session_state.get(
        "autenticado",
        False
    ):
        st.warning(
            "Faça login para acessar esta funcionalidade."
        )

        st.page_link(
            "pages/00_Login.py",
            label="🔐 Ir para Login"
        )

        st.stop()


def morador_logado():
    return {
        "morador_id": st.session_state["morador_id"],
        "bairro_id": st.session_state["bairro_id"],
        "nome": st.session_state["morador_nome"],
        "email": st.session_state["morador_email"],
    }