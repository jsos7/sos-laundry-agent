# agent/tools.py — Herramientas del agente SOS Laundry Miami
# Generado por AgentKit

"""
Herramientas específicas para SOS Laundry Miami.
Cubre: FAQ, calificación de leads y soporte post-venta.
"""

import os
import yaml
import logging

logger = logging.getLogger("agentkit")

# Zonas de servicio
AREAS_SERVICIO = ["doral", "sweetwater", "westchester", "fontainebleau", "tamiami", "medley"]


def cargar_info_negocio() -> dict:
    """Carga la información del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atención del negocio."""
    return {
        "horario": "Lunes a Viernes 9am-8pm | Sábados 10am-6pm | Domingos cerrado (atendemos por texto)",
        "dias": {
            "lunes_viernes": "9:00am - 8:00pm",
            "sabado": "10:00am - 6:00pm",
            "domingo": "Cerrado (atendemos por texto y llamadas)"
        }
    }


def verificar_area_servicio(zona: str) -> bool:
    """Verifica si una zona está dentro del área de servicio."""
    return zona.lower().strip() in AREAS_SERVICIO


def obtener_precios() -> dict:
    """Retorna la lista de servicios y precios."""
    return {
        "bolsa_mediana": {"descripcion": "Hasta ~25 lbs", "precio": 49.99},
        "bolsa_grande": {"descripcion": "Hasta ~40 lbs", "precio": 74.99},
        "articulos_voluminosos": {"descripcion": "Cobijas, edredones, cortinas, etc.", "precio": 34.99},
        "planchado_camisa": {"descripcion": "Camisa o blusa manga larga/corta", "precio": 5.99},
        "planchado_pantalon": {"descripcion": "Pantalón largo o corto", "precio": 5.50},
        "planchado_vestido": {"descripcion": "Vestido corto (hasta la rodilla)", "precio": 9.99},
    }


def buscar_en_knowledge(consulta: str) -> str:
    """
    Busca información relevante en los archivos de /knowledge.
    Retorna el contenido más relevante encontrado.
    """
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontré información específica sobre eso en mis archivos."


def calificar_lead(zona: str, servicio_interes: str) -> dict:
    """
    Califica un lead según su zona y servicio de interés.
    Retorna si es calificado y qué acción tomar.
    """
    en_area = verificar_area_servicio(zona)
    return {
        "calificado": en_area,
        "zona": zona,
        "servicio": servicio_interes,
        "accion": "agendar_pickup" if en_area else "fuera_de_area",
        "mensaje": (
            f"Cliente en {zona} — dentro del área de servicio. Listo para ordenar."
            if en_area else
            f"Cliente en {zona} — fuera del área de servicio actual (Doral, Sweetwater, Westchester, Fontainebleau, Tamiami, Medley)."
        )
    }
