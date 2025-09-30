# SV Processing Framework (Functional Programming in Python)

📌 **Descripción**

Este proyecto implementa un framework de procesamiento de flujos en Python basado en programación funcional y abstracciones monádicas.  
El objetivo es procesar archivos CSV de manera componible, declarativa y sin efectos secundarios, asegurando validación, manejo de errores y generación de métricas.

---

## 🎯 Objetivos alcanzados

✅ Implementación de mónadas, functores y aplicativos (**Validation, Stream**).  
✅ Transformaciones funcionales (`map`, `filter`, `reduce`, `scan`, `tap`).  
✅ Manejo de errores monádico con `Validation`.  
✅ Validación declarativa y extensible con esquema dinámico (`SCHEMA`).  
✅ Persistencia funcional de resultados en `valid.csv` y `errors.csv`.  
✅ Cálculo de métricas (total, válidas, inválidas, precio promedio).  
✅ Pruebas automáticas (leyes, unitarias, integración).  
✅ Arquitectura modular y extensible.

---

## 📂 Estructura del proyecto

```
lectura_de_csv/
│
├── core/                # Núcleo funcional
│   ├── stream.py         # Stream síncrono (map, scan, reduce...)
│   ├── validation.py     # Mónada Validation (éxito/fracaso)
│   ├── functional.py     # Utilidades (map5, partition, traverse...)
│   ├── errors.py         # Definición de ValidationError
│   ├── metrics.py        # Cálculo de métricas
│
├── validate/             # Validadores independientes
│   ├── date_validator.py
│   ├── product_validator.py
│   ├── quantity_validator.py
│   ├── price_validator.py
│   ├── customer_validator.py
│   ├── schema_validator.py   # Validación dinámica con SCHEMA
│
├── infrastructure/
│   ├── open_csv.py       # Apertura de archivos con manejo funcional de errores
│   ├── writer.py         # Persistencia de resultados
│
├── examples/
│   ├── main.py           # Ejemplo completo de pipeline CSV
│
├── test/                 # Pruebas (pytest)
│   ├── test_laws.py      # Leyes monádicas/aplicativas
│   ├── test_validators.py# Pruebas unitarias de validadores
│   ├── test_integration.py# Flujo end-to-end
│
└── README.md             # Documentación del proyecto
```

---

## ⚙️ Pipeline principal

- **Fuente (source):** archivo `ventas.csv` → se abre con `open_csv_file`.  
- **Transformaciones (map):** cada fila se valida según el `SCHEMA`.  
- **Tap (efectos controlados):** impresión de resultados por fila (✅ o ❌).  
- **Scan:** progreso en vivo (conteo acumulado de válidas/erróneas).  
- **Reduce:** métricas finales (total, válidas, inválidas, precio promedio).  
- **Sinks:** escritura en `valid.csv` y `errors.csv`.

---

## 🧪 Pruebas

- **Leyes monádicas/aplicativas:** identidad, composición, asociatividad.  
- **Unitarias:** validadores (`validate_date`, `validate_price`, etc.).  
- **Integración:** flujo completo CSV → validaciones → persistencia → métricas.

Ejecutar todas las pruebas:

```bash
pytest
```

---

## 🚀 Uso

Ejecutar el pipeline de ejemplo:

```bash
python -m examples.main
```

Esto produce:

- `valid.csv`: filas válidas  
- `errors.csv`: errores de validación  
- **Salida en consola** con progreso y métricas finales  


---

## 📖 Historial de soporte (ChatGPT)

Durante el desarrollo de este proyecto se utilizaron consultas a ChatGPT (GPT-5, OpenAI) para orientación y acompañamiento técnico.  
A continuación se listan algunas de las preguntas y respuestas relevantes como evidencia del proceso de construcción colaborativa:

### Pregunta 1
> *“esta es mi estructura, quiero validar qué opinas”*  
**Respuesta:** análisis de la arquitectura propuesta, identificando puntos fuertes (separación en `core`, validadores, pruebas de leyes) y sugerencias de mejora (unificar monadas, corregir `writer.py` truncado, mover `metrics.py` fuera de `core`, etc.).

### Pregunta 2
> *“con lo analizado qué es lo que cumplo de esto y qué es lo que me hace falta?”*  
**Respuesta:** diagnóstico frente a los objetivos del proyecto de Functional Programming (monads, functors, applicatives, stream). Se señaló qué estaba completo (validadores, métricas, pruebas de leyes) y qué faltaba (completar `Stream`, `functional.py`, documentación, unificar `Result` y `Maybe`).

### Pregunta 3
> *“me podrías ayudar a hacerlo?”*  
**Respuesta:** propuesta de diff/patch para completar `stream.py`, `functional.py`, unificar `Result`, arreglar `writer.py`, y README base.

### Pregunta 4
> *“Mejora el writer.py para que  nosea  llamado desde el main y genere los archivos separando responsabilidades”*  
**Respuesta:** se corrigió `writer.py` para contener únicamente `save_valids` y `save_errors`, y se eliminaron duplicaciones en `examples/main.py`.

### Pregunta 5
> *“Entonces, dame la lista de todos los pasos en Markdown para poder agregar un paso extra.”*  
**Respuesta:** Se preparó una guía en Markdown con los pasos para agregar la columna `region`:  
1. Actualizar archivo fuente.  
2. Cambiar `validate_row`.  
3. Ajustar `writer.py`.  
4. Probar pipeline.  
5. (Opcional) Crear `validate_region`.

---


# 📝 Pasos para agregar una columna nueva al pipeline (ejemplo: `region`)

## 1. Actualizar el archivo fuente
- Modifica tu archivo CSV (`ventas.csv`) para incluir la nueva columna en el encabezado.
- Ejemplo:

```csv
fecha,producto,cantidad,precio,cliente,region
2025-09-01,Widget A,2,60.0,Cliente 1,Sur
2025-09-02,Widget B,1,120,Cliente 2,Norte
```

## 2. Ajustar la validación de filas (examples/main.py)
```python
if len(row) != 6:   # antes era 5
    return Validation.failure([
        ValidationError("row", "WRONG_FIELDS", f"Bad row: {row}", row)
    ])
```
Agregar region al diccionario resultante:

```
return map5(
    validate_date(date),
    validate_product(product),
    validate_quantity(quantity),
    validate_price(price),
    validate_customer(customer),
    lambda d, p, q, pr, c: {
        "date": d,
        "product": p,
        "quantity": q,
        "price": pr,
        "customer": c,
        "region": region,   # 👈 nuevo campo
    }
)
```
Actualizar infrastructure/writer.py
FIELDNAMES = ["date", "product", "quantity", "price", "customer", "region"]