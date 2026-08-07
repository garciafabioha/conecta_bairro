from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Bairro(Base):
    __tablename__ = "bairros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    cidade: Mapped[str] = mapped_column(String(120), nullable=False)
    uf: Mapped[str] = mapped_column(String(2), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    moradores = relationship("Morador", back_populates="bairro")

    __table_args__ = (UniqueConstraint("nome", "cidade", "uf", name="uq_bairro_localidade"),)


class Morador(Base):
    __tablename__ = "moradores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="RESTRICT"), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(30))
    endereco: Mapped[str | None] = mapped_column(String(220))
    numero: Mapped[str | None] = mapped_column(String(20))
    senha_hash: Mapped[str | None] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    bairro = relationship("Bairro", back_populates="moradores")


class AlertaSeguranca(Base):
    __tablename__ = "alertas_seguranca"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False)  # suspeito, furto, acidente, emergencia
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    localizacao: Mapped[str | None] = mapped_column(String(220))
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    emergencia: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="aberto", nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Anexo(Base):
    __tablename__ = "anexos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False)
    entidade: Mapped[str] = mapped_column(String(40), nullable=False)
    entidade_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    caminho_arquivo: Mapped[str] = mapped_column(String(500), nullable=False)
    tipo_mime: Mapped[str | None] = mapped_column(String(100))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class OcorrenciaUrbana(Base):
    __tablename__ = "ocorrencias_urbanas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    endereco: Mapped[str | None] = mapped_column(String(220))
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    status: Mapped[str] = mapped_column(String(30), default="aberto", nullable=False)
    protocolo_prefeitura: Mapped[str | None] = mapped_column(String(100))
    enviado_prefeitura: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Viagem(Base):
    __tablename__ = "viagens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date] = mapped_column(Date, nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ApoioViagem(Base):
    __tablename__ = "apoios_viagem"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    viagem_id: Mapped[int] = mapped_column(ForeignKey("viagens.id", ondelete="CASCADE"), nullable=False, index=True)
    vizinho_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    observar_movimentacao: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recolher_correspondencia: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avisar_ocorrencias: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    confirmado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (UniqueConstraint("viagem_id", "vizinho_id", name="uq_viagem_vizinho"),)


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="CASCADE"), nullable=False, index=True)
    criado_por: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    titulo: Mapped[str] = mapped_column(String(160), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    local: Mapped[str | None] = mapped_column(String(220))
    inicio_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fim_em: Mapped[datetime | None] = mapped_column(DateTime)
    publico_infantil: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ParticipanteEvento(Base):
    __tablename__ = "participantes_evento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False, index=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="confirmado", nullable=False)

    __table_args__ = (UniqueConstraint("evento_id", "morador_id", name="uq_evento_morador"),)


class Publicacao(Base):
    __tablename__ = "publicacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="CASCADE"), nullable=False, index=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    titulo: Mapped[str] = mapped_column(String(160), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    valor: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    contato: Mapped[str | None] = mapped_column(String(120))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ComentarioPublicacao(Base):
    __tablename__ = "comentarios_publicacao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    publicacao_id: Mapped[int] = mapped_column(ForeignKey("publicacoes.id", ondelete="CASCADE"), nullable=False, index=True)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False)
    comentario: Mapped[str] = mapped_column(Text, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Votacao(Base):
    __tablename__ = "votacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="CASCADE"), nullable=False, index=True)
    criado_por: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False)
    pergunta: Mapped[str] = mapped_column(String(300), nullable=False)
    data_inicio: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    data_fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class OpcaoVotacao(Base):
    __tablename__ = "opcoes_votacao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    votacao_id: Mapped[int] = mapped_column(ForeignKey("votacoes.id", ondelete="CASCADE"), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(String(180), nullable=False)
    ordem: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class Voto(Base):
    __tablename__ = "votos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    votacao_id: Mapped[int] = mapped_column(ForeignKey("votacoes.id", ondelete="CASCADE"), nullable=False, index=True)
    opcao_id: Mapped[int] = mapped_column(ForeignKey("opcoes_votacao.id", ondelete="CASCADE"), nullable=False)
    morador_id: Mapped[int] = mapped_column(ForeignKey("moradores.id", ondelete="CASCADE"), nullable=False, index=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint("votacao_id", "morador_id", name="uq_um_voto_por_morador"),)


class Agenda(Base):
    __tablename__ = "agenda"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bairro_id: Mapped[int] = mapped_column(ForeignKey("bairros.id", ondelete="CASCADE"), nullable=False, index=True)
    criado_por: Mapped[int | None] = mapped_column(ForeignKey("moradores.id", ondelete="SET NULL"))
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    titulo: Mapped[str] = mapped_column(String(160), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    local: Mapped[str | None] = mapped_column(String(220))
    inicio_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fim_em: Mapped[datetime | None] = mapped_column(DateTime)
    recorrencia: Mapped[str | None] = mapped_column(String(50))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
