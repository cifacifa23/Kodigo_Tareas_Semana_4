# 🚀 Sistema de Normalización y Gestión de Transacciones Financieras

* **Estudiante:** Carlos Isaac Flores Aparicio
* **Materia:** AI for Developers
* **Entorno de desarrollo:** VS Code / Python & Streamlit

---

## 📋 1. Descripción del Proyecto
Este proyecto consiste en un pipeline de datos robusto desarrollado en **Python** para procesar, normalizar, validar y auditar registros de transacciones financieras heterogéneas provenientes de múltiples fuentes con estructuras JSON diversas. El sistema unifica todos los datos bajo un esquema maestro común y expone una **interfaz web interactiva** que permite explorar, filtrar y visualizar métricas globales en tiempo real.

---

## 📂 2. Estructura del Proyecto
La arquitectura del sistema sigue estrictamente el principio de **separación de responsabilidades**, dividiendo la lógica en módulos independientes:

```text
proyecto_transacciones/
│
├── config.py           # Reglas de negocio, mapeo de estados y monedas
├── normalizer.py       # Detección de fuentes y unificación al esquema común
├── validator.py        # Filtrado de calidad y aislamiento de registros inválidos
├── metrics.py          # Cálculo de estadísticas globales y totales monetarios
├── app.py              # Interfaz web interactiva desarrollada con Streamlit
├── transactions.json   # Datos de prueba (registros válidos e inconsistencias)
└── README.md           # Ficha técnica y documentación del repositorio
```

---

## 📐 3. Ficha Técnica y Reglas de Negocio

### A. Esquema Maestro Normalizado
Todas las transacciones de entrada son transformadas al siguiente formato estándar común:
```json
{
  "id": "string",
  "amount": 99.99,
  "currency": "USD",
  "timestamp": "ISO-8601",
  "status": "SUCCESS | FAILED | PENDING",
  "source": "string"
}
```

### B. Componentes del Pipeline
1. **`config.py`:** Centraliza los diccionarios de traducción de estados (ej. `completed`, `OK`, `success` $\rightarrow$ `SUCCESS`) y las divisas soportadas para evitar código duplicado.
2. **`normalizer.py`:** Detecta automáticamente el origen del registro (`source_1`, `source_2`, `source_3`) basándose en sus llaves (`id`, `transaction_id`, `ref`), limpiando símbolos de moneda, ajustando centavos a decimales y estandarizando fechas al formato ISO.
3. **`validator.py`:** Evalúa la integridad de cada transacción procesada. Los registros con montos negativos, IDs nulos o fechas erróneas no interrumpen el flujo, sino que son aislados con una lista detallada de errores para auditoría.
4. **`metrics.py`:** Agrega los datos válidos para calcular el total procesado, conteos por estado y sumas agrupadas por tipo de moneda.

---

## 💻 4. Interfaz Web Interactiva (Streamlit)
Para cumplir con el requerimiento interactivo de forma profesional, se implementó una interfaz visual mediante **Streamlit**. Permite navegar dinámicamente entre vistas mediante un menú lateral:
* **Métricas Globales:** Tarjetas de resumen y paneles estadísticos.
* **Transacciones Válidas:** Tabla dinámica con un **filtro interactivo por estado** (`SUCCESS`, `FAILED`, `PENDING`).
* **Transacciones Inválidas:** Registro de auditoría para detectar errores de entrada.

*Evidencia de funcionamiento de la interfaz web:*
El sistema despliega correctamente las tablas normalizadas y el menú de filtros laterales comprobando su operatividad visual directa en el navegador.

---

## 🤖 5. Uso de la Inteligencia Artificial y Criterios Propios
* **Apoyo de la IA:** Se empleó como asistente técnico de sintaxis para el manejo de fechas (`datetime`) y la estructura modular inicial.
* **Criterios del Desarrollador:** El diseño del esquema maestro, las reglas de validación estricta y la lógica de aislamiento de excepciones fueron definidos e implementados con criterio técnico propio para garantizar la consistencia financiera.

---

## ⚙️ 6. Instrucciones de Ejecución
1. Clona o descarga el repositorio en tu equipo dentro de una carpeta de trabajo.
2. Instala la librería Streamlit ejecutando en tu terminal de VS Code:
   ```bash
   python -m pip install streamlit
   ```
3. Ejecuta la aplicación web:
   ```bash
   python -m streamlit run app.py
   ```
