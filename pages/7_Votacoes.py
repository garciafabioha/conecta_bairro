import streamlit as st
from datetime import datetime, date, time
from rodape import exibir_rodape
from sqlalchemy import select
from rodape import exibir_rodape
from database import SessionLocal
from models import Votacao, OpcaoVotacao, Voto
from zoneinfo import ZoneInfo

if not st.session_state.get("logado", False):
    st.warning("🔐 Faça login para acessar esta página.")
    st.stop()

agora_brasilia = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.set_page_config(
    page_title="Votações | Conecta Bairro",
    page_icon="🗳️",
    layout="wide",
)

st.title("🗳️ Votações")
st.caption(
    "Crie votações para que os moradores participem das decisões do bairro."
)

st.markdown("---")


# =========================================================
# CRIAR NOVA VOTAÇÃO
# =========================================================

st.subheader("Criar nova votação")

with st.form("form_criar_votacao"):

    criado_por = st.session_state["morador_id"]
    bairro_id = st.session_state["bairro_id"]

    st.info(
        f"👤 Morador: **{st.session_state['morador_nome']}**  |  "
        f"🏘️ Bairro: **{st.session_state['bairro_nome']}**"
    )

    pergunta = st.text_area(
        "Pergunta da votação",
        placeholder=(
            "Ex.: Qual deve ser a prioridade de melhoria "
            "para o bairro neste mês?"
        ),
        height=100,
    )

    st.markdown("### Opções de resposta")

    opcao_1 = st.text_input(
        "Opção 1",
        placeholder="Ex.: Melhorar iluminação pública",
    )

    opcao_2 = st.text_input(
        "Opção 2",
        placeholder="Ex.: Recuperar ruas com buracos",
    )

    opcao_3 = st.text_input(
        "Opção 3 (opcional)"
    )

    opcao_4 = st.text_input(
        "Opção 4 (opcional)"
    )

    st.markdown("### Período da votação")

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
            "Data de encerramento",
            value=agora_brasilia.date(),
        )

        hora_fim = st.time_input(
            "Hora de encerramento",
            value=time(18, 0),
        )

    ativa = st.checkbox(
        "Votação ativa",
        value=True,
    )

    criar = st.form_submit_button(
        "🗳️ Criar votação",
        use_container_width=True,
    )


if criar:

    inicio_em = datetime.combine(
        data_inicio,
        hora_inicio,
    )

    fim_em = datetime.combine(
        data_fim,
        hora_fim,
    )

    opcoes = [
        opcao_1.strip(),
        opcao_2.strip(),
        opcao_3.strip(),
        opcao_4.strip(),
    ]

    opcoes = [opcao for opcao in opcoes if opcao]

    if not pergunta.strip():
        st.warning("Informe a pergunta da votação.")

    elif len(opcoes) < 2:
        st.warning(
            "Informe pelo menos duas opções de resposta."
        )

    elif fim_em <= inicio_em:
        st.warning(
            "O encerramento deve ser posterior ao início da votação."
        )

    else:

        try:
            with SessionLocal() as db:

                votacao = Votacao(
                    bairro_id=int(bairro_id),
                    criado_por=int(criado_por),
                    pergunta=pergunta.strip(),
                    data_inicio=inicio_em,
                    data_fim=fim_em,
                    ativa=ativa,
                )

                db.add(votacao)
                db.flush()

                for ordem, descricao in enumerate(
                    opcoes,
                    start=1,
                ):
                    opcao = OpcaoVotacao(
                        votacao_id=votacao.id,
                        descricao=descricao,
                        ordem=ordem,
                    )

                    db.add(opcao)

                db.commit()

                votacao_id = votacao.id

            st.success(
                f"🗳️ Votação nº {votacao_id} criada com sucesso!"
            )

        except Exception as exc:
            st.error("Não foi possível criar a votação.")
            st.exception(exc)


st.markdown("---")


# =========================================================
# REGISTRAR VOTO
# =========================================================

st.subheader("Participar de uma votação")

with SessionLocal() as db:

    votacoes = db.scalars(
        select(Votacao)
        .where(Votacao.ativa.is_(True))
        .order_by(Votacao.data_fim)
    ).all()

    votacoes_disponiveis = [
        votacao
        for votacao in votacoes
        if votacao.data_inicio <= datetime.now() <= votacao.data_fim
    ]


if not votacoes_disponiveis:

    st.info(
        "Não existem votações abertas neste momento."
    )

else:

    mapa_votacoes = {
        f"{v.id} - {v.pergunta}": v.id
        for v in votacoes_disponiveis
    }

    votacao_escolhida = st.selectbox(
        "Selecione a votação",
        list(mapa_votacoes.keys()),
    )

    votacao_id = mapa_votacoes[
        votacao_escolhida
    ]

    with SessionLocal() as db:

        opcoes_votacao = db.scalars(
            select(OpcaoVotacao)
            .where(
                OpcaoVotacao.votacao_id == votacao_id
            )
            .order_by(OpcaoVotacao.ordem)
        ).all()

    mapa_opcoes = {
        opcao.descricao: opcao.id
        for opcao in opcoes_votacao
    }

    with st.form("form_votar"):

        morador_votante_id = st.number_input(
            "Código do morador",
            min_value=1,
            step=1,
        )

        resposta = st.radio(
            "Escolha uma opção",
            list(mapa_opcoes.keys()),
        )

        votar = st.form_submit_button(
            "✅ Confirmar voto",
            use_container_width=True,
        )


    if votar:

        try:
            with SessionLocal() as db:

                voto = Voto(
                    votacao_id=votacao_id,
                    opcao_id=mapa_opcoes[resposta],
                    morador_id=int(morador_votante_id),
                )

                db.add(voto)
                db.commit()

            st.success(
                "✅ Voto registrado com sucesso!"
            )

        except Exception as exc:
            st.error(
                "Não foi possível registrar o voto. "
                "Verifique se este morador já votou nesta votação."
            )
            st.exception(exc)

exibir_rodape()