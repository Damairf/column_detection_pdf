from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    nama = Column(String)
    divisi = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Template(Base):
    __tablename__ = "template"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    nama_template = Column(String)
    jml_halaman = Column(Integer)
    path_template_pdf = Column(String)
    resolusi_width = Column(Integer)
    resolusi_height = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Dokumen(Base):
    __tablename__ = "dokumen"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    nama_dokumen = Column(String)
    status = Column(String)
    path_dokumen = Column(String)
    id_template = Column(Integer, ForeignKey("template.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())


class KolomTemplate(Base):
    __tablename__ = "kolom_template"

    id = Column(Integer, primary_key=True)
    id_template = Column(Integer, ForeignKey("template.id"))
    nama_kolom = Column(String)
    halaman = Column(Integer)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    resolusi_width = Column(Integer)
    resolusi_height = Column(Integer)
    type = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class HasilDeteksi(Base):
    __tablename__ = "hasil_deteksi"

    id = Column(Integer, primary_key=True)
    id_dokumen = Column(Integer, ForeignKey("dokumen.id"))
    id_kolom_template = Column(Integer, ForeignKey("kolom_template.id"))
    status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())