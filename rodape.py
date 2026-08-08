import streamlit as st


def exibir_rodape():

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align: center;
            font-size: 14px;
            color: #8b949e;
            line-height: 1.6;
            padding-top: 8px;
            padding-bottom: 15px;
        ">

        <strong>
            Conecta Bairro® — © 2026 Garcia Consultoria &amp; T.I LTDA.
            Todos os direitos reservados.
        </strong>

        <br><br>

        <strong>Empresa:</strong> Garcia Consultoria &amp; T.I LTDA<br>
        <strong>CNPJ:</strong> 66.495.350/0001-84<br>
        <strong>Contato:</strong>
        <a href="mailto:garciafabioha@gmail.com">
            garciafabioha@gmail.com
        </a><br>
        <strong>Celular:</strong> (44) 9 9722-0216<br>
        <strong>Cidade:</strong> Umuarama - PR

        </div>
        """,
        unsafe_allow_html=True,
    )