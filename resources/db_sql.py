# # database.py (UPDATED - Initial Data Inserted)
# from flask_restful import Resource
# from flask import request
# from typing import List, Optional, TypeVar, Generic
# from abc import ABC, abstractmethod
# from dataclasses import dataclass, asdict
# import sqlite3

# # ============================================
# # Task 1: Models (SRP)
# # ============================================

# @dataclass
# class Book:
#     """Represents a Book entity."""
#     title: str
#     author: str
#     category: str
#     id: Optional[int] = None

# @dataclass
# class Member:
#     """Represents a Member entity."""
#     name: str
#     email: str
#     id: Optional[int] = None

# # ============================================
# # Task 2 & 3: Repositories (OCP, LSP, ISP, DIP)
# # ============================================

# T = TypeVar('T')

# # Base abstraction for LSP
# class BaseRepository(ABC, Generic[T]):
#     @abstractmethod
#     def add(self, entity: T) -> T:
#         pass

#     @abstractmethod
#     def get_by_id(self, entity_id: int) -> Optional[T]:
#         pass

#     @abstractmethod
#     def get_all(self) -> List[T]:
#         pass

#     @abstractmethod
#     def update(self, entity: T) -> Optional[T]:
#         pass

#     @abstractmethod
#     def delete(self, entity_id: int) -> bool:
#         pass

# # Interface Segregation Principle (ISP) - Specific interfaces
# class BookRepository(BaseRepository[Book], ABC):
#     pass

# class MemberRepository(BaseRepository[Member], ABC):
#     pass


# # --- SQLite Implementation (Concrete Repositories) ---

# DB_NAME = "library.db"

# def get_db_connection():
#     """Initializes and returns a SQLite connection."""
#     conn = sqlite3.connect(DB_NAME)
#     conn.row_factory = sqlite3.Row
#     return conn

# def init_db():
#     """Initializes the database schema and inserts initial data."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # --- 1. Create Tables ---
#     # Book Table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS books (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             author TEXT,
#             category TEXT
#         );
#     """)
#     # Member Table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS members (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT UNIQUE NOT NULL
#         );
#     """)

#     # --- 2. Insert Initial Books (3 records) ---
#     cursor.execute("SELECT COUNT(*) FROM books")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO books (title, author, category) VALUES ('Design Patterns', 'Erich Gamma', 'Computer Science')")
#         cursor.execute("INSERT INTO books (title, author, category) VALUES ('Clean Code', 'Robert C. Martin', 'Software Engineering')")
#         cursor.execute("INSERT INTO books (title, author, category) VALUES ('The Alchemist', 'Paulo Coelho', 'Fiction')")

#     # --- 3. Insert Initial Members (3 records) ---
#     cursor.execute("SELECT COUNT(*) FROM members")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO members (name, email) VALUES ('Alice Smith', 'alice@example.com')")
#         cursor.execute("INSERT INTO members (name, email) VALUES ('Bob Johnson', 'bob@example.com')")
#         cursor.execute("INSERT INTO members (name, email) VALUES ('Charlie Brown', 'charlie@example.com')")
    
#     conn.commit()
#     conn.close()

# init_db() # Ensure DB is initialized and seeded when this file is imported

# class SQLiteBookRepository(BookRepository):
#     """Concrete SQLite implementation for Book persistence."""
#     def add(self, book: Book) -> Book:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "INSERT INTO books (title, author, category) VALUES (?, ?, ?)"
#         cursor.execute(query, (book.title, book.author, book.category))
#         book.id = cursor.lastrowid
#         conn.commit()
#         conn.close()
#         return book

#     def get_by_id(self, book_id: int) -> Optional[Book]:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
#         row = cursor.fetchone()
#         conn.close()
#         return Book(**dict(row)) if row else None

#     def get_all(self) -> List[Book]:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM books")
#         books = [Book(**dict(row)) for row in cursor.fetchall()]
#         conn.close()
#         return books
    
#     def update(self, book: Book) -> Optional[Book]:
#         if book.id is None: return None
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "UPDATE books SET title = ?, author = ?, category = ? WHERE id = ?"
#         cursor.execute(query, (book.title, book.author, book.category, book.id))
#         conn.commit()
#         conn.close()
#         return book if cursor.rowcount > 0 else None

#     def delete(self, book_id: int) -> bool:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
#         conn.commit()
#         conn.close()
#         return cursor.rowcount > 0

# class SQLiteMemberRepository(MemberRepository):
#     """Concrete SQLite implementation for Member persistence."""
#     def add(self, member: Member) -> Member:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "INSERT INTO members (name, email) VALUES (?, ?)"
#         cursor.execute(query, (member.name, member.email))
#         member.id = cursor.lastrowid
#         conn.commit()
#         conn.close()
#         return member

#     def get_by_id(self, member_id: int) -> Optional[Member]:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
#         row = cursor.fetchone()
#         conn.close()
#         return Member(**dict(row)) if row else None

#     def get_all(self) -> List[Member]:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM members")
#         members = [Member(**dict(row)) for row in cursor.fetchall()]
#         conn.close()
#         return members

#     def update(self, member: Member) -> Optional[Member]:
#         if member.id is None: return None
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = "UPDATE members SET name = ?, email = ? WHERE id = ?"
#         cursor.execute(query, (member.name, member.email, member.id))
#         conn.commit()
#         conn.close()
#         return member if cursor.rowcount > 0 else None

#     def delete(self, member_id: int) -> bool:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
#         conn.commit()
#         conn.close()
#         return cursor.rowcount > 0

