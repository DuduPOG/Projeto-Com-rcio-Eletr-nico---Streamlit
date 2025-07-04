from models.cliente import Cliente, Clientes
from models.categoria import Categoria, Categorias
from models.produto import Produto, Produtos
from models.venda import Venda, Vendas
from models.venda_item import VendaItem, VendaItens

from view import View

class UI:  # Visão/Apresentação - Não tem instância
    carrinho = None   # atributo de classe
    @staticmethod
    def menu():
        print("|------------------------------------------------|")
        print("| Cadastro de Clientes                           |")
        print("| 1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir    |")
        print("|------------------------------------------------|")
        print("| Cadastro de Categorias                         |")
        print("| 5-Inserir, 6-Listar, 7-Atualizar, 8-Excluir    |")
        print("|------------------------------------------------|")
        print("| Cadastro de Produtos                           |")
        print("| 9-Inserir, 10-Listar, 11-Atualizar, 12-Excluir |")
        print("|------------------------------------------------|")
        print("| 13-Iniciar um carrinho de compra               |")
        print("| 14-Listar as compras                           |")
        print("| 15-Visualizar carrinho                         |")
        print("| 16-Inserir produto no carrinho                 |")
        print("| 17-Confirmar a compra                          |")
        print("|------------------------------------------------|")
        print("| 99-FIM                                         |")
        print("|------------------------------------------------|")
        print()
        op = int(input("Selecione uma opção: "))
        print()
        return op

    @staticmethod
    def main(): 
        View.cadastrar_admin()  
        op = 0
        # clientes = []
        while op != 99:
            op = UI.menu()
            if op == 1: UI.cliente_inserir() 
            if op == 2: UI.cliente_listar()
            if op == 3: UI.cliente_atualizar()
            if op == 4: UI.cliente_excluir()

            if op == 5: UI.categoria_inserir() 
            if op == 6: UI.categoria_listar()
            if op == 7: UI.categoria_atualizar()
            if op == 8: UI.categoria_excluir()

            if op == 9: UI.produto_inserir() 
            if op == 10: UI.produto_listar()
            if op == 11: UI.produto_atualizar()
            if op == 12: UI.produto_excluir()

            if op == 13: UI.venda_inserir()
            if op == 14: UI.venda_listar()
            if op == 15: UI.visualizar_carrinho()
            if op == 16: UI.inserir_produto_no_carrinho()
            if op == 17: UI.confirmar_compra()


    # Operações de Venda
    @classmethod
    def venda_inserir(cls): # C - create
        v = Venda(0)
        Vendas.inserir(v)
        cls.carrinho = v

    @staticmethod # R - read
    def venda_listar(): 
        for v in Vendas.listar(): 
            print(v)
            for item in VendaItens.listar():
                if item.id_venda == v.id:
                    id_produto = item.id_produto
                    descricao = Produtos.listar_id(id_produto).descricao
                    print(f"  {descricao} - Qtd: {item.qtd} - R$ {item.preco:.2f}")


    @classmethod 
    def visualizar_carrinho(cls): 
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        print("Este é seu carrinho atual: ", cls.carrinho)
        for item in VendaItens.listar():
            if item.id_venda == cls.carrinho.id:
                id_produto = item.id_produto
                descricao = Produtos.listar_id(id_produto).descricao
                print(f"  {descricao} - Qtd: {item.qtd} - R$ {item.preco:.2f}")

    @classmethod 
    def inserir_produto_no_carrinho(cls):
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        
        # Listar os produtos disponíveis
        UI.produto_listar()
        id_produto = int(input("Informe o id do produto: "))
        qtd = int(input("Informe a qtd: "))

        # inserir o produto no carrinho
        View.inserir_produto_no_carrinho(cls.carrinho.id, id_produto, qtd)
        """
        # Consultar preço do produto
        preco = Produtos.listar_id(id_produto).preco
        # Instanciar o item da venda
        vi = VendaItem(0, qtd, preco)
        vi.id_venda = cls.carrinho.id
        vi.id_produto = id_produto
        # Inserir o item da venda
        VendaItens.inserir(vi)
        # Atualizar o total da venda (carrinho)
        subtotal = qtd * preco
        cls.carrinho.total += subtotal
        Vendas.atualizar(cls.carrinho)
        """
    @classmethod 
    def confirmar_compra(cls): 
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        # Na venda (carrinho), colocar o atributo carrinho para False
        cls.carrinho.carrinho = False
        Vendas.atualizar(cls.carrinho)
        # Percorrer os itens da venda (vendaitem-qtd) e baixar o estoque no
        # cadastro de produto (produto-estoque)
        for item in VendaItens.listar():
            if item.id_venda == cls.carrinho.id:
                id_produto = item.id_produto
                qtd = item.qtd
                produto = Produtos.listar_id(id_produto)
                produto.estoque -= qtd
                Produtos.atualizar(produto)

    # CRUD de Clientes
    @staticmethod
    def cliente_inserir(): # C - create
        # id = int(input("Informe o id do cliente: "))
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o fone: ")
        #c = Cliente(0, nome, email, fone)
        #Clientes.inserir(c)
        View.cliente_inserir(nome, email, fone)
    @staticmethod # R - read
    def cliente_listar(): 
        #for c in Clientes.listar(): print(c)
        for c in View.cliente_listar(): print(c)
    @staticmethod # U - update
    def cliente_atualizar(): 
        UI.cliente_listar()
        id = int(input("Informe o id do cliente a ser atualizado: "))
        nome = input("Informe o novo nome: ")
        email = input("Informe o novo e-mail: ")
        fone = input("Informe o novo fone: ")        
        #c = Cliente(id, nome, email, fone)
        #Clientes.atualizar(c)
        View.cliente_atualizar(id, nome, email, fone)
    @staticmethod # D - delete
    def cliente_excluir(): 
        UI.cliente_listar()
        id = int(input("Informe o id do cliente a ser excluído: "))
        #c = Cliente(id, "", "", "")
        #Clientes.excluir(c)
        View.cliente_excluir(id)

    # CRUD de Categorias
    @staticmethod
    def categoria_inserir(): # C - create
        descricao = input("Informe a descrição: ")
        c = Categoria(0, descricao)
        Categorias.inserir(c)
    
    @staticmethod # R - read
    def categoria_listar(): 
        for c in Categorias.listar(): print(c)
    
    @staticmethod # U - update
    def categoria_atualizar(): 
        UI.categoria_listar()
        id = int(input("Informe o id da categoria a ser atualizada: "))
        descricao = input("Informe a nova descrição: ")
        c = Categoria(id, descricao)
        Categorias.atualizar(c)
    
    @staticmethod # D - delete
    def categoria_excluir(): 
        UI.categoria_listar()
        id = int(input("Informe o id da categoria a ser excluída: "))
        c = Categoria(id, "")
        Categorias.excluir(c)

    # CRUD de Produtos
    @staticmethod
    def produto_inserir(): # C - create
        descricao = input("Informe a descrição: ")
        preco = float(input("Informe o preço: "))
        estoque = int(input("Informe o estoque: "))
        UI.categoria_listar()
        id_categoria = int(input("Informe o id da categoria: "))
        c = Produto(0, descricao, preco, estoque)
        c.id_categoria = id_categoria
        Produtos.inserir(c)
    @staticmethod # R - read
    def produto_listar(): 
        for c in Produtos.listar(): print(c)
    @staticmethod # U - update
    def produto_atualizar(): 
        UI.produto_listar()
        id = int(input("Informe o id do produto a ser atualizado: "))
        descricao = input("Informe a nova descrição: ")
        preco = float(input("Informe o novo preço: "))
        estoque = int(input("Informe o novo estoque: "))
        UI.categoria_listar()
        id_categoria = int(input("Informe o id da nova categoria: "))
        c = Produto(id, descricao, preco, estoque)
        c.id_categoria = id_categoria
        Produtos.atualizar(c)
    @staticmethod # D - delete
    def produto_excluir(): 
        UI.produto_listar()
        id = int(input("Informe o id do produto a ser excluído: "))
        c = Produto(id, "", "", "")
        Produtos.excluir(c)

UI.main()