from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=True)
    apellido: Mapped[str] = mapped_column(String(80), nullable=True)
    fecha_registro: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    favoritos: Mapped[list["Favorito"]] = relationship(back_populates="usuario")
    posts: Mapped[list["Post"]] = relationship(back_populates="autor")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }


class Personaje(db.Model):
    __tablename__ = "personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    especie: Mapped[str] = mapped_column(String(120), nullable=True)
    genero: Mapped[str] = mapped_column(String(50), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)

    favoritos: Mapped[list["Favorito"]] = relationship(back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }


class Planeta(db.Model):
    __tablename__ = "planeta"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    clima: Mapped[str] = mapped_column(String(120), nullable=True)
    terreno: Mapped[str] = mapped_column(String(120), nullable=True)
    poblacion: Mapped[int] = mapped_column(BigInteger, nullable=True)

    favoritos: Mapped[list["Favorito"]] = relationship(back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }


class Favorito(db.Model):
    __tablename__ = "favorito"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=True)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=True)
    fecha_guardado: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="favoritos")
    personaje: Mapped["Personaje"] = relationship(back_populates="favoritos")
    planeta: Mapped["Planeta"] = relationship(back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_publicacion: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    autor: Mapped["Usuario"] = relationship(back_populates="posts")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo
        }


class Comentario(db.Model):
    __tablename__ = "comentario"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="comentarios")
    post: Mapped["Post"] = relationship(back_populates="comentarios")

    def serialize(self):
        return {
            "id": self.id,
            "contenido": self.contenido
        }
