import streamlit as st
from sqlalchemy import text
from database import engine
from rodape import exibir_rodape

# ---------------------------------------------------------
# PROTEÇÃO DA PÁGINA
# ---------------------------------------------------------

if not st.session_state.get("logado", False):
    st.warning("Faça login para acessar o Painel do Bairro.")
    st.stop()


# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------

st.title("📊 Painel do Bairro")

st.caption(
    "Visão consolidada das informações registradas "
    "nos bairros do Conecta Bairro."
)


# ---------------------------------------------------------
# BUSCAR BAIRROS ATIVOS
# ---------------------------------------------------------

sql_bairros = text("""
    SELECT
        id,
        nome,
        cidade,
        uf
    FROM bairros
    WHERE ativo = TRUE
    ORDER BY nome, cidade, uf
""")


try:

    with engine.connect() as conn:
        bairros = conn.execute(sql_bairros).mappings().all()

except Exception as exc:

    st.error("Não foi possível consultar os bairros.")
    st.exception(exc)
    st.stop()


# ---------------------------------------------------------
# VERIFICAR SE EXISTEM BAIRROS
# ---------------------------------------------------------

if not bairros:
    st.info("Nenhum bairro ativo foi encontrado.")
    st.stop()


# ---------------------------------------------------------
# PREPARAR LISTA DE BAIRROS
# ---------------------------------------------------------

bairro_opcoes = {
    bairro["id"]:
        f"{bairro['nome']} - "
        f"{bairro['cidade']}/{bairro['uf']}"
    for bairro in bairros
}


# ---------------------------------------------------------
# DEFINIR BAIRRO PADRÃO
# ---------------------------------------------------------

bairro_usuario = st.session_state.get("bairro_id")

ids_bairros = list(bairro_opcoes.keys())

if bairro_usuario in ids_bairros:
    indice_padrao = ids_bairros.index(bairro_usuario)
else:
    indice_padrao = 0


# ---------------------------------------------------------
# SELEÇÃO DO BAIRRO
# ---------------------------------------------------------

bairro_id = st.selectbox(
    "🏘️ Selecione o bairro",
    options=ids_bairros,
    index=indice_padrao,
    format_func=lambda id_bairro: bairro_opcoes[id_bairro],
)


st.markdown("---")


# ---------------------------------------------------------
# CONSULTAS DOS INDICADORES
# ---------------------------------------------------------

sql_indicadores = text("""
    SELECT

        (
            SELECT COUNT(*)
            FROM alertas_seguranca
            WHERE bairro_id = :bairro_id
        ) AS seguranca,

        (
            SELECT COUNT(*)
            FROM ocorrencias_urbanas
            WHERE bairro_id = :bairro_id
        ) AS manutencao,

        (
            SELECT COUNT(*)
            FROM viagens v
            INNER JOIN moradores m
                ON m.id = v.morador_id
            WHERE m.bairro_id = :bairro_id
        ) AS viagens,

        (
            SELECT COUNT(*)
            FROM eventos
            WHERE bairro_id = :bairro_id
        ) AS eventos,

        (
            SELECT COUNT(*)
            FROM eventos
            WHERE bairro_id = :bairro_id
              AND publico_infantil = TRUE
        ) AS criancas,

        (
            SELECT COUNT(*)
            FROM publicacoes
            WHERE bairro_id = :bairro_id
        ) AS mural,

        (
            SELECT COUNT(*)
            FROM votacoes
            WHERE bairro_id = :bairro_id
        ) AS votacoes,

        (
            SELECT COUNT(*)
            FROM agenda
            WHERE bairro_id = :bairro_id
        ) AS agenda
""")


try:

    with engine.connect() as conn:

        indicadores = conn.execute(
            sql_indicadores,
            {
                "bairro_id": bairro_id
            }
        ).mappings().one()

except Exception as exc:

    st.error(
        "Não foi possível consultar os indicadores "
        "do bairro."
    )

    st.exception(exc)
    st.stop()


# ---------------------------------------------------------
# NOME DO BAIRRO SELECIONADO
# ---------------------------------------------------------

st.subheader(
    f"🏘️ {bairro_opcoes[bairro_id]}"
)


# ---------------------------------------------------------
# PRIMEIRA LINHA DE INDICADORES
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🚨 Segurança",
        indicadores["seguranca"]
    )

with col2:
    st.metric(
        "🛠️ Manutenção Urbana",
        indicadores["manutencao"]
    )

with col3:
    st.metric(
        "✈️ Viagens",
        indicadores["viagens"]
    )

with col4:
    st.metric(
        "🎉 Eventos",
        indicadores["eventos"]
    )


# ---------------------------------------------------------
# SEGUNDA LINHA DE INDICADORES
# ---------------------------------------------------------

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "🧒 Crianças",
        indicadores["criancas"]
    )

with col6:
    st.metric(
        "📣 Mural Comunitário",
        indicadores["mural"]
    )

with col7:
    st.metric(
        "🗳️ Votações",
        indicadores["votacoes"]
    )

with col8:
    st.metric(
        "📅 Agenda",
        indicadores["agenda"]
    )


