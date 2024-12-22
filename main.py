import sys
from datetime import datetime
from InquirerPy import prompt
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from rich import print

from rich.console import Console


console = Console()

engine = create_engine("sqlite:///gerenciamento_estoque.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Estoque(Base):
    __tablename__ = 'Estoque'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    produto = Column('produto', String)
    quantidade = Column('quantidade', Integer)
    preco_unitario = Column('preço unitario', Float)
    data_de_entrega = Column('data de entrega', String)
    fornecedor = Column('fornecedor', String)
    categoria = Column('categoria', String)


    def __init__(self, produto, quantidade, preco_unitario, data_de_entrega, fornecedor, categoria):
        
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.data_de_entrega = data_de_entrega
        self.fornecedor = fornecedor
        self.categoria = categoria
        
    
Base.metadata.create_all(engine)


def adicionar_produto():
       
        produto = input('Digite um produto para adicionar ao estoque: ').lower()

        produto_existente = session.query(Estoque).filter(Estoque.produto == produto).first()
        
        if produto_existente is not None:
            console.print('AVISO: Esse produto ja existe edite ele.', style='yellow')
            sys.exit()
            
        try:
            quantidade = int(input('Digite a quantidade do produto: '))
            
        except ValueError:
            console.print('ERROR: Digite números e não letras', style='red')
            sys.exit()
               
        try:
            preco_unitario = float(input('Digite o preco unitario do produto: '))
            
        except ValueError:
            console.print('ERROR: Digite números e não letras', style='red')
            sys.exit()

        data_de_entrega = datetime.now().date()
        fornecedor = input('Digite o fornecedor: ').lower()
        categoria = input('Digite a categoria do produto: ').lower()

        produto = Estoque(
            produto = produto,
            quantidade = quantidade,
            preco_unitario = preco_unitario,
            data_de_entrega = data_de_entrega,
            fornecedor = fornecedor,
            categoria = categoria
        )
        
        session.add(produto)
        session.commit()
        console.print("Produto adicionado com sucesso!", style='green')
        

def remover_produto():
    produto_a_remover = input('Digite o produto que você deseja remover: ').lower()
    pergunta = session.query(Estoque).filter(Estoque.produto == produto_a_remover).first()

    if pergunta is not None:
        session.delete(pergunta)
        session.commit()
        console.print('Produto removido com sucesso', style='green')


    else:
        console.print('AVISO: Esse produto não existe', style='yellow')


def listar_produto():
    produtos = input('Digite o produto que deseje listar: ').lower()
    

    produto = session.query(Estoque).filter(Estoque.produto == produtos).first()

    if not produto:
        console.print('AVISO: Esse produto não existe.', style='yellow')
        sys.exit()
    
   
    console.print(f"ID: {produto.id}", style='blue')
    console.print(f"Produto: {produto.produto}")
    console.print(f"Quantidade: {produto.quantidade}")
    console.print(f"Preço Unitário: R${produto.preco_unitario:.2f}")
    console.print(f"Data de Entrega: {produto.data_de_entrega}")
    console.print(f"Fornecedor: {produto.fornecedor}")
    console.print(f"Categoria: {produto.categoria}")
    console.print("-" * 30) 


def editar_produto():
    pergunta = input('Digite o produto que você deseje editar: ').lower()
    pergunta = session.query(Estoque).filter(Estoque.produto == pergunta).first()

    if pergunta is None:
        console.print('AVISO: Esse produto não existe.', style='yellow')
        console.print('AVISO: Você pode ter digitado o nome do produto errado.', style='yellow')
        sys.exit()

    produto = input('Digite o nome do produto: ').lower()
    pergunta.produto = produto

    try:
        quantidade = int(input('Digite a quantidade do produto: '))
        pergunta.quantidade = quantidade
    
    except ValueError:
        console.print('ERROR: Digite números e não letras ou digite números inteiros', style='red')
        sys.exit()

    try:
        preco_unitario = float(input('Digite o preço unitário: '))
        pergunta.preco_unitario = preco_unitario
    
    except ValueError:
        console.print('ERROR: Digite números e não letras', style='red')
        sys.exit()


    data_de_entrega = datetime.now().date()
    pergunta.data_de_entrega = data_de_entrega

    fornecedor = input('Digite o nome do fornecedor: ').lower()
    pergunta.fornecedor = fornecedor

    categoria = input("Digite a categoria: ").lower()
    pergunta.categoria = categoria

   
    session.commit()
    console.print('Produto alterado com sucesso!', style='green')


def menu():
    perguntas = [
        {
            'type': 'list',
            'name': 'opcao',
            'message': 'Selecione uma das opções abaxo:',
            'choices': [
                        
                        '1.Adicionar Produto',
                        '2.Remover Produto',
                        '3.Mostrar informações do Produto',
                        '4.Editar Produto',
                        '5.Sair'                   
                        
                    ]
                        
        }
    ]
    
    resultado = prompt(perguntas)

    if resultado['opcao'] == '1.Adicionar Produto':
        adicionar_produto()

    elif resultado['opcao'] == '2.Remover Produto':
        remover_produto()

    elif resultado['opcao'] == '3.Mostrar informações do Produto':
        listar_produto()

    elif resultado['opcao'] == '4.Editar Produto':
        editar_produto()
    
    elif resultado['opcao'] == '5.Sair':
        console.print('Saindo do programa.', style='blue')
        sys.exit()


    

menu()

print("Obrigado por utilizar meu programa.")