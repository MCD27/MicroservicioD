from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from pydantic import BaseModel  # Importar Pydantic

app = FastAPI()

# http://127.0.0.1:8000/
@app.get("/")
def index():
    return {"message": "Bienvenido al microservicio"}

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- MODELOS Pydantic ----------------------

class ProfesorCreate(BaseModel):
    nombre: str
    materia: str

class EstudianteCreate(BaseModel):
    nombre: str
    carrera: str
    semestre: int
    profesor_id: int

# ---------------------- ESTUDIANTES ----------------------

# Obtener todos los estudiantes
@app.get("/estudiantes/")
def get_estudiantes(db: Session = Depends(get_db)):
    return db.query(models.Estudiante).all()

# Agregar un nuevo estudiante (usando request body)
@app.post("/estudiantes/")
def create_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    profesor = db.query(models.Profesor).filter(models.Profesor.id == estudiante.profesor_id).first()
    if not profesor:
        raise HTTPException(status_code=400, detail="El profesor_id no es válido")
    
    nuevo_estudiante = models.Estudiante(
        nombre=estudiante.nombre,
        carrera=estudiante.carrera,
        semestre=estudiante.semestre,
        profesor_id=estudiante.profesor_id
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

# Actualizar un estudiante
@app.put("/estudiantes/{id}")
def update_estudiante(id: int, estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    estudiante_db = db.query(models.Estudiante).filter(models.Estudiante.id == id).first()
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante_db.nombre = estudiante.nombre
    estudiante_db.carrera = estudiante.carrera
    estudiante_db.semestre = estudiante.semestre
    estudiante_db.profesor_id = estudiante.profesor_id
    
    db.commit()
    return estudiante_db

# Eliminar un estudiante
@app.delete("/estudiantes/{id}")
def delete_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(models.Estudiante).filter(models.Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()
    return {"message": "Estudiante eliminado correctamente"}

# ---------------------- PROFESORES ----------------------

# Obtener todos los profesores
@app.get("/profesores/")
def get_profesores(db: Session = Depends(get_db)):
    return db.query(models.Profesor).all()

# Agregar un nuevo profesor (usando request body)
@app.post("/profesores/")
def create_profesor(profesor: ProfesorCreate, db: Session = Depends(get_db)):
    nuevo_profesor = models.Profesor(nombre=profesor.nombre, materia=profesor.materia)
    db.add(nuevo_profesor)
    db.commit()
    db.refresh(nuevo_profesor)
    return nuevo_profesor

# Actualizar un profesor
@app.put("/profesores/{id}")
def update_profesor(id: int, profesor: ProfesorCreate, db: Session = Depends(get_db)):
    profesor_db = db.query(models.Profesor).filter(models.Profesor.id == id).first()
    if not profesor_db:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    profesor_db.nombre = profesor.nombre
    profesor_db.materia = profesor.materia

    db.commit()
    return profesor_db

# Eliminar un profesor
@app.delete("/profesores/{id}")
def delete_profesor(id: int, db: Session = Depends(get_db)):
    profesor = db.query(models.Profesor).filter(models.Profesor.id == id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    db.delete(profesor)
    db.commit()
    return {"message": "Profesor eliminado correctamente"}
