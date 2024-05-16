from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import mysql.connector

#Cria a janela principal
janela = Tk()
janela.title("ALMOXARIFADO")
janela.configure(background= '#1e3743')
janela.geometry("700x600")
janela.resizable(True, True)
janela.maxsize(width=800, height=700)
janela.minsize(width=500, height=300)
frame_1 = Frame(janela, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
frame_2 = Frame(janela, bd=4, bg='#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)


def estoque_faltas():
    janela.title("ALMOXARIFADO ESTOQUE, EM BAIXAS")
    conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="almoxarifado"
        )
    
    def mudar_materiais():
        destruir_campos()
        materiais()   

    #Função para mudar para o CRUD do estoque  
    def mudar_posicao_estoque():
        destruir_campos()
        pos_estoque()
    
    def mudar_professores():
        destruir_campos()
        professores()
        
    def destruir_campos():
        lb_cod_pos.destroy()
        cod_pos_entry.destroy()
        bt_materiais.destroy()
        bt_mudar_prof.destroy()
        bt_posicao_estoque.destroy()
        lista_pos2.destroy()
        bt_buscar_estoque.destroy()
        lb_cod_pos_estoque.destroy()
        
    def pesquisar_estoque_baixo():
        try:
            cursor = conexao.cursor()
            consulta_sql = "SELECT posicao_estoque.codigo_pos, posicao_estoque.quant_min_pos, posicao_estoque.quant_atual_pos, posicao_estoque.quant_max_pos, materiais.descricao_mat FROM posicao_estoque INNER JOIN materiais ON posicao_estoque.codigo_pos = materiais.codigo_mat WHERE posicao_estoque.quant_atual_pos < posicao_estoque.quant_min_pos"
            cursor.execute(consulta_sql)
            resultados = cursor.fetchall()
            for linha in resultados:  
                lista_pos.insert("", END, values=linha)
                
        except mysql.connector.Error as erro:
            print("Erro ao pesquisar o dado:", erro)
            messagebox.shoaskyesnowinfo("Mensagem", "pesquisa não realizada.")
            
    def pesquisar_estoque():
        try:
            lista_pos2.delete(*lista_pos2.get_children())
            cursor = conexao.cursor()
            texto_digitado = cod_pos_entry.get()
            consulta_sql = "SELECT posicao_estoque.codigo_pos, posicao_estoque.quant_min_pos, posicao_estoque.quant_atual_pos, posicao_estoque.quant_max_pos, materiais.descricao_mat FROM posicao_estoque INNER JOIN materiais ON posicao_estoque.codigo_pos = materiais.codigo_mat WHERE codigo_pos = %s"
            cursor.execute(consulta_sql, (texto_digitado,))
            resultados = cursor.fetchall()
            for linha in resultados:
                lista_pos2.insert("", END, values=linha)
                qnt_min = linha [1]
                qnt_atual = linha [2]
                qnt_max = linha [3]
                
            qnt_min = int(qnt_min)
            qnt_atual = int(qnt_atual)
            qnt_max = int(qnt_max)
            
            if qnt_min > qnt_atual:
                qnt_faltando = qnt_min - qnt_atual
                qnt_faltando = str(qnt_faltando)
                novo_texto = "Produto a baixo do esperado, para atingir o minimo faltam: " + qnt_faltando
                lb_cod_pos_estoque.config(text=novo_texto)
                
            elif qnt_atual > qnt_min:
                qnt_sobre = qnt_atual - qnt_min
                qnt_sobre = str(qnt_sobre)
                novo_texto = "Produto a acima do minimo : " + qnt_sobre
                lb_cod_pos_estoque.config(text=novo_texto)
                
            elif qnt_atual > qnt_max:
                qnt_sobre = qnt_atual - qnt_max
                qnt_sobre = str(qnt_sobre)
                novo_texto = "Produto a acima do maximo : " + qnt_sobre
                lb_cod_pos_estoque.config(text=novo_texto)
                
                
        except mysql.connector.Error as erro:
            print("Erro ao pesquisar o dado:", erro)
            messagebox.shoaskyesnowinfo("Mensagem", "pesquisa não realizada.")


    
    lb_cod_pos = Label(frame_1, text = "Registro", bg= '#dfe3ee', fg = '#107db2')
    lb_cod_pos.place(relx= 0.05, rely= 0.05 )
    
    cod_pos_entry = Entry(frame_1 )
    cod_pos_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)
     
    bt_materiais = Button(frame_1, command=mudar_materiais, text= 'Materiais', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_materiais.place(relx=0.50, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_prof = Button(frame_1, command=mudar_professores, text= 'Professores', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_prof.place(relx=0.10, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_posicao_estoque = Button(frame_1, command=mudar_posicao_estoque, text= 'Estoque', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_posicao_estoque.place(relx=0.30, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_buscar_estoque = Button(frame_1, text='Buscar' ,command=pesquisar_estoque,  bg = '#107db2', fg = 'white')
    bt_buscar_estoque.place(relx=0.15, rely=0.11, relwidth=0.1, relheight=0.14)
    janela.bind("<Return>", lambda event: pesquisar_estoque())
    cod_pos_entry.focus()
    
    fonte = ("Arial", 14)
    lb_cod_pos_estoque = Label(frame_1, text = "", bg= '#dfe3ee', fg = '#107db2', font=fonte)
    lb_cod_pos_estoque.place(relx= 0.05, rely= 0.50, relwidth=0.80, relheight=0.15)
    
    lista_pos2 = ttk.Treeview(frame_1, height=2,column=("col1", "col2", "col3", "col4", "col5", "col6" ))
    lista_pos2.heading("#0", text="")
    lista_pos2.heading("#1", text="Código")
    lista_pos2.heading("#2", text="Minímo")
    lista_pos2.heading("#3", text="Atual")
    lista_pos2.heading("#4", text="Máximo")
    lista_pos2.heading("#5", text="Material")
    lista_pos2.column("#0", width=0)
    lista_pos2.column("#1", width=70)
    lista_pos2.column("#2", width=80)
    lista_pos2.column("#3", width=80)
    lista_pos2.column("#4", width=80)
    lista_pos2.column("#5", width=80)
    lista_pos2.place(relx=0.30, rely=0.10, relwidth=0.65, relheight=0.30)
    scroolLista = Scrollbar(frame_2, orient='vertical')
    lista_pos2.configure(yscroll=scroolLista.set)
    scroolLista.place(relx=0.30, rely=0.10, relwidth=0.65, relheight=0.40)
    
    
    lista_pos = ttk.Treeview(frame_2, height=3,column=("col1", "col2", "col3", "col4", "col5", "col6" ))
    lista_pos.heading("#0", text="")
    lista_pos.heading("#1", text="Código")
    lista_pos.heading("#2", text="Quantidade miníma")
    lista_pos.heading("#3", text="Quantidade atual")
    lista_pos.heading("#4", text="Quantidade máxima")
    lista_pos.heading("#5", text="Material")
    lista_pos.column("#0", width=1)
    lista_pos.column("#1", width=120)
    lista_pos.column("#2", width=120)
    lista_pos.column("#3", width=120)
    lista_pos.column("#4", width=120)
    lista_pos.column("#5", width=120)
    lista_pos.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
    scroolLista = Scrollbar(frame_2, orient='vertical')
    lista_pos.configure(yscroll=scroolLista.set)
    scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
    
    pesquisar_estoque_baixo()

    
#=========================================================================================================#
#PROFESSOR#

#Funçao para alternar até o CRUD da tabela professor
def professores():
    janela.title("ALMOXARIFADO PROFESSORES")
    conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="almoxarifado"
        )

    #Função para mudar para o CRUD dos materiais
    def mudar_materiais():
        destruir_campos()
        materiais()   

    #Função para mudar para o CRUD do estoque  
    def mudar_estoque():
        destruir_campos()
        pos_estoque()
        
    def mudar_estoque_faltas():
        destruir_campos()
        estoque_faltas()

        
    #Função para destruir tudo na tela a fim de sair do CRUD dos professores    
    def destruir_campos():
        bt_mudar_materiais.destroy()
        bt_mudar_estoque.destroy()
        bt_limpar_prof.destroy()
        bt_buscar_prof.destroy()
        bt_novo_prof.destroy()
        bt_alterar_prof.destroy()
        bt_apagar_prof.destroy()
        bt_confirmar.destroy()
        bt_cancelar.destroy()
        lb_cod_prof.destroy()
        cod_prof_entry.destroy()
        lb_nome_prof.destroy()
        nome_prof_entry.destroy()
        lb_tipo_usuario.destroy()
        tipo_usuario_entry.destroy()
        lb_senha.destroy()
        senha_entry.destroy()
        lb_numero_tel.destroy()
        numero_tel_entry.destroy()
        bt_mudar_estoque.destroy()
        bt_mudar_materiais.destroy()
        bt_mudar_estoque_faltas.destroy()
     
    #Funçao para limpar atualizar automaticamente quando feita alguma mudança no banco de dados
    def limpar_tabela():
        nome_prof_entry.config(state='normal')
        tipo_usuario_entry.config(state='normal')
        senha_entry.config(state='normal')
        numero_tel_entry.config(state="normal")
        cod_prof_entry.delete(0, END)
        nome_prof_entry.delete(0, END)
        tipo_usuario_entry.delete(0, END)
        senha_entry.delete(0, END)
        numero_tel_entry.delete(0, END)
        nome_prof_entry.config(state='disabled')
        tipo_usuario_entry.config(state='disabled')
        senha_entry.config(state='disabled')
        numero_tel_entry.config(state="disabled")
        bt_novo_prof.config(state='disabled')
        bt_apagar_prof.config(state='disabled')
        bt_alterar_prof.config(state='disabled')
        bt_confirmar.config(state='disabled')
        bt_cancelar.config(state='disabled')
        cod_prof_entry.config(state="normal")
        cod_prof_entry.focus()

        
    #Função com a logica de registramento dos professores
    def cadastrar_prof():
        registro_prof = cod_prof_entry.get()
        nome_prof = nome_prof_entry.get()
        telefone_prof = numero_tel_entry.get()
        usuario_adm_prof = tipo_usuario_entry.get()
        senha_prof = senha_entry.get()
        if registro_prof == "" or nome_prof == "" or telefone_prof == "" or usuario_adm_prof == "" or senha_prof == "":
            messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
        else:
            try:
                    cursor = conexao.cursor()
                    cursor.execute("INSERT INTO professor (registro_prof, nome_prof, telefone_prof, usuario_adm_prof,senha_prof) VALUES (%s, %s, %s, %s, %s)", (registro_prof, nome_prof, telefone_prof, usuario_adm_prof,senha_prof))
                    conexao.commit()
            except mysql.connector.Error as erro:
                    print("Erro ao inserir os dados:", erro)
                    messagebox.showinfo("Mensagem", "Erro ao inserir os dados.")
            finally:
                    bt_novo_prof.config(state='disabled')
                    numero_tel_entry.config(state='disabled')
                    tipo_usuario_entry.config(state='disabled')
                    senha_entry.config(state='disabled')
                    nome_prof_entry
                    limpar_tabela()
                    lista_prof.delete(*lista_prof.get_children())
                    pesquisar_tabela_prof()
                    cod_prof_entry.config(state='normal')
                    cod_prof_entry.focus()


    def ocultar_senha(senha_prof):
        return '*' * len(senha_prof)

    #Função para mostrar toda tabela professores ao usuario 
    def pesquisar_tabela_prof():
        try:
            cursor = conexao.cursor()
            consulta_sql = "SELECT registro_prof, nome_prof, telefone_prof, usuario_adm_prof, senha_prof FROM professor ORDER BY nome_prof "
            cursor.execute(consulta_sql)
            resultados = cursor.fetchall()
            for linha in resultados:  
                linha_oculta = list(linha)
                linha_oculta[4] = ocultar_senha(linha[4])
                lista_prof.insert("", END, values=linha_oculta)
        except mysql.connector.Error as erro:
            print("Erro ao pesquisar o dado:", erro)
            messagebox.shoaskyesnowinfo("Mensagem", "Pesquisa não realizada.")  
        cod_prof_entry.focus()
 
            
    #Função para pesquisar um professor especifico
    def buscar_prof():
        try:
            cursor = conexao.cursor()
            texto_digitado = cod_prof_entry.get()
            cursor.execute("SELECT COUNT(*) FROM professor WHERE registro_prof = %s", (texto_digitado,))
            count = cursor.fetchone()[0]
            if count > 0:
                consulta_sql = "SELECT * FROM professor WHERE registro_prof = %s"
                cursor.execute(consulta_sql, (texto_digitado,))
                resultados = cursor.fetchall()
                bt_apagar_prof.config(state='normal')
                bt_alterar_prof.config(state='normal')
                nome_prof_entry.config(state='normal')
                tipo_usuario_entry.config(state='normal')
                senha_entry.config(state='normal', show="*")
                numero_tel_entry.config(state='normal')
                for linha in resultados:  
                    tipo_usuario_entry.delete(0, END)
                    senha_entry.delete(0, END)
                    numero_tel_entry.delete(0, END)
                    nome_prof_entry.insert(0, linha[1] )
                    numero_tel_entry.insert(0, linha[2] )
                    tipo_usuario_entry.insert(0, linha[3] )
                    senha_entry.insert(0, linha[4] )
                    nome_prof_entry.config(state='disabled')
                    tipo_usuario_entry.config(state='disabled')
                    senha_entry.config(state='disabled')
                    numero_tel_entry.config(state='disabled')     
                    bt_cancelar.config(state='disabled')     
                    bt_confirmar.config(state='disabled')     
            else:
                resposta = messagebox.askyesno("Mensagem", "Código não encontrado, deseja inserir um(a) novo(a) professor(a)?")
                if resposta:
                    nome_prof_entry.focus()
                    cod_prof_entry.config(state='disabled')
                    bt_novo_prof.config(state='normal')
                    nome_prof_entry.config(state='normal')
                    tipo_usuario_entry.config(state='normal')
                    senha_entry.config(state='normal')
                    numero_tel_entry.config(state='normal')
                    bt_alterar_prof.config(state='disabled')
                    bt_apagar_prof.config(state='disabled')
                    bt_cancelar.config(state='normal')
                    bt_confirmar.config(state='normal')

        except mysql.connector.Error as erro:
            print("Erro ao pesquisar o dado:", erro)
            messagebox.shoaskyesnowinfo("Mensagem", "Pesquisa não realizada.")

      
    #Função para abilitar os campos de digitação quando selecionado a opção de alterar      
    def alterar_professor():
        nome_prof_entry.config(state='normal')
        tipo_usuario_entry.config(state='normal')
        senha_entry.config(state='normal')
        numero_tel_entry.config(state='normal')
        bt_confirmar.config(state='normal')
        bt_cancelar.config(state='normal')
        bt_apagar_prof.config(state='disabled')
        bt_alterar_prof.config(state='disabled')
        cod_prof_entry.config(state='disabled')
        nome_prof_entry.focus()


      
    #Função para desabilitar os campos de digitação caso o usuario cancele a alteração  
    def alterar_prof_can():
        estado = bt_novo_prof.cget("state")
        if estado == "normal":
            nome_prof_entry.config(state='disabled')
            tipo_usuario_entry.config(state='disabled')
            senha_entry.config(state='disabled')
            numero_tel_entry.config(state='disabled')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')
            bt_apagar_prof.config(state='disabled')
            bt_alterar_prof.config(state='disabled')
            cod_prof_entry.config(state='normal')
            cod_prof_entry.focus()
        else:
            nome_prof_entry.config(state='disabled')
            tipo_usuario_entry.config(state='disabled')
            senha_entry.config(state='disabled')
            numero_tel_entry.config(state='disabled')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')
            bt_apagar_prof.config(state='normal')
            bt_alterar_prof.config(state='normal')
            cod_prof_entry.config(state='normal')
            cod_prof_entry.focus()



    #Função com a logica de alterar o professor
    def alterar_prof1():
        estado = bt_novo_prof.cget("state")
        if estado == "normal":
            cadastrar_prof()
        else:
            registro_prof = cod_prof_entry.get()
            nome_prof = nome_prof_entry.get()
            telefone_prof = numero_tel_entry.get()
            usuario_adm_prof = tipo_usuario_entry.get()
            senha_prof = senha_entry.get()
            if registro_prof == "" or nome_prof == "" or telefone_prof == "" or usuario_adm_prof == "" or senha_prof == "":
                messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
            else:
                try:

                    cursor = conexao.cursor()
                    cursor.execute("UPDATE professor SET nome_prof = %s, telefone_prof = %s, usuario_adm_prof = %s, senha_prof = %s WHERE registro_prof = %s",
                    (nome_prof, telefone_prof, usuario_adm_prof, senha_prof, registro_prof))
                    conexao.commit()
                except mysql.connector.Error as e:
                    print("Erro ao atualizar :", e)
                finally:
                    bt_confirmar.config(state='disabled')
                    bt_cancelar.config(state='disabled')
                    cod_prof_entry.config(state='normal')
                    limpar_tabela()
                    lista_prof.delete(*lista_prof.get_children())
                    pesquisar_tabela_prof()
                    cod_prof_entry.focus()

            
    #função para verificar se o usuario que realmente excluir um professor    
    def excluir_verificaçao():
        texto_digitado = cod_prof_entry.get()
        print("id digitado:", texto_digitado)
        resposta = messagebox.askyesno("EXCLUIR", f"Tem certeza que deseja excluir este professor?")
        if resposta:
            texto_digitado = cod_prof_entry.get()
            exluir_prof()      
        else:
            messagebox.showinfo("Mensagem", "Exclusão cancelada.")
        cod_prof_entry.focus()
     
     #função com a logica de exclusao do professor       
    def exluir_prof():
        try:
            cursor = conexao.cursor()
            texto_digitado = cod_prof_entry.get()
            cursor.execute("SELECT COUNT(*) FROM professor WHERE registro_prof = %s", (texto_digitado,))
            count = cursor.fetchone()[0]
            if count > 0:
                sql = "DELETE FROM professor WHERE registro_prof = %s"
                cursor.execute(sql, (texto_digitado,))
                conexao.commit()
                texto_digitado = cod_prof_entry.get()
                cursor.execute("SELECT COUNT(*) FROM professor WHERE registro_prof = %s", (texto_digitado,))
                count = cursor.fetchone()[0]
                if count == 0:
                    joiaa = 1
            else:
                messagebox.showinfo("Mensagem", "Exclusão não realizada.")
        except mysql.connector.Error as erro:
            print("Erro ao deletar o dado:", erro)
            messagebox.showinfo("ERRO", "Exclusão não realizada.")
        finally:
            limpar_tabela()
            lista_prof.delete(*lista_prof.get_children())
            pesquisar_tabela_prof() 
            cod_prof_entry.focus()
            
#==================================================================================================================================================#
         
    
    #Botoens da tela Professores   
    bt_limpar_prof = Button(frame_1, text= 'Limpar', command=limpar_tabela ,bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_limpar_prof.place(relx=0.14, rely=0.08, relwidth=0.1, relheight=0.14)
    
    bt_buscar_prof = Button(frame_1, command= buscar_prof, text='Buscar' ,  bg = '#107db2', fg = 'white')
    bt_buscar_prof.place(relx=0.26, rely=0.08, relwidth=0.1, relheight=0.14)
    #quando o usuario clicar no enter a funçao burcar professor especifica do id é selecionada
    janela.bind("<Return>", lambda event: buscar_prof())
    
    bt_novo_prof = Button(frame_1, command=cadastrar_prof,text='' , bg = 'SystemButtonFace',fg = 'white')
    bt_novo_prof.place(relx=1, rely=1, relwidth=0.01, relheight=0.01)    
    bt_novo_prof.config(state='disabled')

    bt_apagar_prof = Button(frame_1, command=excluir_verificaçao, text='Excluir' , bg = '#107db2',fg = 'white')
    bt_apagar_prof.place(relx=0.74, rely=0.08, relwidth=0.1, relheight=0.14)
    bt_apagar_prof.config(state='disabled')
    
    bt_alterar_prof = Button(frame_1, command= alterar_professor, text='Alterar' , bg = '#107db2',fg = 'white')
    bt_alterar_prof.place(relx=0.62, rely=0.08, relwidth=0.1, relheight=0.14)
    bt_alterar_prof.config(state='disabled')
    
    bt_confirmar = Button(frame_1, command= alterar_prof1, text= 'confirmar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_confirmar.place(relx=0.85, rely=0.08, relwidth=0.12, relheight=0.14)
    bt_confirmar.config(state='disabled')

    bt_cancelar = Button(frame_1, command= alterar_prof_can, text= 'Cancelar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_cancelar.place(relx=0.85, rely=0.25, relwidth=0.12, relheight=0.14)  
    bt_cancelar.config(state='disabled')
    
    bt_mudar_estoque = Button(frame_1, command=mudar_estoque, text= 'Estoque', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_estoque.place(relx=0.30, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_materiais = Button(frame_1, command=mudar_materiais, text= 'Materiais', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_materiais.place(relx=0.10, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_estoque_faltas = Button(frame_1, command=mudar_estoque_faltas, text= 'baixas', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_estoque_faltas.place(relx=0.50, rely=0.85, relwidth=0.15, relheight=0.15)
    
    #labels e campos de digitaçao 
    lb_cod_prof = Label(frame_1, text = "Registro", bg= '#dfe3ee', fg = '#107db2')
    lb_cod_prof.place(relx= 0.05, rely= 0.05 )
    cod_prof_entry = Entry(frame_1 )
    cod_prof_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)
    cod_prof_entry.focus()


    lb_nome_prof = Label(frame_1, text="Nome", bg= '#dfe3ee', fg = '#107db2')
    lb_nome_prof.place(relx=0.05, rely=0.35)
    nome_prof_entry= Entry(frame_1)
    nome_prof_entry.place(relx=0.05, rely=0.45, relwidth=0.4)
    nome_prof_entry.config(state='disabled')

    lb_numero_tel = Label(frame_1, text="Telefone", bg= '#dfe3ee', fg = '#107db2')
    lb_numero_tel.place(relx=0.5, rely=0.35)
    numero_tel_entry = Entry(frame_1)
    numero_tel_entry.place(relx=0.50, rely=0.45, relwidth=0.4)
    numero_tel_entry.config(state='disabled')

    lb_tipo_usuario = Label(frame_1, text="Tipo de usuário", bg= '#dfe3ee', fg = '#107db2')
    lb_tipo_usuario.place(relx=0.05, rely=0.6)
    tipo_usuario_entry = Entry(frame_1)
    tipo_usuario_entry.place(relx=0.05, rely=0.7, relwidth=0.4) 
    tipo_usuario_entry.config(state='disabled')

    lb_senha = Label(frame_1 , text="Senha", bg= '#dfe3ee', fg = '#107db2')
    lb_senha.place(relx=0.5, rely=0.6)
    senha_entry = Entry(frame_1)
    senha_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
    senha_entry.config(state='disabled')
    
   
    
    #Tabela que aparece na parte de baixo da tela com os registros vindos do banco de dados (tabela professor)
    lista_prof = ttk.Treeview(frame_2, height=3,column=("col1", "col2", "col3", "col4", "col5", "col6" ))
    lista_prof.heading("#0", text="")
    lista_prof.heading("#1", text="Registro")
    lista_prof.heading("#2", text="Nome")
    lista_prof.heading("#3", text="Telefone")
    lista_prof.heading("#4", text="Usuario ou Adm")
    lista_prof.heading("#5", text="Senha")
    lista_prof.column("#0", width=1)
    lista_prof.column("#1", width=120)
    lista_prof.column("#2", width=120)
    lista_prof.column("#3", width=120)
    lista_prof.column("#4", width=120)
    lista_prof.column("#5", width=120)
    lista_prof.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
    scroolLista = Scrollbar(frame_2, orient='vertical')
    lista_prof.configure(yscroll=scroolLista.set)
    scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
    
    #chama automaticamente pesquisar_tabela para que assim que o usuario clique ja apareça os registros
    pesquisar_tabela_prof()


#==================================================================================================================================================#
#MATERIAIS#

#Função para alterar até o CRUD da tabela materiais
def materiais(): 
    janela.title("ALMOXARIFADO MATERIAIS")
    conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="almoxarifado"
        ) 
    
    #Função para mudar até o CRUD da tabela posiçao_estoque
    def mudar_posicao_estoque():
        destoir_campos()
        pos_estoque()
      
      
    #Função para mudar até o CRUD da tabela professor  
    def mudar_professores():
        destoir_campos() 
        professores()
    
    
    #função para destroir os campos a fim de sair da tela materiais    
    def destoir_campos():
        bt_limpar_mat.destroy()
        bt_buscar_mat.destroy()
        bt_posicao_estoque.destroy()
        lb_cod_material.destroy()
        bt_posicao_estoque.destroy()
        bt_novo_mat.destroy()
        bt_alterar_mat.destroy()
        bt_apagar_mat.destroy()
        bt_mudar_prof.destroy()
        cod_mateiral_entry.destroy()
        lb_tipo_mat.destroy()
        tipo_mat_entry.destroy()
        tipo_mat_entry.destroy()
        lb_numero_bp_mat.destroy()
        numero_bp_mat_entry.destroy()
        lb_observacao_mat.destroy()
        observacao_mat_entry.destroy()
        lb_descricao_mat.destroy()
        descricao_mat_entry.destroy()
        bt_cancelar.destroy()
        bt_confirmar.destroy()
        bt_mudar_prof.destroy()
        bt_mudar_estoque_faltas.destroy()
        
    def mudar_estoque_faltas():
        destoir_campos()
        estoque_faltas()
        

    #Função para limpar os campos de digitação e a tabela inferior a fim de atualizar altomaticamente     
    def limpar_material():
        cod_mateiral_entry.config(state='normal')
        tipo_mat_entry.config(state='normal')
        numero_bp_mat_entry.config(state='normal')
        descricao_mat_entry.config(state='normal')
        observacao_mat_entry.config(state='normal')
        cod_mateiral_entry.delete(0, END)
        tipo_mat_entry.delete(0, END)
        numero_bp_mat_entry.delete(0, END)
        descricao_mat_entry.delete(0, END)
        observacao_mat_entry.delete(0, END)
        tipo_mat_entry.config(state='disabled')
        numero_bp_mat_entry.config(state='disabled')
        descricao_mat_entry.config(state='disabled')
        observacao_mat_entry.config(state='disabled')
        bt_confirmar.config(state='disabled')
        bt_cancelar.config(state='disabled')
        bt_alterar_mat.config(state='disabled')
        bt_apagar_mat.config(state='disabled')
        cod_mateiral_entry.config(state="normal")
        cod_mateiral_entry.focus()


     #Função com a logica para adicionar um novo material ao banco           
    def novo_material():
        codigo_mat = cod_mateiral_entry.get()
        tipo_mat = tipo_mat_entry.get()
        numero_bp_mat = numero_bp_mat_entry.get()
        descricao_mat = descricao_mat_entry.get()
        observacao_mat = observacao_mat_entry.get()
        if codigo_mat == "" or tipo_mat =="" or numero_bp_mat == "" or descricao_mat == "" or observacao_mat == "":
            messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
        else:
            try:
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO materiais (codigo_mat, tipo_mat, numero_bp_mat, descricao_mat, observacao_mat) VALUES (%s, %s, %s, %s, %s)", (codigo_mat, tipo_mat, numero_bp_mat, descricao_mat, observacao_mat))
                conexao.commit()
            except mysql.connector.Error as erro:
                print("Erro ao inserir os dados:", erro)
                messagebox.showinfo("Mensagem", "Erro ao inserir os dados.")
            finally:
                bt_novo_mat.config(state='disabled')
                tipo_mat_entry.config(state='disabled')
                numero_bp_mat_entry.config(state='disabled')
                observacao_mat_entry.config(state='disabled')
                descricao_mat_entry.config(state='disabled')
                tipo_mat_entry.delete(0, END)
                numero_bp_mat_entry.delete(0, END)
                observacao_mat_entry.delete(0, END)
                observacao_mat_entry.delete(0, END)
                descricao_mat_entry.delete(0, END)
                limpar_material()
                lista_materiais.delete(*lista_materiais.get_children())
                buscar_tabela_materiais()  
                cod_mateiral_entry.config(state="normal")
                cod_mateiral_entry.focus()


    #Função com a logica para buscar toda a tabela materiais
    def buscar_tabela_materiais():     
            try:
                cursor = conexao.cursor()
                consulta_sql = "SELECT * FROM materiais"
                cursor.execute(consulta_sql)
                resultados = cursor.fetchall()
                for linha in resultados:  
                    lista_materiais.insert("", END, values=linha)
            except mysql.connector.Error as erro:
                print("Erro ao pesquisar o dado:", erro)
                messagebox.shoaskyesnowinfo("Mensagem", "Pesquisa não realizada.")
         
                
    #Função com a logica para buscar um registro especifico na tabela materiais
    def pesquisar_texto_material():                
            try:
                cursor = conexao.cursor()
                texto_digitado = cod_mateiral_entry.get()
                cursor.execute("SELECT COUNT(*) FROM materiais WHERE codigo_mat = %s", (texto_digitado,))
                count = cursor.fetchone()[0]
                if count > 0:
                    consulta_sql = "SELECT * FROM materiais WHERE codigo_mat = %s"
                    cursor.execute(consulta_sql, (texto_digitado,))
                    resultados = cursor.fetchall()
                    bt_apagar_mat.config(state='normal')
                    bt_alterar_mat.config(state='normal')
                    numero_bp_mat_entry.delete(0, END) 
                    numero_bp_mat_entry.configure(state='disabled')
                    bt_novo_mat.config(state='disabled')
                    tipo_mat_entry.config(state='normal')
                    numero_bp_mat_entry.config(state='normal')
                    observacao_mat_entry.config(state='normal')
                    descricao_mat_entry.config(state='normal')
                    for linha in resultados:  
                        descricao_mat_entry.delete(0, END) 
                        tipo_mat_entry.delete(0, END)
                        numero_bp_mat_entry.delete(0, END)
                        observacao_mat_entry.delete(0, END)
                        tipo_mat_entry.insert(0, linha[1] )
                        numero_bp_mat_entry.insert(0, linha[2] )
                        observacao_mat_entry.insert(0, linha[4] )
                        descricao_mat_entry.insert(0, linha[3] )
                        tipo_mat_entry.config(state='disabled')
                        numero_bp_mat_entry.config(state='disabled')
                        observacao_mat_entry.config(state='disabled')
                        descricao_mat_entry.config(state='disabled')
                        bt_confirmar.config(state='disabled')
                        bt_cancelar.config(state='disabled')
                else:
                    resposta = messagebox.askyesno("Mensagem", "Código não encontrado, deseja adicionar um novo material?")
                    if resposta:
                        cod_mateiral_entry.config(state='disabled')
                        bt_novo_mat.config(state='normal')
                        tipo_mat_entry.config(state='normal')
                        numero_bp_mat_entry.config(state='normal')
                        observacao_mat_entry.config(state='normal')
                        descricao_mat_entry.config(state='normal')
                        bt_alterar_mat.config(state='disabled')
                        bt_apagar_mat.config(state='disabled')
                        bt_cancelar.config(state='normal')     
                        bt_confirmar.config(state='normal')  
                        tipo_mat_entry.focus() 
                        
            except mysql.connector.Error as erro:
                print("Erro ao pesquisar o dado:", erro)
                messagebox.shoaskyesnowinfo("Mensagem", "Pesquisa não realizada.")
                
                
    #Função para abilitar os campos de digitação para alterar dados do material            
    def alterar_materiais():
        tipo_mat_entry.config(state='normal')
        numero_bp_mat_entry.config(state='normal')
        observacao_mat_entry.config(state='normal')
        descricao_mat_entry.config(state='normal')
        bt_confirmar.config(state='normal')
        bt_cancelar.config(state='normal')
        bt_apagar_mat.config(state='disabled')
        bt_alterar_mat.config(state='disabled')
        cod_mateiral_entry.config(state='disabled')
        tipo_mat_entry.focus()

    #Função para desabiliatar os campos caso o usuario cancele a alteração
    def alterar_materiais_canc():
        if bt_novo_mat.winfo_exists():
            tipo_mat_entry.config(state='disabled')
            numero_bp_mat_entry.config(state='disabled')
            observacao_mat_entry.config(state='disabled')
            descricao_mat_entry.config(state='disabled')
            cod_mateiral_entry.config(state='normal')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')
            bt_alterar_mat.config(state='disabled')
            bt_apagar_mat.config(state='disabled')
            cod_mateiral_entry.focus()

        else:
            
            tipo_mat_entry.config(state='disabled')
            numero_bp_mat_entry.config(state='disabled')
            observacao_mat_entry.config(state='disabled')
            descricao_mat_entry.config(state='disabled')
            cod_mateiral_entry.config(state='normal')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')
            bt_alterar_mat.config(state='normal')
            bt_apagar_mat.config(state='normal')
            cod_mateiral_entry.focus()

    
    #Função para alterar materiais
    def alterar_materiais1():
        estado = bt_novo_mat.cget("state")
        if estado == "normal":
            novo_material()
        else:
            codigo_mat = cod_mateiral_entry.get()
            tipo_mat = tipo_mat_entry.get()
            numero_bp_mat = numero_bp_mat_entry.get()
            descricao_mat = descricao_mat_entry.get()
            observacao_mat = observacao_mat_entry.get()
            if codigo_mat == "" or tipo_mat =="" or numero_bp_mat == "" or descricao_mat == "" or observacao_mat == "":
                messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
            else:
                try:

                    cursor = conexao.cursor()
                    cursor.execute("UPDATE materiais SET tipo_mat = %s, numero_bp_mat = %s, descricao_mat = %s, observacao_mat = %s WHERE codigo_mat = %s", 
                    (tipo_mat, numero_bp_mat, descricao_mat, observacao_mat, codigo_mat))
                    conexao.commit()
                except mysql.connector.Error as e:
                    print("Erro ao atualizar :", e)
                finally:
                    tipo_mat_entry.config(state='disabled')
                    numero_bp_mat_entry.config(state='disabled')
                    observacao_mat_entry.config(state='disabled')
                    descricao_mat_entry.config(state='disabled')
                    bt_confirmar.config(state='disabled')
                    bt_cancelar.config(state='disabled')
                    cod_mateiral_entry.config(state='normal')
                    cod_mateiral_entry.focus()

                    limpar_material()
                    lista_materiais.delete(*lista_materiais.get_children())
                    buscar_tabela_materiais()
                
    #Função para verificar se o usuario deseja realmente excluir um registro da tabela materiais
    def excluir_verificacao():
        texto_digitado = cod_mateiral_entry.get()
        print("id digitado:", texto_digitado)
        resposta = messagebox.askyesno("EXCLUIR", f"Tem certeza que deseja excluir este material?")
        if resposta:
            texto_digitado = cod_mateiral_entry.get()
            delete_material()      
        else:
            messagebox.showinfo("Mensagem", "Operação cancelada.")

    #Função com a logica de exclusão de um registro 
    def delete_material():
        try:
            cursor = conexao.cursor()
            texto_digitado = cod_mateiral_entry.get()
            cursor.execute("SELECT COUNT(*) FROM materiais WHERE codigo_mat = %s", (texto_digitado,))
            count = cursor.fetchone()[0]
            if count > 0:
                sql = "DELETE FROM materiais WHERE codigo_mat = %s"
                cursor.execute(sql, (texto_digitado,))
                conexao.commit()
                texto_digitado = cod_mateiral_entry.get()
                cursor.execute("SELECT COUNT(*) FROM materiais WHERE codigo_mat = %s", (texto_digitado,))
                count = cursor.fetchone()[0]
                if count == 0:
                    joiaa = 1
            else:
                messagebox.showinfo("Mensagem", "Exclusão não realizada.")
        except mysql.connector.Error as erro:
            print("Erro ao deletar o dado:", erro)
            messagebox.showinfo("ERRO", "exclusão não realizada. Verifique se não ha posição no estoque referente a este código, se não houver tente novamente")
        finally:
            limpar_material()
            lista_materiais.delete(*lista_materiais.get_children())
            buscar_tabela_materiais()
    
    
 #==================================================================================================================================================#
         
    
    #Botoens da tela materiais   
    bt_limpar_mat = Button(frame_1, command=limpar_material, text= 'Limpar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_limpar_mat.place(relx=0.14, rely=0.08, relwidth=0.1, relheight=0.14)
            
    bt_buscar_mat = Button(frame_1, text='Buscar' ,command=pesquisar_texto_material,  bg = '#107db2', fg = 'white')
    bt_buscar_mat.place(relx=0.26, rely=0.08, relwidth=0.1, relheight=0.14)
    #quando o usuario clicar no enter a funçao burcar professor especifica do id é selecionada
    janela.bind("<Return>", lambda event: pesquisar_texto_material())
    
    bt_novo_mat = Button(frame_1, text='' , command = novo_material,bg = 'SystemButtonFace',fg = 'white')
    bt_novo_mat.place(relx=1, rely=1, relwidth=0.01, relheight=0.01)    
    bt_novo_mat.config(state='disabled')
    
    bt_apagar_mat = Button(frame_1, text='Excluir' ,command=excluir_verificacao, bg = '#107db2',fg = 'white')
    bt_apagar_mat.place(relx=0.74, rely=0.08, relwidth=0.1, relheight=0.14)
    bt_apagar_mat.config(state='disabled')
    
    bt_alterar_mat = Button(frame_1, text='Alterar' , command = alterar_materiais, bg = '#107db2',fg = 'white')
    bt_alterar_mat.place(relx=0.62, rely=0.08, relwidth=0.1, relheight=0.14)
    bt_alterar_mat.config(state='disabled')
    
    bt_confirmar = Button(frame_1, command=alterar_materiais1, text= 'Confirmar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_confirmar.place(relx=0.85, rely=0.08, relwidth=0.12, relheight=0.14)
    bt_confirmar.config(state='disabled')

    bt_cancelar = Button(frame_1, command=alterar_materiais_canc, text= 'Cancelar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_cancelar.place(relx=0.85, rely=0.25, relwidth=0.12, relheight=0.14) 
    bt_cancelar.config(state='disabled')
    
    bt_posicao_estoque = Button(frame_1, command=mudar_posicao_estoque, text= 'Estoque', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_posicao_estoque.place(relx=0.30, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_prof = Button(frame_1, command=mudar_professores, text= 'Professores', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_prof.place(relx=0.10, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_estoque_faltas = Button(frame_1, command=mudar_estoque_faltas, text= 'baixas', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_estoque_faltas.place(relx=0.50, rely=0.85, relwidth=0.15, relheight=0.15)
    
    #labels e campos de digitaçao 
    lb_cod_material = Label(frame_1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
    lb_cod_material.place(relx= 0.05, rely= 0.05 )
    cod_mateiral_entry = Entry(frame_1 )
    cod_mateiral_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)
    cod_mateiral_entry.focus()


    lb_tipo_mat = Label(frame_1, text="Tipo(E / F / C)", bg= '#dfe3ee', fg = '#107db2')
    lb_tipo_mat.place(relx=0.05, rely=0.35)
    tipo_mat_entry= Entry(frame_1)
    tipo_mat_entry.place(relx=0.05, rely=0.45, relwidth=0.4)
    tipo_mat_entry.config(state='disabled')
        
    lb_descricao_mat = Label(frame_1, text="Descrição (nome)", bg= '#dfe3ee', fg = '#107db2')
    lb_descricao_mat.place(relx=0.5, rely=0.35)
    descricao_mat_entry = Entry(frame_1)
    descricao_mat_entry.place(relx=0.50, rely=0.45, relwidth=0.4)
    descricao_mat_entry.config(state='disabled')

    lb_numero_bp_mat = Label(frame_1, text="Numero BP", bg= '#dfe3ee', fg = '#107db2')
    lb_numero_bp_mat.place(relx=0.05, rely=0.6)
    numero_bp_mat_entry = Entry(frame_1)
    numero_bp_mat_entry.place(relx=0.05, rely=0.7, relwidth=0.4) 
    numero_bp_mat_entry.config(state='disabled')

    lb_observacao_mat = Label(frame_1, text="Observação", bg= '#dfe3ee', fg = '#107db2')
    lb_observacao_mat.place(relx=0.5, rely=0.6)
    observacao_mat_entry = Entry(frame_1)
    observacao_mat_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
    observacao_mat_entry.config(state='disabled')
    
    #Tabela que aparece na parte de baixo da tela com os registros vindos do banco de dados (tabela materiais)
    lista_materiais = ttk.Treeview(frame_2, height=3,column=("col1", "col2", "col3", "col4", "col5"))
    lista_materiais.heading("#0", text="")
    lista_materiais.heading("#1", text="código")
    lista_materiais.heading("#2", text="tipo")
    lista_materiais.heading("#3", text="numero")
    lista_materiais.heading("#4", text="descrição")
    lista_materiais.heading("#5", text="observação")
    lista_materiais.column("#0", width=1)
    lista_materiais.column("#1", width=100)
    lista_materiais.column("#2", width=100)
    lista_materiais.column("#3", width=100)
    lista_materiais.column("#4", width=100)
    lista_materiais.column("#5", width=100)
    lista_materiais.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
    scroolLista = Scrollbar(frame_2, orient='vertical')
    lista_materiais.configure(yscroll=scroolLista.set)
    scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
    
    #chama automaticamente buscar_tabela_materiais para que assim que o usuario clique ja apareça os registros
    buscar_tabela_materiais()
    
    
#==================================================================================================================================================#
#ESTOQUE#

#Função para alterar até o CRUD da tabela pos_estoque
def pos_estoque():
    janela.title("ALMOXARIFADO ESTOQUE")
    conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="almoxarifado"
        )
    #Função para mudar até o CRUD da tabela professor
    def mudar_professores():
        destroir_campos()
        professores()
        
        
    #Função para mudar até o CRUD da tabela matetriais
    def mudar_materiais():
        destroir_campos()
        materiais()
        
    def mudar_estoque_faltas():
        destroir_campos()
        estoque_faltas()
        
    #Função para destroir os campos a fim de sair da tela pos_estoque    
    def destroir_campos():
        bt_limpar.destroy()
        bt_buscar.destroy()
        bt_materiais.destroy()
        lb_cod_pos_estoque.destroy()
        cod_pos_estoque_entry.destroy()
        lb_quant_min_pos.destroy()
        quant_min_pos_entry.destroy()
        lb_quant_atual_pos.destroy()
        quant_atual_pos_entry.destroy()
        lb_quant_max_pos.destroy()
        quant_max_pos_entry.destroy() 
        bt_novo.destroy() 
        bt_apagar.destroy() 
        bt_alterar.destroy()
        bt_cancelar.destroy()
        bt_confirmar.destroy()
        bt_mudar_prof.destroy()
        bt_mudar_estoque_faltas.destroy()

    #Função para limpar os campos de digitação e a tabela inferior 
    def limpar_texto_estoque():
        quant_min_pos_entry.config(state='normal')
        quant_atual_pos_entry.config(state='normal')
        quant_max_pos_entry.config(state='normal')
        cod_pos_estoque_entry.delete(0, END)
        quant_min_pos_entry.delete(0, END)
        quant_atual_pos_entry.delete(0, END)
        quant_max_pos_entry.delete(0, END)
        quant_min_pos_entry.config(state='disabled')
        quant_atual_pos_entry.config(state='disabled')
        quant_max_pos_entry.config(state='disabled')
        bt_novo.config(state='disabled')
        bt_alterar.config(state='disabled')
        bt_apagar.config(state='disabled')
        bt_confirmar.config(state='disabled')
        bt_cancelar.config(state='disabled')
        cod_pos_estoque_entry.config(state="normal")
        cod_pos_estoque_entry.focus()

        
    #Função com a logica para cadastrar uma nova posição no estoque  
    def novo_pos_estoque():
        codigo_pos_estoque = cod_pos_estoque_entry.get()
        qnt_min_estoque = quant_min_pos_entry.get()
        qnt_atual_estoque = quant_atual_pos_entry.get()
        qnt_max_estoque = quant_max_pos_entry.get()
        cursor = conexao.cursor()
        if  qnt_min_estoque == "" or qnt_max_estoque == "" or qnt_atual_estoque == "" :
            messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
        else: 
            qnt_min_estoque = int (qnt_min_estoque)
            qnt_max_estoque = int (qnt_max_estoque)
            qnt_atual_estoque = int (qnt_atual_estoque)
            if qnt_atual_estoque < qnt_min_estoque:
                messagebox.showinfo("Mensagem", "Quantidade atual inferior a minima, quantidade baixa de estoque!")
            if qnt_min_estoque > qnt_max_estoque or qnt_min_estoque < 0 or qnt_max_estoque < 0 or qnt_atual_estoque < 0 :
                messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")

            else:
                qnt_min_estoque = str (qnt_min_estoque)
                qnt_max_estoque = str (qnt_max_estoque)
                qnt_atual_estoque = str (qnt_atual_estoque)
                try:
                        cursor.execute("INSERT INTO posicao_estoque (codigo_pos, quant_min_pos, quant_atual_pos, quant_max_pos) VALUES (%s, %s, %s, %s)", (codigo_pos_estoque, qnt_min_estoque, qnt_atual_estoque, qnt_max_estoque))
                        conexao.commit()
                except mysql.connector.Error as erro:
                        print("Erro ao inserir os dados:", erro)
                        messagebox.showinfo("Mensagem", "Erro ao inserir a posição.")
                finally:
                        bt_novo.config(state='disabled')
                        quant_min_pos_entry.config(state='disabled')
                        quant_atual_pos_entry.config(state='disabled')
                        quant_max_pos_entry.config(state='disabled')
                        quant_min_pos_entry.delete(0, END)
                        quant_atual_pos_entry.delete(0, END)
                        quant_max_pos_entry.delete(0, END)
                        limpar_texto_estoque()
                        lista_pos.delete(*lista_pos.get_children())
                        buscar_tabela_posicao_estoque()
                        cod_pos_estoque_entry.config(state="normal")
                        cod_pos_estoque_entry.focus()

                
    #Função para pesquisar toda a tabela pos_estoque
    def buscar_tabela_posicao_estoque():     
        try:
            cursor = conexao.cursor()
            consulta_sql = "SELECT posicao_estoque.codigo_pos, posicao_estoque.quant_min_pos, posicao_estoque.quant_atual_pos, posicao_estoque.quant_max_pos, materiais.descricao_mat FROM posicao_estoque INNER JOIN materiais ON posicao_estoque.codigo_pos = materiais.codigo_mat"
            cursor.execute(consulta_sql)
            resultados = cursor.fetchall()
            for linha in resultados:  
                lista_pos.insert("", END, values=linha)
        except mysql.connector.Error as erro:
            print("Erro ao pesquisar o dado:", erro)
            messagebox.shoaskyesnowinfo("Mensagem", "pesquisa não realizada.")
            
    #Função para pesquisar um registro espesifico na tabela pos_estoque
    def pesquisar_texto_pos():
        try:
            cursor = conexao.cursor()
            texto_digitado = cod_pos_estoque_entry.get()
            cursor.execute("SELECT COUNT(*) FROM posicao_estoque WHERE codigo_pos = %s", (texto_digitado,))
            count = cursor.fetchone()[0]
            if count > 0:
                bt_alterar.config(state='normal')
                bt_apagar.config(state='normal')
                bt_novo.config(state='disabled')
                quant_min_pos_entry.config(state='normal')
                quant_atual_pos_entry.config(state='normal')
                quant_max_pos_entry.config(state='normal')             
                consulta_sql = "SELECT * FROM posicao_estoque WHERE codigo_pos = %s"
                cursor.execute(consulta_sql, (texto_digitado,))
                resultados = cursor.fetchall()
                for linha in resultados:  
                        quant_min_pos_entry.delete(0, END) 
                        quant_atual_pos_entry.delete(0, END)
                        quant_max_pos_entry.delete(0, END) 
                        quant_min_pos_entry.insert(0, linha[1] )
                        quant_atual_pos_entry.insert(0, linha[2] )
                        quant_max_pos_entry.insert(0, linha[3] )
                        quant_min_pos_entry.config(state='disabled')
                        quant_atual_pos_entry.config(state='disabled')
                        quant_max_pos_entry.config(state='disabled')     
                        bt_cancelar.config(state='disabled')     
                        bt_confirmar.config(state='disabled')     
            else:
                resposta = messagebox.askyesno("Nova posição?", "Código nao encontrado, deseja criar uma nova posição?")
                if resposta:
                    texto_digitado = cod_pos_estoque_entry.get()
                    cursor.execute("SELECT COUNT(*) FROM materiais WHERE codigo_mat = %s", (texto_digitado,))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        
                        bt_confirmar.config(state='normal')
                        bt_cancelar.config(state='normal')
                        cod_pos_estoque_entry.config(state='disabled')
                        bt_novo.config(state='normal')
                        quant_min_pos_entry.config(state='normal')
                        quant_atual_pos_entry.config(state='normal')
                        quant_max_pos_entry.config(state='normal')
                        bt_alterar.config(state='disabled')
                        bt_apagar.config(state='disabled') 
                        quant_min_pos_entry.focus() 
                    else:
                        messagebox.showinfo("Mensagem", "Codigo não relacionado a materiais, verifique e tente novamente.")

                        
        except mysql.connector.Error as erro:
                print("Erro ao pesquisar o dado:", erro)
                messagebox.showinfo("Mensagem", "Pesquisa não realizada.")
                
    #Função para abilitar os campos de digitação para alterar dados do estoque
    def alterar_pos_estoque():
        quant_min_pos_entry.config(state='normal')
        quant_atual_pos_entry.config(state='normal')
        quant_max_pos_entry.config(state='normal')
        bt_confirmar.config(state='normal')
        bt_cancelar.config(state='normal')
        bt_apagar.config(state='disabled')
        bt_alterar.config(state='disabled')
        cod_pos_estoque_entry.config(state='disabled')
        quant_min_pos_entry.focus()
        
    #Função para desabiliatar os campos caso o usuario cancele a alteração
    def alterar_pos_canc():
        estado = bt_novo.cget("state")
        if estado == "normal":
            quant_min_pos_entry.config(state='disabled')
            quant_atual_pos_entry.config(state='disabled')
            quant_max_pos_entry.config(state='disabled')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')
            bt_alterar.config(state='disabled')
            bt_apagar.config(state='disabled')
            cod_pos_estoque_entry.config(state='normal')
            cod_pos_estoque_entry.focus()
            
        else:
                
            quant_min_pos_entry.config(state='disabled')
            quant_atual_pos_entry.config(state='disabled')
            quant_max_pos_entry.config(state='disabled')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')
            bt_alterar.config(state='normal')
            bt_apagar.config(state='normal')
            cod_pos_estoque_entry.config(state='normal')
            cod_pos_estoque_entry.focus()

                           
                           
    #Função com a logica alterar materiais
    def alterar_pos1():
        estado = bt_novo.cget("state")
        if estado == "normal":
            novo_pos_estoque()
        else:
            qnt_min_estoque = quant_min_pos_entry.get()
            qnt_atual_estoque = quant_atual_pos_entry.get()
            qnt_max_estoque = quant_max_pos_entry.get()
            cod_pos_estoque = cod_pos_estoque_entry.get()
            cursor = conexao.cursor()
            cursor = conexao.cursor()
            consulta = "SELECT quant_atual_pos FROM posicao_estoque WHERE codigo_pos = %s"
            atual_banco = (cod_pos_estoque,)
            cursor.execute(consulta, atual_banco)
            atual_banco = cursor.fetchone()[0]

            if  qnt_min_estoque == "" or qnt_max_estoque == "" or qnt_atual_estoque == "" :
                messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
            else: 
                qnt_min_estoque = int (qnt_min_estoque)
                qnt_max_estoque = int (qnt_max_estoque)
                qnt_atual_estoque = int (qnt_atual_estoque)
                if qnt_atual_estoque < qnt_min_estoque:
                    messagebox.showinfo("Mensagem", "Quantidade atual inferior a minima, quantidade baixa de estoque!")
                if qnt_min_estoque > qnt_max_estoque or qnt_min_estoque < 0 or qnt_max_estoque < 0 or qnt_atual_estoque < 0 :
                    messagebox.showinfo("Mensagem", "Verifique se os dados correspondem a valores válidos, e tente novamente.")
                else:
                    if atual_banco == qnt_atual_estoque:
                        alterar_pos_estoque2()
                    else:
                        resposta = messagebox.askyesno("Mensagem ", "Tem certeza que deseja alterar a quantidade atual?")
                        if resposta:
                            alterar_pos_estoque2()
                        else:
                            alterar_pos_canc()

                        

    def alterar_pos_estoque2():
        try:
            cod_pos = cod_pos_estoque_entry.get()
            quant_min = quant_min_pos_entry.get()
            quant_atual = quant_atual_pos_entry.get()
            quant_max = quant_max_pos_entry.get()
            cursor = conexao.cursor()
            cursor.execute("UPDATE posicao_estoque SET quant_min_pos = %s, quant_atual_pos = %s, quant_max_pos = %s WHERE codigo_pos = %s", 
            (quant_min, quant_atual, quant_max, cod_pos))
            conexao.commit()
        except mysql.connector.Error as e:
            print("Erro ao atualizar :", e)
        finally:
            quant_min_pos_entry.config(state='disabled')
            quant_atual_pos_entry.config(state='disabled')
            quant_max_pos_entry.config(state='disabled')
            bt_confirmar.config(state='disabled')
            bt_cancelar.config(state='disabled')

            limpar_texto_estoque()
            lista_pos.delete(*lista_pos.get_children())
            buscar_tabela_posicao_estoque()
            cod_pos_estoque_entry.config(state='normal')
            cod_pos_estoque_entry.focus()

                
    #Função para verificar se o usuario deseja realmente excluir um registro da tabela pos_estoque
    def excluir_verificacao():
        texto_digitado = cod_pos_estoque_entry.get()
        print("id digitado:", texto_digitado)
        resposta = messagebox.askyesno("EXCLUIR", f"Tem certeza que deseja excluir esta posição?")
        if resposta:
            texto_digitado = cod_pos_estoque_entry.get()
            delete_pos_estoque()      
        else:
            messagebox.showinfo("Mensagem", "Operação cancelada.")
    
    #Função com a logica de exclusão de um registro 
    def delete_pos_estoque():
        try:
            cursor = conexao.cursor()
            texto_digitado = cod_pos_estoque_entry.get()
            cursor.execute("SELECT COUNT(*) FROM posicao_estoque WHERE codigo_pos = %s", (texto_digitado,))
            count = cursor.fetchone()[0]
            if count > 0:
                sql = "DELETE FROM posicao_estoque WHERE codigo_pos = %s"
                cursor.execute(sql, (texto_digitado,))
                conexao.commit()
            else:
                messagebox.showinfo("ERRO", "Exclusão não realizada. Código não encontrado")
        except mysql.connector.Error as erro:
            print("Erro ao deletar o dado:", erro)
            messagebox.showinfo("Mensagem", "Exclusão não realizada.")
        finally:
            limpar_texto_estoque()
            lista_pos.delete(*lista_pos.get_children())
            buscar_tabela_posicao_estoque()
            cod_pos_estoque_entry.focus()


 #==================================================================================================================================================#
  
    #Botoens da tela estoque
    bt_limpar = Button(frame_1, command=limpar_texto_estoque, text= 'Limpar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_limpar.place(relx=0.14, rely=0.08, relwidth=0.1, relheight=0.14)
            
    bt_buscar = Button(frame_1, text='Buscar' ,command=pesquisar_texto_pos,  bg = '#107db2', fg = 'white')
    bt_buscar.place(relx=0.26, rely=0.08, relwidth=0.1, relheight=0.14)
    #quando o usuario clicar no enter a funçao burcar professor especifica do id é selecionada
    janela.bind("<Return>", lambda event: pesquisar_texto_pos())   

    bt_novo = Button(frame_1, text='' , command = novo_pos_estoque,bg = 'SystemButtonFace',fg = 'white')
    bt_novo.place(relx=1, rely=1, relwidth=0.01, relheight=0.01)
    bt_novo.config(state='disabled')

    bt_apagar = Button(frame_1, text='Excluir' ,command=excluir_verificacao, bg = '#107db2',fg = 'white')
    bt_apagar.place(relx=0.74, rely=0.08, relwidth=0.1, relheight=0.14)
    bt_apagar.config(state='disabled')

    bt_alterar = Button(frame_1, text='Alterar' ,command=alterar_pos_estoque, bg = '#107db2',fg = 'white')
    bt_alterar.place(relx=0.62, rely=0.08, relwidth=0.1, relheight=0.14)
    bt_alterar.config(state='disabled')
    
    bt_confirmar = Button(frame_1, command=alterar_pos1, text= 'Confirmar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_confirmar.place(relx=0.85, rely=0.08, relwidth=0.12, relheight=0.14)
    bt_confirmar.config(state='disabled')

    bt_cancelar = Button(frame_1, command=alterar_pos_canc, text= 'Cancelar', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_cancelar.place(relx=0.85, rely=0.25, relwidth=0.12, relheight=0.14)  
    bt_cancelar.config(state='disabled')
    
    bt_materiais = Button(frame_1, command=mudar_materiais, text= 'Materiais', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_materiais.place(relx=0.30, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_prof = Button(frame_1, command=mudar_professores, text= 'Professores', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_prof.place(relx=0.10, rely=0.85, relwidth=0.15, relheight=0.15)
    
    bt_mudar_estoque_faltas = Button(frame_1, command=mudar_estoque_faltas, text= 'baixas', bg = '#107db2', fg = 'white', font= ("verdana", 10, "bold"))
    bt_mudar_estoque_faltas.place(relx=0.50, rely=0.85, relwidth=0.15, relheight=0.15)
    
    #labels e campos de digitaçao 
    
    lb_cod_pos_estoque = Label(frame_1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
    lb_cod_pos_estoque.place(relx= 0.05, rely= 0.05 )
    cod_pos_estoque_entry = Entry(frame_1 )
    cod_pos_estoque_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)
    cod_pos_estoque_entry.focus()

    lb_quant_min_pos = Label(frame_1, text="Quantidade mínima", bg= '#dfe3ee', fg = '#107db2')
    lb_quant_min_pos.place(relx=0.05, rely=0.35)
    quant_min_pos_entry= Entry(frame_1)
    quant_min_pos_entry.place(relx=0.05, rely=0.45, relwidth=0.8)
    quant_min_pos_entry.config(state='disabled')

    lb_quant_atual_pos = Label(frame_1, text="Quantidade atual", bg= '#dfe3ee', fg = '#107db2')
    lb_quant_atual_pos.place(relx=0.05, rely=0.6)
    quant_atual_pos_entry = Entry(frame_1)
    quant_atual_pos_entry.place(relx=0.05, rely=0.7, relwidth=0.4)
    quant_atual_pos_entry.config(state='disabled')

    lb_quant_max_pos = Label(frame_1, text="Quantidade máxima", bg= '#dfe3ee', fg = '#107db2')
    lb_quant_max_pos.place(relx=0.5, rely=0.6)
    quant_max_pos_entry = Entry(frame_1)
    quant_max_pos_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
    quant_max_pos_entry.config(state='disabled')

    #Tabela que aparece na parte de baixo da tela com os registros vindos do banco de dados (tabela pos_estoque)
    
    lista_pos = ttk.Treeview(frame_2, height=3,column=("col1", "col2", "col3", "col4", "col5", "col6" ))
    lista_pos.heading("#0", text="")
    lista_pos.heading("#1", text="Código")
    lista_pos.heading("#2", text="Quantidade miníma")
    lista_pos.heading("#3", text="Quantidade atual")
    lista_pos.heading("#4", text="Quantidade máxima")
    lista_pos.heading("#5", text="Material")
    lista_pos.column("#0", width=1)
    lista_pos.column("#1", width=120)
    lista_pos.column("#2", width=120)
    lista_pos.column("#3", width=120)
    lista_pos.column("#4", width=120)
    lista_pos.column("#5", width=120)
    lista_pos.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
    
    #chama automaticamente pesquisar_tabela para que assim que o usuario clique ja apareça os registros
    buscar_tabela_posicao_estoque()
    scroolLista = Scrollbar(frame_2, orient='vertical')
    lista_pos.configure(yscroll=scroolLista.set)
    scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
    
#chama a função pos_estoque para que seja a primeira tela ao entrar no programa 
pos_estoque()
#mantem a janela aberta sem que se feche assim que clique em entrar
janela.mainloop()