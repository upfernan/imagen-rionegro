import tkinter as tk
from tkinter import ttk, messagebox
import calculo
import configuracion
import matplotlib.pyplot as plt
from PIL import Image
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
raiz = None
conteo_servicios = {}
tipo_area = None
tamano_area = None
tiempo_contrato = None
etiquetas_resultado = {}
vars_config = {}
etiquetas_comparativa = {}
pestana_mapa_frame = None
estado_mapa = None

def crear_cuaderno():
    global raiz
    style = ttk.Style()
    style.configure('TNotebook', background="#f0f0f0")
    style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 9))
    style.map('TNotebook.Tab', background=[('selected', '#4a90e2'), ('active', '#b3d4fc')])
    style.map('TNotebook.Tab', foreground=[('selected', 'white'), ('active', 'black')])
    cuaderno = ttk.Notebook(raiz)
    cuaderno.pack(fill=tk.BOTH, expand=True)
    pestana_principal = ttk.Frame(cuaderno)
    pestana_config = ttk.Frame(cuaderno)
    pestana_resultado = ttk.Frame(cuaderno)
    pestana_comparativa = ttk.Frame(cuaderno)
    pestana_mapa = ttk.Frame(cuaderno)
    cuaderno.add(pestana_principal, text="Principal")
    cuaderno.add(pestana_config, text="Configuración")
    cuaderno.add(pestana_resultado, text="Calcular")
    cuaderno.add(pestana_comparativa, text="Comparativa")
    cuaderno.add(pestana_mapa, text="Cobertura de domicilio")
    
    configurar_pestana_principal(pestana_principal)
    configurar_pestana_config(pestana_config)
    configurar_pestana_resultado(pestana_resultado)
    configurar_pestana_comparativa(pestana_comparativa)
    configurar_pestana_mapa(pestana_mapa)
def iniciar_interfaz():
    global raiz, conteo_servicios, tipo_area, tamano_area, tiempo_contrato, vars_config
    raiz = tk.Tk()
    raiz.title("Servicio de Limpieza")
    raiz.geometry("900x600")      
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")  
    style.configure("Green.TFrame", background="#1c6e8c")
    style.configure("Purple.TFrame", background="#1c6e8c")
    style.configure("Orange.TButton", background="#e67e22", foreground="white", 
                   font=("Arial", 12, "bold"))
    style.configure("Green.TLabel", background="#1c6e8c", foreground="white",
                   font=("Arial", 12), padding=10)
    style.configure("Purple.TLabel", background="#1c6e8c", foreground="white",
                   font=("Arial", 14, "bold"), padding=10)
    style.configure("Accent.TButton", background="#ff7733", foreground="white", 
                   font=("Arial", 10, "bold"))
    conteo_servicios = {
        "Limpieza General": tk.IntVar(value=0),
        "Limpieza Baños": tk.IntVar(value=0),
        "Limpieza Cocinas/Alfombras y Tapetes": tk.IntVar(value=0),
        "Limpieza Muebles": tk.IntVar(value=0),
        "Limpieza Áreas Exteriores": tk.IntVar(value=0),
        "Limpieza Residuos": tk.IntVar(value=0),
        "Limpieza Profunda y especializada": tk.IntVar(value=0),
        "Limpieza Desinfección": tk.IntVar(value=0)
    }
    tipo_area = tk.StringVar(value="Casa")
    tamano_area = tk.DoubleVar(value=0)
    tiempo_contrato = tk.IntVar(value=1)
    vars_config = configuracion.cargar_config()
    crear_cuaderno()
    return raiz

