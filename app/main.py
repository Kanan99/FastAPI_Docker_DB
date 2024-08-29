# Import necessary modules
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Define Pydantic model for book creation
class BookCreate(BaseModel):
    title: str
    author: str
    description: str

# Define route to create a book
@app.post("/books/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Create new Book instance
    db_book = models.Book(**book.dict())
    # Add book to database
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Define route to get all books
@app.get("/books/")
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Query database for books
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

# Define route to get a specific book
@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    # Query database for specific book
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
