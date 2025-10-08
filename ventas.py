import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Ventas(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)


        titulo = tk.Label(self, text="VENTAS", bg="#dddddd", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5,y=0, width=1090, height=90)    

        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1) 
        frame2.place(x=0, y=100, width=1100, height=550)

        lblframe = LabelFrame(frame2, text="Informacíon de la venta", bg="#C6D9E3", font="sans 16 bold")
        lblframe.place(x=10, y=10, width=1060, height=80)

        label_numero_factura = tk.Label(lblframe, text="Número de \nfactura", bg="#C6D9E3", font="sans 12 bold")
        label_numero_factura.place(x=10, y=5)
        self.numero_factura = tk.StringVar()

        self.entry_numero_factura = ttk.Entry(lblframe, textvariable=self.entry_numero_factura, state="readonly", font="sans 12 bold")
        self.entry_numero_factura.place(x=100, y=5, width=80)
        
        label_nombre = tk.label(lblframe, text= "Productos: ", bg="#C6D9E3", font= "sans 12 bold")
        label_nombre.place(x= 200, y = 12)
        self.entry_nombre = ttk.Combobox(lblframe, font= 'sans 12 bold', state="readonly")
        self.entry_nombre.place(x= 280, y = 10, width=180)
        
        label_valor = tk.label(lblframe, text="Precio:", bg="#C6D9E3", font="sans 12 bold")
        label_valor.place(x= 470, y = 12)
        self.entry_valor = ttk.Entry(lblframe, font= "sans 12 bold")
        self.entry_valor.place(x= 540, y = 10, width= 180)
        
        label_cantidad = tk.label(lblframe,text="Cantidad:", bg="#C6D9E3", font="sans 12 bold")
        label_cantidad.place(x= 730, y=12)
        
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x = 820, y = 10)
        
        treFrame = tk.Frame(frame2, bg="#C6D9E3")
        treFrame.place(x = 150, y = 120, width=800, height=200)
        
        scroll_y=ttk.Scrollbar(treFrame, orient = VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(treFrame, orient= HORIZONTAL)
        scroll_x.pack(side = BOTTOM, fill = X)
        
        self.tree = ttk.Treeview(treFrame, columns=("Productos", "Precio", "Cantidad", "Subtotal"), show= "headings", height=10, yscrollcommand= scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.heading("#1", text= "Producto")
        self.tree.heading("#2", text= "Precio")
        self.tree.heading("#3", text= "Cantidad")
        self.tree.heading("#4", text= "Subtotal")
        
        self.tree.column("Producto", anchor= "center")
        self.tree.column("Precio", anchor= "center")
        self.tree.column("Cantidad", anchor= "center")
        self.tree.column("Subtotal", anchor= "center")
        
        self.tree.pack(expand=True, fill = BOTH)
        lblframe1 = LabelFrame(frame2, text="Opciones", bg="#C6D9E3", font="sans 12 bold")
        lblframe1.place(x=10, y=300, width=1060, height=100)
        
        boton_agregar = tk.Button(lblframe1, tect="Agregar Artículo", bg="#C6D9E3", font="sans 12 bold")
        boton_agregar.place(x=50, y=10, width= 240, height=50)
        
        boton_pagar = tk.Button(lblframe1, text ="Agregar Artculo", bg="#C6D9E3", font="sans 12 bold")
        boton_pagar.place(x=400, y= 10, width=240, height=50)
        
        boton_ver_facturas = tk.Button(lblframe1, text="Ver Facturas", bg="dddddd", font="sans 12")
        boton_ver_facturas.place(x=750, y=10, width=240, height=50)

        self.label_suma_total = tk.Label(frame2, text="Total a pagar: MXN 0", bg="#C6D9E3", font="sans 25 bold")
        self.label_suma_total.place(x=360, y=355)

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario") 
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            if not productos:
                print("No se encontraron productos en la base de datos.")
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar procutso desde la base de datos:", e)
        
               
        
        
        

# Aqui empieza el video 8, min(1:06:30)

    def calcular_cambio():
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio < 0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                return
            label_cambio.