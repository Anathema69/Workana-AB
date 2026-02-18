"""
Corrige caracteres especiales del español (acentos, ñ, ü) en el notebook.
Aplica find-and-replace sobre markdown y strings de código.
NO modifica nombres de variables, columnas ni funciones.
"""
import json, re, sys, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evalbids_analysis.ipynb')

# Reemplazos simples (orden: más específicos primero)
SIMPLE = [
    ("tamanio", "tamaño"), ("senal", "señal"), ("confunsion", "confusión"),
    ("Construccion", "Construcción"), ("Definicion", "Definición"),
    ("Justificacion", "Justificación"), ("materializacion", "materialización"),
    ("intervencion", "intervención"), ("confirmacion", "confirmación"),
    ("Gamificacion", "Gamificación"), ("gamificacion", "gamificación"),
    ("Segmentacion", "Segmentación"), ("segmentacion", "segmentación"),
    ("Distribucion", "Distribución"), ("distribucion", "distribución"),
    ("recomendacion", "recomendación"), ("Conversion", "Conversión"),
    ("conversion", "conversión"), ("interaccion", "interacción"),
    ("asignacion", "asignación"), ("aceptacion", "aceptación"),
    ("continuacion", "continuación"), ("Evolucion", "Evolución"),
    ("evolucion", "evolución"), ("Conclusion", "Conclusión"),
    ("conclusion", "conclusión"), ("iteracion", "iteración"),
    ("produccion", "producción"), ("direccion", "dirección"),
    ("friccion", "fricción"), ("Accion", "Acción"), ("accion", "acción"),
    ("Decision", "Decisión"), ("decision", "decisión"),
    ("seleccion,", "selección,"), ("seleccion.", "selección."),
    ("funcion:", "función:"), ("funcion.", "función."),
    ("expansion", "expansión"), ("extension", "extensión"),
    ("regresion", "regresión"), ("solucion", "solución"),
    ("Proporcion", "Proporción"), ("proporcion", "proporción"),
    ("Duracion", "Duración"),
    ("Metricas", "Métricas"), ("metricas", "métricas"),
    ("Metrica", "Métrica"), ("metrica", "métrica"),
    ("Estadisticos", "Estadísticos"), ("ESTADISTICOS", "ESTADÍSTICOS"),
    ("Estadistico", "Estadístico"), ("estadistico", "estadístico"),
    ("estadistica", "estadística"),
    ("Analisis", "Análisis"), ("analisis", "análisis"),
    ("metodos", "métodos"), ("explicitamente", "explícitamente"),
    ("Proximos", "Próximos"), ("Mexico", "México"),
    ("Calculo", "Cálculo"), ("Formula", "Fórmula"),
    ("minimo", "mínimo"), ("optimos", "óptimos"),
    ("especifico", "específico"), ("dinamica", "dinámica"),
    ("logica", "lógica"), ("tecnicas", "técnicas"), ("Exito", "Éxito"),
    ("reflejaria", "reflejaría"), ("descartaria", "descartaría"),
    ("escalaria", "escalaría"), ("podriamos", "podríamos"),
    ("podria", "podría"), ("deberia", "debería"),
    ("teniamos", "teníamos"), ("facilitara", "facilitará"),
    ("contamino", "contaminó"), ("revelo", "reveló"),
    ("rapida", "rápida"), ("rapido", "rápido"), ("tambien", "también"),
    ("pagina", "página"), ("patron", "patrón"),
    ("subcategorias", "subcategorías"), ("subcategoria", "subcategoría"),
    ("categorias", "categorías"), ("categoria", "categoría"),
    ("Pais ", "País "), ("paises", "países"),
]

# Reemplazos con regex (contexto necesario)
REGEX = [
    (r'\baun ', 'aún '),
    (r' mas ', ' más '), (r'\bMas ', 'Más '),
    (r'\baqui\b', 'aquí'),
    (r'\bestan ', 'están '),
    (r'\besta cumpliendo', 'está cumpliendo'),
    (r'\besta limpio', 'está limpio'),
    (r'\besta mal', 'está mal'),
    (r'\besta concentrado', 'está concentrado'),
    (r'no cambio \(', 'no cambió ('),
    (r'Por que:', 'Por qué:'),
    (r'(?<![_a-zA-Z])dias(?![_a-zA-Z])', 'días'),
    (r' a traves ', ' a través '),
    (r'\| Que nos dice', '| Qué nos dice'),
    (r'### Que podemos', '### Qué podemos'),
    (r'\*\*Que hacer:\*\*', '**Qué hacer:**'),
    (r'"cuanto paga', '"cuánto paga'),
    (r'"cuanto genera', '"cuánto genera'),
    (r'identificar donde', 'identificar dónde'),
    (r'Identificar donde', 'Identificar dónde'),
    (r'decidir cuando', 'decidir cuándo'),
]


def fix(text):
    count = 0
    for old, new in SIMPLE:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            count += n
    for pat, rep in REGEX:
        matches = list(re.finditer(pat, text))
        if matches:
            text = re.sub(pat, rep, text)
            count += len(matches)
    return text, count


def main():
    with open(PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    total = 0
    for i, cell in enumerate(nb['cells']):
        orig = ''.join(cell['source'])
        fixed, n = fix(orig)
        if n:
            lines = fixed.split('\n')
            cell['source'] = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
            total += n
            print(f"  Cell {i:2d} ({cell['cell_type']:8s}): {n:3d} fixes")

    with open(PATH, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"\nTotal: {total} correcciones en {PATH}")


if __name__ == '__main__':
    main()
