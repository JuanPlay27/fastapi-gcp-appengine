from fastapi import FastAPI
from database import get_db_connection
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": os.getenv("HOLA_MUNDO")}

@app.get("/students")
def read_students():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students;")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return {"students": students}

@app.post("/students")
def create_student(name: str, age: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s) RETURNING *;", (name, age))
    new_student = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return {"student": new_student}