# # ============================================
# # Task 4: Service Layer (DIP)
# # ============================================

# class BookService:
#     """Handles business logic related to Books."""
#     # DIP: Depends on the abstract BookRepository
#     def __init__(self, repo: BookRepository):
#         self._repo = repo

#     def add_book(self, title: str, author: str, category: str) -> Book:
#         return self._repo.add(Book(id=None, title=title, author=author, category=category))

#     def get_all_books(self) -> List[Book]:
#         return self._repo.get_all()

#     def get_book_by_id(self, book_id: int) -> Optional[Book]:
#         return self._repo.get_by_id(book_id)

#     def update_book(self, book_id: int, title: str, author: str, category: str) -> Optional[Book]:
#         return self._repo.update(Book(id=book_id, title=title, author=author, category=category))

#     def delete_book(self, book_id: int) -> bool:
#         return self._repo.delete(book_id)

# class MemberService:
#     """Handles business logic related to Members."""
#     # DIP: Depends on the abstract MemberRepository
#     def __init__(self, repo: MemberRepository):
#         self._repo = repo

#     def add_member(self, name: str, email: str) -> Member:
#         return self._repo.add(Member(id=None, name=name, email=email))

#     def get_all_members(self) -> List[Member]:
#         return self._repo.get_all()

#     def get_member_by_id(self, member_id: int) -> Optional[Member]:
#         return self._repo.get_by_id(member_id)
    
#     def update_member(self, member_id: int, name: str, email: str) -> Optional[Member]:
#         return self._repo.update(Member(id=member_id, name=name, email=email))

#     def delete_member(self, member_id: int) -> bool:
#         return self._repo.delete(member_id)

# # ============================================
# # Task 5: Flask-Restful Controllers (SRP)
# # ============================================

# # Global service references for Dependency Injection
# book_service: Optional[BookService] = None
# member_service: Optional[MemberService] = None

# def init_services(b_service: BookService, m_service: MemberService):
#     """Injects service instances into the controllers."""
#     global book_service, member_service
#     book_service = b_service
#     member_service = m_service

# # --- Book Resources ---

# class BooksGETResource(Resource):
#     def get(self):
#         books = [asdict(book) for book in book_service.get_all_books()]
#         return books

# class BookGETResource(Resource):
#     def get(self, id):
#         book = book_service.get_book_by_id(id)
#         if book:
#             return asdict(book)
#         return {"message": f"Book with id {id} not found"}, 404

# class BookPOSTResource(Resource):
#     def post(self):
#         try:
#             data = request.get_json(force=True)
#             title, author, category = data.get("title"), data.get("author", "N/A"), data.get("category", "General")
#         except:
#             return {"message": "Invalid JSON data provided"}, 400

#         if not title:
#             return {"message": "Missing 'title' field in request body"}, 400

#         new_book = book_service.add_book(title, author, category)
#         return asdict(new_book), 201

# class BookPUTResource(Resource):
#     def put(self, id):
#         try:
#             data = request.get_json(force=True)
#             title = data.get("title")
#             author = data.get("author")
#             category = data.get("category")
#         except:
#             return {"message": "Invalid JSON data provided"}, 400

#         if not all([title, author, category]):
#             return {"message": "Missing required fields for update (title, author, category)"}, 400

#         updated_book = book_service.update_book(id, title, author, category)
#         if updated_book:
#             return asdict(updated_book)
#         return {"message": f"Book with id {id} not found"}, 404

# class BookDELETEResource(Resource):
#     def delete(self, id):
#         if book_service.delete_book(id):
#             return "", 204
#         return {"message": f"Book with id {id} not found"}, 404


# # --- Member Resources ---

# class MembersGETResource(Resource):
#     def get(self):
#         members = [asdict(m) for m in member_service.get_all_members()]
#         return members

# class MemberGETResource(Resource):
#     def get(self, id):
#         member = member_service.get_member_by_id(id)
#         if member:
#             return asdict(member)
#         return {"message": f"Member with id {id} not found"}, 404

# class MemberPOSTResource(Resource):
#     def post(self):
#         try:
#             data = request.get_json(force=True)
#             name, email = data.get("name"), data.get("email")
#         except:
#             return {"message": "Invalid JSON data provided"}, 400

#         if not all([name, email]):
#             return {"message": "Missing required fields (name, email)"}, 400

#         new_member = member_service.add_member(name, email)
#         return asdict(new_member), 201
        
# class MemberPUTResource(Resource):
#     def put(self, id):
#         try:
#             data = request.get_json(force=True)
#             name, email = data.get("name"), data.get("email")
#         except:
#             return {"message": "Invalid JSON data provided"}, 400

#         if not all([name, email]):
#             return {"message": "Missing required fields for update (name, email)"}, 400

#         updated_member = member_service.update_member(id, name, email)
#         if updated_member:
#             return asdict(updated_member)
#         return {"message": f"Member with id {id} not found"}, 404

# class MemberDELETEResource(Resource):
#     def delete(self, id):
#         if member_service.delete_member(id):
#             return "", 204
#         return {"message": f"Member with id {id} not found"}, 404

# # Expose the necessary resources for application.py
# __all__ = [
#     'SQLiteBookRepository', 'SQLiteMemberRepository', 
#     'BookService', 'MemberService', 
#     'init_services',
#     'BooksGETResource', 'BookGETResource', 'BookPOSTResource', 'BookPUTResource', 'BookDELETEResource',
#     'MembersGETResource', 'MemberGETResource', 'MemberPOSTResource', 'MemberPUTResource', 'MemberDELETEResource'
# ]