def configurar_pestana_principal(padre):
    global tipo_area, tamano_area, conteo_servicios, vars_config, tiempo_contrato
    main_frame = ttk.Frame(padre)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    marco_servicios = ttk.LabelFrame(main_frame, text="Servicio de Limpieza -")
    marco_servicios.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    texto_servicios_style = {"font": ("Arial", 9), "fg": "#000000"}
    fila = 0
    for nombre_servicio, var in conteo_servicios.items():
        tk.Label(marco_servicios, text=nombre_servicio+":", 
                anchor="e", **texto_servicios_style).grid(
            row=fila, column=0, padx=5, pady=5, sticky=tk.E)
        spinbox = tk.Spinbox(marco_servicios, from_=0, to=10, textvariable=var, 
                           width=3, justify="center")
        spinbox.grid(row=fila, column=1, padx=5, pady=5, sticky=tk.W)
        fila += 1
    marco_derecho = ttk.Frame(main_frame)
    marco_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    marco_derecho.columnconfigure(0, weight=1) 
    marco_derecho.columnconfigure(1, weight=1)  
    fila_derecha = 0
    etiqueta_area = ttk.Label(marco_derecho, text="Ingrese el area en\nmetros cuadrados", 
                           background="#1c6e8c", foreground="white", 
                           padding=8, anchor="center")
    etiqueta_area.grid(row=fila_derecha, column=0, padx=5, pady=10, sticky="ew")
    entrada_area = ttk.Entry(marco_derecho, textvariable=tamano_area)
    entrada_area.grid(row=fila_derecha, column=1, padx=5, pady=10, sticky="ew")
    fila_derecha += 1
    etiqueta_tipo_area = ttk.Label(marco_derecho, text="Area", 
                               background="#8e44ad", foreground="white", 
                               padding=8, anchor="center")
    etiqueta_tipo_area.grid(row=fila_derecha, column=0, padx=5, pady=10, sticky="ew")
    tipos_area = ["Casa", "Restaurante", "Bodega", "Edificio Corporativo"]
    combo_tipo_area = ttk.Combobox(marco_derecho, textvariable=tipo_area, 
                                 values=tipos_area)
    combo_tipo_area.grid(row=fila_derecha, column=1, padx=5, pady=10, sticky="ew")
    combo_tipo_area.set(tipo_area.get())
    fila_derecha += 1
    etiqueta_ubicacion = ttk.Label(marco_derecho, text="Ubicacion: En pestaña de mapa", 
                                background="#27ae60", foreground="white", 
                                padding=8, anchor="center")
    etiqueta_ubicacion.grid(row=fila_derecha, column=0, padx=5, pady=10, sticky="ew")
    campo_ubicacion = ttk.Label(marco_derecho, text="")
    campo_ubicacion.grid(row=fila_derecha, column=1, padx=5, pady=10, sticky="ew")
    fila_derecha += 1
    espacio = ttk.Frame(marco_derecho)
    espacio.grid(row=fila_derecha, column=0, columnspan=2, pady=5)
    fila_derecha += 1
    calcular_btn = tk.Button(marco_derecho, text="Calcular", 
                           command=calcular, 
                           bg="#ff7733", fg="white",
                           padx=20, pady=5,
                           relief=tk.RAISED,
                           borderwidth=1)
    calcular_btn.grid(row=fila_derecha, column=0, columnspan=2, pady=10)
    tipo_area.trace_add("write", lambda *args: configuracion.actualizar_costo_por_m2(tipo_area, vars_config))
    configuracion.actualizar_costo_por_m2(tipo_area, vars_config)
def configurar_pestana_config(padre):
    global vars_config
    main_frame = ttk.Frame(padre)
    main_frame.pack(fill=tk.BOTH, expand=True)
    header_frame = ttk.Frame(main_frame, style="Header.TFrame")
    header_frame.pack(fill=tk.X, pady=10)
    ttk.Label(header_frame, text="Configuración:", font=("Arial", 12, "bold")).pack(pady=5)
    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    iva_frame = ttk.Frame(content_frame)
    iva_frame.pack(fill=tk.X, pady=10)
    iva_label = ttk.Label(iva_frame, text="IVA", font=("Arial", 10, "bold"), 
                          background="#1c6e8c", foreground="white", anchor="center")
    iva_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    iva_label.configure(width=20)
    iva_entry = ttk.Entry(iva_frame, textvariable=vars_config["porcentaje_iva"], width=15)
    iva_entry.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(iva_frame, text="%").grid(row=0, column=2, sticky="w")
    m2_frame = ttk.Frame(content_frame)
    m2_frame.pack(fill=tk.X, pady=10)
    m2_label = ttk.Label(m2_frame, text="METRO\nCUADRADO", font=("Arial", 10, "bold"), 
                         background="#1c6e8c", foreground="white", anchor="center")
    m2_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    m2_label.configure(width=20)
    
    m2_entry = ttk.Entry(m2_frame, textvariable=vars_config["costo_por_m2"], width=15)
    m2_entry.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(m2_frame, text="$").grid(row=0, column=2, sticky="w")
    emp_frame = ttk.Frame(content_frame)
    emp_frame.pack(fill=tk.X, pady=10)
    emp_label = ttk.Label(emp_frame, text="COSTO POR\nEMPLEADO", font=("Arial", 10, "bold"), 
                          background="#1c6e8c", foreground="white", anchor="center")
    emp_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    emp_label.configure(width=20)
    emp_entry = ttk.Entry(emp_frame, textvariable=vars_config["costo_por_empleado"], width=15)
    emp_entry.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(emp_frame, text="$").grid(row=0, column=2, sticky="w")
    guardar_frame = ttk.Frame(content_frame)
    guardar_frame.pack(fill=tk.X, pady=20)
    guardar_btn = tk.Button(guardar_frame, 
                          text="Guardar cambios",
                          command=lambda: configuracion.guardar_config(vars_config),
                          bg="#ff7733",      
                          fg="white",        
                          font=("Arial", 10, "bold"),
                          padx=15,
                          pady=8,
                          relief=tk.RAISED, 
                          borderwidth=1)  
    guardar_btn.pack(pady=10)
    info_frame = ttk.LabelFrame(content_frame, text="Precios Predeterminados por Área")
    info_frame.pack(fill=tk.X, pady=10)
    for i, (area, precio) in enumerate(configuracion.PRECIOS_M2_PREDETERMINADOS.items()):
        ttk.Label(info_frame, text=f"{area}:").grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(info_frame, text=f"{precio} $").grid(row=i, column=1, padx=5, pady=2, sticky=tk.W)
