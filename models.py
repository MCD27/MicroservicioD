from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabla de profesores
class Profesor(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String, nullable=False)
    materia = Column(String, nullable=False)

    # Relación con estudiantes
    estudiantes = relationship("Estudiante", back_populates="profesor")

# Tabla de estudiantes
class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String, nullable=False)
    carrera = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"))

    profesor = relationship("Profesor", back_populates="estudiantes")

