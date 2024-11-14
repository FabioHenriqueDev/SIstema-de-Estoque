
# produto atributo

import sys
from datetime import datetime
from InquirerPy import prompt
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()

engine = create_engine("sqlite:///gerenciamento_estoque.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Estoque(Base):
    pass



Base.metadata.create_all(engine)