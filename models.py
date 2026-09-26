from datetime import date, time
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Date, Time, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Actividad(Base):
    __tablename__ = "actividad"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(225), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    duracion: Mapped[int] = mapped_column(Integer, nullable=False)
    cupo_max: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relaciones
    clases: Mapped[List["Clase"]] = relationship(back_populates="actividad")
    inscripciones: Mapped[List["Inscripcion"]] = relationship(back_populates="actividad")

class Profesor(Base):
    __tablename__ = "profesor"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    apellido: Mapped[str] = mapped_column(String(225), nullable=False)
    nombre: Mapped[str] = mapped_column(String(225), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(225), nullable=True)
    email: Mapped[str] = mapped_column(String(225), nullable=False)
    nro_documento: Mapped[str] = mapped_column(String(225), unique=True, nullable=False)

    # Relaciones
    clases: Mapped[List["Clase"]] = relationship(back_populates="profesor")

class Socio(Base):
    __tablename__ = "socio"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    apellido: Mapped[str] = mapped_column(String(225), nullable=False)
    nombre: Mapped[str] = mapped_column(String(225), nullable=False)
    f_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(225), nullable=True)
    email: Mapped[str] = mapped_column(String(225), nullable=False)
    f_alta: Mapped[date] = mapped_column(Date, default=date.today, nullable=True)
    nro_documento: Mapped[str] = mapped_column(String(225), unique=True, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)

    # Relaciones
    inscripciones: Mapped[List["Inscripcion"]] = relationship(back_populates="socio")
    asistencias: Mapped[List["Asistencia"]] = relationship(back_populates="socio")

class Clase(Base):
    __tablename__ = "clase"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dia_de_la_semana: Mapped[str] = mapped_column(String, nullable=False)
    horario: Mapped[time] = mapped_column(Time, nullable=False)
    profesor_id: Mapped[int] = mapped_column(ForeignKey("profesor.id"), nullable=False)
    actividad_id: Mapped[int] = mapped_column(ForeignKey("actividad.id"), nullable=False)

    # Restricción Unique (UK)
    __table_args__ = (
        UniqueConstraint("dia_de_la_semana", "horario", "actividad_id", name="uk_clase_act_dia_hora"),
    )

    # Relaciones
    profesor: Mapped["Profesor"] = relationship(back_populates="clases")
    actividad: Mapped["Actividad"] = relationship(back_populates="clases")
    asistencias: Mapped[List["Asistencia"]] = relationship(back_populates="clase")

class Inscripcion(Base):
    __tablename__ = "inscripcion"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actividad_id: Mapped[int] = mapped_column(ForeignKey("actividad.id"), nullable=False)
    socio_id: Mapped[int] = mapped_column(ForeignKey("socio.id"), nullable=False)
    f_inscripcion: Mapped[date] = mapped_column(Date, default=date.today, nullable=True)

    __table_args__ = (
        UniqueConstraint("actividad_id", "socio_id", name="uk_inscripcion_clase_socio"),
    )

    # Relaciones
    actividad: Mapped["Actividad"] = relationship(back_populates="inscripciones")
    socio: Mapped["Socio"] = relationship(back_populates="inscripciones")

class Asistencia(Base):
    __tablename__ = "asistencia"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    socio_id: Mapped[int] = mapped_column(ForeignKey("socio.id"), nullable=False)
    clase_id: Mapped[int] = mapped_column(ForeignKey("clase.id"), nullable=False)
    f_asistencia: Mapped[date] = mapped_column(Date, default=date.today, nullable=True)

    __table_args__ = (
        UniqueConstraint("socio_id", "clase_id", "f_asistencia", name="uk_socio_clase_fecha"),
    )

    # Relaciones
    socio: Mapped["Socio"] = relationship(back_populates="asistencias")
    clase: Mapped["Clase"] = relationship(back_populates="asistencias")