def configurar_pestana_resultado(padre):
    global etiquetas_resultado
    
    main_frame = ttk.Frame(padre)
    main_frame.pack(fill=tk.BOTH, expand=True)
    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    content_frame.columnconfigure(0, weight=2)
    content_frame.columnconfigure(1, weight=1)
    results_frame = ttk.Frame(content_frame)
    results_frame.grid(row=0, column=0, sticky="nsew", padx=10)
    
    etiquetas_resultado = {}
    etiquetas = [
        "VALOR TOTAL DE METROS CUADRADOS",
        "IVA",
        "COSTO EMPLEADOS",
        "VALOR TOTAL A PAGAR",
        "AHORRO MENSUAL",
        "AHORRO ANUAL",
        "TIEMPO DE CONTRATO (AÑOS)"
    ]
    for i, texto_etiqueta in enumerate(etiquetas):
        row_frame = ttk.Frame(results_frame, style="Result.TFrame")
        row_frame.pack(fill=tk.X, pady=5)
        label = ttk.Label(row_frame, text=texto_etiqueta, background="#1c6e8c", 
                          foreground="white", anchor="center", padding=(5, 10))
        label.pack(fill=tk.X)
        etiqueta_resultado = ttk.Label(row_frame, text="0", anchor="center", padding=(5, 10))
        etiqueta_resultado.pack(fill=tk.X)
        etiquetas_resultado[texto_etiqueta] = etiqueta_resultado
    ahorro_frame = ttk.Frame(content_frame)
    ahorro_frame.grid(row=0, column=1, sticky="n", padx=10, pady=30)
    
    ahorro_label = ttk.Label(ahorro_frame, text="AHORRO", background="#ff6633", 
                            foreground="white", font=("Arial", 12, "bold"), padding=(20, 10))
    ahorro_label.pack(fill=tk.X, pady=10)
    ahorro_valor = ttk.Label(ahorro_frame, text="0", font=("Arial", 14))
    ahorro_valor.pack(fill=tk.X, pady=10)
    etiquetas_resultado["AHORRO DESTACADO"] = ahorro_valor