st.markdown("---")


# ---------------------------------------------------------
# SITUAÇÕES QUE PRECISAM DE ATENÇÃO
# ---------------------------------------------------------

st.subheader("⚠️ Situações que precisam de atenção")


sql_atencao = text("""
    SELECT

        (
            SELECT COUNT(*)
            FROM alertas_seguranca
            WHERE bairro_id = :bairro_id
              AND status = 'aberto'
        ) AS seguranca_aberta,

        (
            SELECT COUNT(*)
            FROM ocorrencias_urbanas
            WHERE bairro_id = :bairro_id
              AND status = 'aberto'
        ) AS manutencao_aberta,

        (
            SELECT COUNT(*)
            FROM viagens v
            INNER JOIN moradores m
                ON m.id = v.morador_id
            WHERE m.bairro_id = :bairro_id
              AND v.ativa = TRUE
              AND CURRENT_DATE
                  BETWEEN v.data_inicio AND v.data_fim
        ) AS viagens_ativas,

        (
            SELECT COUNT(*)
            FROM votacoes
            WHERE bairro_id = :bairro_id
              AND ativa = TRUE
              AND CURRENT_TIMESTAMP
                  BETWEEN data_inicio AND data_fim
        ) AS votacoes_ativas
""")


try:

    with engine.connect() as conn:

        atencao = conn.execute(
            sql_atencao,
            {
                "bairro_id": bairro_id
            }
        ).mappings().one()

except Exception as exc:

    st.error(
        "Não foi possível consultar as situações "
        "pendentes."
    )

    st.exception(exc)
    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🚨 Alertas abertos",
        atencao["seguranca_aberta"]
    )

with col2:
    st.metric(
        "🛠️ Manutenções abertas",
        atencao["manutencao_aberta"]
    )

with col3:
    st.metric(
        "✈️ Viagens em andamento",
        atencao["viagens_ativas"]
    )

with col4:
    st.metric(
        "🗳️ Votações ativas",
        atencao["votacoes_ativas"]
    )


st.markdown("---")


# ---------------------------------------------------------
# ÚLTIMAS ATIVIDADES DO BAIRRO
# ---------------------------------------------------------

st.subheader("🕒 Últimas atividades do bairro")


sql_atividades = text("""
    SELECT *
    FROM (

        SELECT
            criado_em AS data,
            '🚨 Segurança' AS modulo,
            titulo AS titulo,
            status AS detalhe
        FROM alertas_seguranca
        WHERE bairro_id = :bairro_id

        UNION ALL

        SELECT
            criado_em AS data,
            '🛠️ Manutenção Urbana' AS modulo,
            tipo AS titulo,
            status AS detalhe
        FROM ocorrencias_urbanas
        WHERE bairro_id = :bairro_id

        UNION ALL

        SELECT
            criado_em AS data,
            '✈️ Viagem' AS modulo,
            'Viagem cadastrada' AS titulo,
            CASE
                WHEN ativa = TRUE
                    THEN 'Ativa'
                ELSE 'Inativa'
            END AS detalhe
        FROM viagens
        WHERE morador_id IN (
            SELECT id
            FROM moradores
            WHERE bairro_id = :bairro_id
        )

        UNION ALL

        SELECT
            criado_em AS data,
            '🎉 Eventos' AS modulo,
            titulo AS titulo,
            categoria AS detalhe
        FROM eventos
        WHERE bairro_id = :bairro_id

        UNION ALL

        SELECT
            criado_em AS data,
            '📣 Mural Comunitário' AS modulo,
            titulo AS titulo,
            categoria AS detalhe
        FROM publicacoes
        WHERE bairro_id = :bairro_id

        UNION ALL

        SELECT
            data_inicio AS data,
            '🗳️ Votações' AS modulo,
            pergunta AS titulo,
            CASE
                WHEN ativa = TRUE
                    THEN 'Ativa'
                ELSE 'Encerrada'
            END AS detalhe
        FROM votacoes
        WHERE bairro_id = :bairro_id

        UNION ALL

        SELECT
            criado_em AS data,
            '📅 Agenda' AS modulo,
            titulo AS titulo,
            tipo AS detalhe
        FROM agenda
        WHERE bairro_id = :bairro_id

    ) atividades

    ORDER BY data DESC

    LIMIT 20
""")


try:

    with engine.connect() as conn:

        atividades = conn.execute(
            sql_atividades,
            {
                "bairro_id": bairro_id
            }
        ).mappings().all()

except Exception as exc:

    st.error(
        "Não foi possível consultar as últimas "
        "atividades."
    )

    st.exception(exc)
    st.stop()


# ---------------------------------------------------------
# MOSTRAR ATIVIDADES
# ---------------------------------------------------------

if atividades:

    dados = []

    for atividade in atividades:

        dados.append(
            {
                "Data": atividade["data"],
                "Módulo": atividade["modulo"],
                "Registro": atividade["titulo"],
                "Situação / Categoria":
                    atividade["detalhe"],
            }
        )

    st.dataframe(
        dados,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "Ainda não existem atividades registradas "
        "para este bairro."
    )

exibir_rodape()