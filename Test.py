import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

INVENTORY_FILE = 'inventario.csv'
SALES_FILE = 'ventas.csv'

if os.path.exists(INVENTORY_FILE):
	inventario = pd.read_csv(INVENTORY_FILE)
else:
	inventario = pd.DataFrame(columns=['item', 'cantidad'])

# Cargar ventas o crear uno nuevo
if os.path.exists(SALES_FILE):
	ventas = pd.read_csv(SALES_FILE)
else:
	ventas = pd.DataFrame(columns=['item', 'cantidad'])

# Función para guardar inventario y ventas
def guardar_datos():
	inventario.to_csv(INVENTORY_FILE, index=False)
	ventas.to_csv(SALES_FILE, index=False)

# GUI principal
class InventarioApp(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('Inventario')
		self.geometry('600x400')
		self.protocol('WM_DELETE_WINDOW', self.on_closing)

		# Frame de control
		control_frame = tk.Frame(self)
		control_frame.pack(pady=10)

		tk.Label(control_frame, text='Ítem:').grid(row=0, column=0)
		self.item_entry = tk.Entry(control_frame)
		self.item_entry.grid(row=0, column=1)

		tk.Label(control_frame, text='Cantidad:').grid(row=0, column=2)
		self.cantidad_entry = tk.Entry(control_frame)
		self.cantidad_entry.grid(row=0, column=3)

		tk.Button(control_frame, text='Agregar', command=self.agregar_item).grid(row=0, column=4, padx=5)
		tk.Button(control_frame, text='Eliminar', command=self.eliminar_item).grid(row=0, column=5, padx=5)
		tk.Button(control_frame, text='Buscar', command=self.buscar_item).grid(row=0, column=6, padx=5)

		# Frame de ventas
		ventas_frame = tk.Frame(self)
		ventas_frame.pack(pady=5)
		tk.Label(ventas_frame, text='Vender ítem:').grid(row=0, column=0)
		self.venta_item_entry = tk.Entry(ventas_frame)
		self.venta_item_entry.grid(row=0, column=1)
		tk.Label(ventas_frame, text='Cantidad:').grid(row=0, column=2)
		self.venta_cantidad_entry = tk.Entry(ventas_frame)
		self.venta_cantidad_entry.grid(row=0, column=3)
		tk.Button(ventas_frame, text='Registrar venta', command=self.registrar_venta).grid(row=0, column=4, padx=5)
		tk.Button(ventas_frame, text='Resumen ventas', command=self.mostrar_resumen_ventas).grid(row=0, column=5, padx=5)
		tk.Button(ventas_frame, text='Gráfica ventas', command=self.mostrar_grafica_ventas).grid(row=0, column=6, padx=5)

		# Tabla de inventario
		self.tree = ttk.Treeview(self, columns=('Ítem', 'Cantidad'), show='headings')
		self.tree.heading('Ítem', text='Ítem')
		self.tree.heading('Cantidad', text='Cantidad')
		self.tree.pack(expand=True, fill='both', pady=10)
		self.actualizar_tabla()
	def mostrar_grafica_ventas(self):
		import matplotlib.pyplot as plt
		if ventas.empty:
			messagebox.showinfo('Sin datos', 'No hay ventas registradas para graficar.')
			return
		plt.figure(figsize=(6,4))
		plt.bar(ventas['item'], ventas['cantidad'], color='skyblue')
		plt.xlabel('Ítem')
		plt.ylabel('Cantidad vendida')
		plt.title('Resumen de ventas')
		plt.tight_layout()
		plt.show()

	def registrar_venta(self):
		global inventario, ventas
		item = self.venta_item_entry.get().strip()
		try:
			cantidad = int(self.venta_cantidad_entry.get())
		except ValueError:
			messagebox.showerror('Error', 'Cantidad debe ser un número entero')
			return
		if not item:
			messagebox.showerror('Error', 'El nombre del ítem no puede estar vacío')
			return
		if item in inventario['item'].values:
			idx = inventario[inventario['item'] == item].index[0]
			if inventario.at[idx, 'cantidad'] >= cantidad:
				inventario.at[idx, 'cantidad'] -= cantidad
				# Registrar venta
				if item in ventas['item'].values:
					ventas.loc[ventas['item'] == item, 'cantidad'] += cantidad
				else:
					ventas = pd.concat([ventas, pd.DataFrame({'item': [item], 'cantidad': [cantidad]})], ignore_index=True)
				self.actualizar_tabla()
				messagebox.showinfo('Venta registrada', f'Se vendieron {cantidad} de {item}')
			else:
				messagebox.showerror('Error', 'No hay suficiente stock para vender')
		else:
			messagebox.showerror('Error', 'Ítem no encontrado en inventario')

	def mostrar_resumen_ventas(self):
		resumen = '\n'.join([f"{row['item']}: {row['cantidad']} vendidos" for _, row in ventas.iterrows()])
		if not resumen:
			resumen = 'No hay ventas registradas.'
		messagebox.showinfo('Resumen de ventas', resumen)

	def __init__(self):
		super().__init__()
		self.title('Inventario')
		self.geometry('600x400')
		self.protocol('WM_DELETE_WINDOW', self.on_closing)

		# Frame de control
		control_frame = tk.Frame(self)
		control_frame.pack(pady=10)

		tk.Label(control_frame, text='Ítem:').grid(row=0, column=0)
		self.item_entry = tk.Entry(control_frame)
		self.item_entry.grid(row=0, column=1)

		tk.Label(control_frame, text='Cantidad:').grid(row=0, column=2)
		self.cantidad_entry = tk.Entry(control_frame)
		self.cantidad_entry.grid(row=0, column=3)

		tk.Button(control_frame, text='Agregar', command=self.agregar_item).grid(row=0, column=4, padx=5)
		tk.Button(control_frame, text='Eliminar', command=self.eliminar_item).grid(row=0, column=5, padx=5)
		tk.Button(control_frame, text='Buscar', command=self.buscar_item).grid(row=0, column=6, padx=5)

		# Tabla de inventario
		self.tree = ttk.Treeview(self, columns=('Ítem', 'Cantidad'), show='headings')
		self.tree.heading('Ítem', text='Ítem')
		self.tree.heading('Cantidad', text='Cantidad')
		self.tree.pack(expand=True, fill='both', pady=10)
		self.actualizar_tabla()

	def agregar_item(self):
		global inventario
		item = self.item_entry.get().strip()
		try:
			cantidad = int(self.cantidad_entry.get())
		except ValueError:
			messagebox.showerror('Error', 'Cantidad debe ser un número entero')
			return
		if not item:
			messagebox.showerror('Error', 'El nombre del ítem no puede estar vacío')
			return
		if item in inventario['item'].values:
			inventario.loc[inventario['item'] == item, 'cantidad'] += cantidad
		else:
			inventario = pd.concat([inventario, pd.DataFrame({'item': [item], 'cantidad': [cantidad]})], ignore_index=True)
		self.actualizar_tabla()

	def eliminar_item(self):
		global inventario
		item = self.item_entry.get().strip()
		if item in inventario['item'].values:
			inventario = inventario[inventario['item'] != item]
			self.actualizar_tabla()
		else:
			messagebox.showinfo('Info', 'Ítem no encontrado')

	def buscar_item(self):
		item = self.item_entry.get().strip()
		for row in self.tree.get_children():
			self.tree.delete(row)
		if item:
			resultado = inventario[inventario['item'].str.contains(item, case=False, na=False)]
			for _, row in resultado.iterrows():
				self.tree.insert('', 'end', values=(row['item'], row['cantidad']))
		else:
			self.actualizar_tabla()

	def actualizar_tabla(self):
		for row in self.tree.get_children():
			self.tree.delete(row)
		for _, row in inventario.iterrows():
			self.tree.insert('', 'end', values=(row['item'], row['cantidad']))

	def on_closing(self):
		guardar_datos()
		self.destroy()

if __name__ == '__main__':
	app = InventarioApp()
	app.mainloop()