def configurar_pestana_comparativa(padre):
    global etiquetas_comparativa
    marco_comparativa = ttk.Frame(padre)
    marco_comparativa.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    ttk.Label(marco_comparativa, text="Comparativa de Costos", font=("Arial", 12, "bold")).pack(pady=10)
    marco_tabla = ttk.Frame(marco_comparativa)
    marco_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    style = ttk.Style()
    style.configure("Header.TLabel", font=("Arial", 10, "bold"), background="#1c6e8c", foreground="white", padding=5)
    ttk.Label(marco_tabla, text="Concepto", style="Header.TLabel").grid(row=0, column=0, padx=2, pady=5, sticky="nsew")
    ttk.Label(marco_tabla, text="Servicio Contratado", style="Header.TLabel").grid(row=0, column=1, padx=2, pady=5, sticky="nsew")
    ttk.Label(marco_tabla, text="Servicio Interno", style="Header.TLabel").grid(row=0, column=2, padx=2, pady=5, sticky="nsew")
    ttk.Label(marco_tabla, text="Ahorro", style="Header.TLabel").grid(row=0, column=3, padx=2, pady=5, sticky="nsew")
    ttk.Label(marco_tabla, text="Costo Mensual:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    ttk.Label(marco_tabla, text="Costo Anual:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    ttk.Label(marco_tabla, text="Costo Total del Contrato:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    etiquetas_comparativa = {
        "servicio_mensual": ttk.Label(marco_tabla, text="0"),
        "interno_mensual": ttk.Label(marco_tabla, text="0"),
        "ahorro_mensual": ttk.Label(marco_tabla, text="0"),
        "servicio_anual": ttk.Label(marco_tabla, text="0"),
        "interno_anual": ttk.Label(marco_tabla, text="0"),
        "ahorro_anual": ttk.Label(marco_tabla, text="0"),
        "servicio_total": ttk.Label(marco_tabla, text="0"),
        "interno_total": ttk.Label(marco_tabla, text="0"),
        "ahorro_total": ttk.Label(marco_tabla, text="0")
    }
    etiquetas_comparativa["servicio_mensual"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["interno_mensual"].grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["ahorro_mensual"].grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["servicio_anual"].grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["interno_anual"].grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["ahorro_anual"].grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["servicio_total"].grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["interno_total"].grid(row=3, column=2, padx=5, pady=5, sticky=tk.E)
    etiquetas_comparativa["ahorro_total"].grid(row=3, column=3, padx=5, pady=5, sticky=tk.E)
    marco_ventajas = ttk.LabelFrame(marco_comparativa, text="Ventajas del Servicio Contratado")
    marco_ventajas.pack(fill=tk.X, padx=10, pady=20)
    
    ventajas = [
        "Sin costos de contratación y gestión de personal.",
        "Personal capacitado y equipos especializados.",
        "Flexibilidad en la programación de servicios.",
        "Garantía en la calidad del servicio.",
        "Reducción de costos administrativos y de supervisión."
    ]
    for i, ventaja in enumerate(ventajas):
        ttk.Label(marco_ventajas, text="• " + ventaja).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
def configurar_pestana_mapa(padre):
    global pestana_mapa_frame, estado_mapa
    marco_mapa = ttk.Frame(padre)
    marco_mapa.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    ttk.Label(marco_mapa, text="Cobertura de servicio", font=("Arial", 12, "bold")).pack(pady=5)
    marco_controles = ttk.Frame(marco_mapa)
    marco_controles.pack(fill=tk.X, pady=5)
    ttk.Button(marco_controles, text="Cargar Mapa", command=seleccionar_archivo_mapa).pack(side=tk.LEFT, padx=5)
    estado_mapa = ttk.Label(marco_controles, text="")
    estado_mapa.pack(side=tk.LEFT, padx=5)
    pestana_mapa_frame = ttk.Frame(marco_mapa)
    pestana_mapa_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    ttk.Label(pestana_mapa_frame, text="Cargando mapa...").pack(pady=50)
    raiz.after(1000, mostrar_mapa_en_pestana)
def cargar_mapa(ruta=None):
    rutas_predeterminadas = [
        "mapa-rionegro.png",
        "mapas/mapa-rionegro.png",
        "imagenes/mapa-rionegro.png",
        "recursos/mapa-rionegro.png"
    ] 
    if ruta and os.path.exists(ruta):
        return Image.open(ruta)
    for ruta_pred in rutas_predeterminadas:
        if os.path.exists(ruta_pred):
            return Image.open(ruta_pred)
    return None
def seleccionar_archivo_mapa():
    from tkinter import filedialog
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar Mapa",
        filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")]
    )
    if ruta_archivo:
        mostrar_mapa_en_pestana(ruta_archivo)
def mostrar_mapa_en_pestana(ruta_mapa=None):
    global pestana_mapa_frame, estado_mapa
    for widget in pestana_mapa_frame.winfo_children():
        widget.destroy()
    mapa = cargar_mapa(ruta_mapa)
    if mapa:
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.imshow(mapa)
        ax.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=pestana_mapa_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        estado_mapa.config(text="Mapa cargado correctamente")
    else:
        estado_mapa.config(text="No se pudo cargar el mapa")
        ttk.Label(pestana_mapa_frame, text="Mapa no disponible").pack(pady=50)
def calcular():
    global conteo_servicios, tipo_area, tamano_area, tiempo_contrato, etiquetas_resultado, vars_config, etiquetas_comparativa
    
    try:
        datos_servicios = {nombre: var.get() for nombre, var in conteo_servicios.items()}
        
        if datos_servicios["Limpieza General"] > 1:
            datos_servicios["Limpieza General"] = 1
            conteo_servicios["Limpieza General"].set(1)
            messagebox.showwarning("Ajuste aplicado", "El valor de Limpieza General ha sido ajustado a 1 (máximo permitido).")
        
        datos_area = {
            "tipo": tipo_area.get(),
            "tamano": tamano_area.get()
        }
        
        resultados = calculo.calcular_costo_servicio(datos_servicios, datos_area, vars_config, tiempo_contrato.get())
        etiquetas_resultado["VALOR TOTAL DE METROS CUADRADOS"].config(text=f"{resultados['costo_area']:.2f} $")
        etiquetas_resultado["IVA"].config(text=f"{resultados['monto_iva']:.2f} $")
        etiquetas_resultado["COSTO EMPLEADOS"].config(text=f"{resultados['costo_empleados']:.2f} $")
        etiquetas_resultado["VALOR TOTAL A PAGAR"].config(text=f"{resultados['costo_total']:.2f} $")
        etiquetas_resultado["AHORRO MENSUAL"].config(text=f"{resultados['ahorro_mensual']:.2f} $")
        etiquetas_resultado["AHORRO ANUAL"].config(text=f"{resultados['ahorro_anual']:.2f} $")
        etiquetas_resultado["TIEMPO DE CONTRATO (AÑOS)"].config(text=f"{tiempo_contrato.get()} años")
        if "AHORRO DESTACADO" in etiquetas_resultado:
            etiquetas_resultado["AHORRO DESTACADO"].config(text=f"{resultados['ahorro_anual']:.2f} $")
        etiquetas_comparativa["servicio_mensual"].config(text=f"{resultados['costo_total']:.2f} $")
        etiquetas_comparativa["interno_mensual"].config(text=f"{resultados['costo_interno_mensual']:.2f} $")
        etiquetas_comparativa["ahorro_mensual"].config(text=f"{resultados['ahorro_mensual']:.2f} $")
        etiquetas_comparativa["servicio_anual"].config(text=f"{resultados['costo_total'] * 12:.2f} $")
        etiquetas_comparativa["interno_anual"].config(text=f"{resultados['costo_interno_mensual'] * 12:.2f} $")
        etiquetas_comparativa["ahorro_anual"].config(text=f"{resultados['ahorro_mensual'] * 12:.2f} $")
        etiquetas_comparativa["servicio_total"].config(text=f"{resultados['costo_anual']:.2f} $")
        etiquetas_comparativa["interno_total"].config(text=f"{resultados['costo_interno_anual']:.2f} $")
        etiquetas_comparativa["ahorro_total"].config(text=f"{resultados['ahorro_anual']:.2f} $")
        messagebox.showinfo("Cálculo Completado", "Los resultados se han calculado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular: {str(e)}")
def guardar_datos():
    global conteo_servicios, tipo_area, tamano_area, tiempo_contrato
    try:
        datos_servicios = {nombre: var.get() for nombre, var in conteo_servicios.items()} 
        if datos_servicios["Limpieza General"] > 1:
            datos_servicios["Limpieza General"] = 1
            conteo_servicios["Limpieza General"].set(1)
            messagebox.showwarning("Ajuste aplicado", "El valor de Limpieza General ha sido ajustado a 1 (máximo permitido).")
        datos = {
            "tipo_area": tipo_area.get(),
            "tamano_area": tamano_area.get(),
            "tiempo_contrato": tiempo_contrato.get(),
            "servicios": datos_servicios
        }
        configuracion.guardar_datos_usuario(datos)
        messagebox.showinfo("Guardado", "Los datos se han guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar datos: {str(e)}")
def main():
    raiz_app = iniciar_interfaz()
    raiz_app.mainloop()

if __name__ == "__main__":
    main()