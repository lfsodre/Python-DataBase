import tkinter as tk
import psycopg2
from datetime import datetime

#-----------------CONECTAR AO BANCO DE DADOS-----------------#
conn = psycopg2.connect(database="faculdade", user="postgres", password="235722", host="localhost", port="5432")
cursor = conn.cursor()

try:
    sql='CREATE DATABASE faculdade'
    cursor.execute(sql)
    conn.commit()
    sql='CREATE TABLE notas (id SERIAL PRIMARY KEY,matricula VARCHAR(10),nome VARCHAR(100),nota FLOAT)'
    cursor.execute(sql)
    conn.commit()
    sql='CREATE TABLE ajustes_notas (id SERIAL PRIMARY KEY,matricula_aluno VARCHAR(10),nome_aluno VARCHAR(100),nota_anterior FLOAT,nova_nota FLOAT,motivo TEXT,data_hora TIMESTAMP)'
    cursor.execute(sql)
    conn.commit()
except Exception as e:
    print ("Database/Tabela já criado(a).")
    conn.rollback()

def cadastrar_nota():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    nota = float(entry_nota.get())
    
    #------------INSERIR NOTA------------#
    cursor.execute("INSERT INTO notas (matricula, nome, nota) VALUES (%s, %s, %s)", (matricula, nome, nota))
    conn.commit()
    
    #-----------LIMPAR CAMPOS------------#
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_nota.delete(0, tk.END)

def consultar_nota():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    
    #------------------CONSULTAR NOTA------------------#
    cursor.execute("SELECT nota FROM notas WHERE matricula = %s AND nome = %s", (matricula, nome))
    nota = cursor.fetchone()
    
    if nota:
        label_resultado.config(text=f"Nota: {nota[0]}")
    else:
        label_resultado.config(text="Aluno não encontrado")
        
#--------------FUNÇÃO AJUSTAR NOTA-------------#
def ajustar_nota():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    nova_nota = float(entry_nova_nota.get())
    motivo = entry_motivo.get()
    
    #-------------CONSULTAR NOTA-------------#
    cursor.execute("SELECT nota FROM notas WHERE matricula = %s AND nome = %s", (matricula, nome))
    nota_atual = cursor.fetchone()
    
    if nota_atual:
        nota_atual = nota_atual[0]
        
        #------------------ATUALIZAR NOTA E GERAR REGISTRO------------------#
        cursor.execute("UPDATE notas SET nota = %s WHERE matricula = %s AND nome = %s", (nova_nota, matricula, nome))
        conn.commit()
        
        #------------------REGISTRAR ALTERAÇÃO------------------#
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ajustes_notas (matricula_aluno, nome_aluno, nota_anterior, nova_nota, motivo, data_hora) VALUES (%s, %s, %s, %s, %s, %s)", (matricula, nome, nota_atual, nova_nota, motivo, data_hora))
        conn.commit()
        
        label_resultado.config(text=f"Nota ajustada para {nova_nota}")
    else:
        label_resultado.config(text="Aluno não encontrado")

def verificar_status():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    
    #------------------CONSULTAR NOTA------------------#
    cursor.execute("SELECT nota FROM notas WHERE matricula = %s AND nome = %s", (matricula, nome))
    nota = cursor.fetchone()
    
    if nota:
        nota = nota[0]
        if nota >= 6.0:
            label_status.config(text="Aprovado")
        elif nota >= 4.0:
            label_status.config(text="Exame")
        else:
            label_status.config(text="Reprovado")
    else:
            label_status.config(text="Aluno não encontrado")
            
#----------------TKINTER--------------------------#
root = tk.Tk()
root.title("GESTÃO DE NOTAS")
root.geometry('300x300')

#-----------------WIDGET--------------------------#
label_matricula = tk.Label  (root, text="Matrícula:")
label_nome = tk.Label       (root, text="Nome:")
label_nota = tk.Label       (root, text="Nota:")
label_nova_nota = tk.Label  (root, text="Nova Nota:")
label_motivo = tk.Label     (root, text="Motivo:")
label_status = tk.Label     (root, text="Status:")

#-----------------ENTRADAS------------------------#
entry_matricula =   tk.Entry(root)
entry_nome =        tk.Entry(root)
entry_nota =        tk.Entry(root)
entry_nova_nota =   tk.Entry(root)
entry_motivo =      tk.Entry(root)

#-----------------BOTÕES--------------------------#
button_cadastrar = tk.Button        (root, text="1 - Cadastrar Nota",   command=cadastrar_nota)
button_consultar = tk.Button        (root, text="2 - Consultar Nota",   command=consultar_nota)
button_ajustar = tk.Button          (root, text="3 - Ajustar Nota",     command=ajustar_nota)
button_verificar_status = tk.Button (root, text="4 - Verificar Status", command=verificar_status)

label_resultado = tk.Label(root, text="")

# --------------------GRIDS-----------------------#
label_matricula.grid        (row=0, column=0)
entry_matricula.grid        (row=0, column=1)
label_nome.grid             (row=1, column=0)
entry_nome.grid             (row=1, column=1)
label_nota.grid             (row=2, column=0)
entry_nota.grid             (row=2, column=1)
label_nova_nota.grid        (row=3, column=0)
entry_nova_nota.grid        (row=3, column=1)
label_motivo.grid           (row=4, column=0)
entry_motivo.grid           (row=4, column=1)
# -----------------GRID BOTÕES---------------------#
button_cadastrar.grid       (row=5, column=1, columnspan=2)
button_consultar.grid       (row=6, column=1, columnspan=2)
button_ajustar.grid         (row=7, column=1, columnspan=2)
button_verificar_status.grid(row=8, column=1, columnspan=2)

label_status.grid           (row=9, column=1, columnspan=2)
label_resultado.grid        (row=10, column=1, columnspan=2)

# Executar a aplicação
root.mainloop()