import tkinter as tk
import json
import os
import datetime

PRECIOS_M2_PREDETERMINADOS = {
    "Casa": 6000,
    "Restaurante": 7500,
    "Bodega": 6500,
    "Edificio Corporativo": 7000
}

def cargar_config():

    
    vars_config = {
        "porcentaje_iva": tk.DoubleVar(value=19),  
        "costo_por_m2": tk.DoubleVar(value=6000),  
        "costo_por_empleado": tk.DoubleVar(value=25000)  
    }
    
    
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                config_guardada = json.load(f)
            
            
            vars_config["porcentaje_iva"].set(config_guardada.get("porcentaje_iva", 19))
            vars_config["costo_por_m2"].set(config_guardada.get("costo_por_m2", 6000))
            vars_config["costo_por_empleado"].set(config_guardada.get("costo_por_empleado", 25000))
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
    
    return vars_config

def guardar_config(vars_config):

    datos_config = {
        "porcentaje_iva": vars_config["porcentaje_iva"].get(),
        "costo_por_m2": vars_config["costo_por_m2"].get(),
        "costo_por_empleado": vars_config["costo_por_empleado"].get()
    }
    
    try:
        with open("config.json", "w") as f:
            json.dump(datos_config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar configuración: {e}")
        return False

def guardar_datos_usuario(datos):

    try:
        if not os.path.exists("datos_usuario"):
            os.makedirs("datos_usuario")
        
        marca_tiempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"datos_usuario/solicitud_servicio_{marca_tiempo}.json"
        
        with open(nombre_archivo, "w") as f:
            json.dump(datos, f, indent=4)
        
        return True
    except Exception as e:
        print(f"Error al guardar datos del usuario: {e}")
        return False

def obtener_factor_costo_area(tipo_area):

    factores = {
        "Casa": 1.0,
        "Restaurante": 1.2,
        "Bodega": 0.9,
        "Edificio Corporativo": 1.3
    }
    return factores.get(tipo_area, 1.0)

def actualizar_costo_por_m2(var_tipo_area, vars_config):

    tipo_area = var_tipo_area.get()
    precio_predeterminado = PRECIOS_M2_PREDETERMINADOS.get(tipo_area, 6000)
    vars_config["costo_por_m2"].set(precio_predeterminado)