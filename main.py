from fastapi import FastAPI  # import FastAPI es la clase que se importa del modulo descargado from fastapi

app = FastAPI()

#http://127.0.0.1:8000/

@app.get("/") # se registra la ruta para que funcione el def index
def index():
    return {"message" : "Bienvenido al microservicio"}


