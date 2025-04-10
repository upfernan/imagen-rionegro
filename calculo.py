def calcular_costo_servicio(datos_servicios, datos_area, vars_config, tiempo_contrato=1):
    tamano_area = datos_area["tamano"]
    tipo_area = datos_area["tipo"]
    costo_por_m2 = vars_config["costo_por_m2"].get()
    
    factores_area = {
        "Casa": 1.0,
        "Restaurante": 1.2,
        "Bodega": 0.9,
        "Edificio Corporativo": 1.3
    }
    factor_area = factores_area.get(tipo_area, 1.0)
    costo_area = tamano_area * costo_por_m2 * factor_area
    total_empleados = calcular_empleados_requeridos(datos_servicios, tamano_area)
    costo_empleados = total_empleados * vars_config["costo_por_empleado"].get()
    porcentaje_iva = vars_config["porcentaje_iva"].get()
    subtotal = costo_area + costo_empleados
    monto_iva = subtotal * (porcentaje_iva / 100)
    costo_total = subtotal + monto_iva
    costo_interno_mensual = costo_total * 1.25
    ahorro_mensual = costo_interno_mensual - costo_total
    costo_anual = costo_total * 12 * tiempo_contrato
    costo_interno_anual = costo_interno_mensual * 12 * tiempo_contrato
    ahorro_anual = ahorro_mensual * 12 * tiempo_contrato
    
    return {
        "costo_area": costo_area,
        "costo_empleados": costo_empleados,
        "monto_iva": monto_iva,
        "subtotal": subtotal,
        "costo_total": costo_total,
        "costo_interno_mensual": costo_interno_mensual,
        "ahorro_mensual": ahorro_mensual,
        "costo_anual": costo_anual,
        "costo_interno_anual": costo_interno_anual,
        "ahorro_anual": ahorro_anual,
        "total_empleados": total_empleados
    }

def calcular_empleados_requeridos(datos_servicios, tamano_area):
    empleados_base = max(1, int(tamano_area / 100))
    
    pesos_servicio = {
        "Limpieza General": 1,
        "Limpieza Baños": 0.5,
        "Limpieza Cocinas/Alfombras y Tapetes": 0.7,
        "Limpieza Muebles": 0.3,
        "Limpieza Áreas Exteriores": 0.8,
        "Limpieza Residuos": 0.2,
        "Limpieza Profunda y especializada": 1.5,
        "Limpieza Desinfección": 0.6
    }
    
    empleados_adicionales = sum(datos_servicios.get(servicio, 0) * peso 
                               for servicio, peso in pesos_servicio.items())
    

    total_empleados = round(empleados_base + empleados_adicionales)

    return max(1, total_empleados)
