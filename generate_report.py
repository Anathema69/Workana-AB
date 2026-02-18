"""
Generador del informe final: Evalbids Order - A/B Test Analysis
Workana Growth Team | Product Data Analyst Challenge

Genera un HTML profesional autocontenido (con imágenes embebidas)
que puede imprimirse a PDF directamente desde el navegador.

Herramientas: Python 3.13, pandas, scipy, matplotlib, seaborn
"""

import pandas as pd
import numpy as np
import base64
import os
from pathlib import Path

# ── Rutas ──────────────────────────────────────────────────────────
BASE = Path(__file__).parent
INPUT = BASE / "input" / "ChallengeDataAnalystEvalbidsOrderDatos.xlsx"
OUTPUT = BASE / "output"
REPORT_PATH = BASE / "Informe_Evalbids_Order.html"


def img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def build_report_html() -> str:
    """Construye el HTML completo del informe."""

    imgs = {}
    for fname in sorted(OUTPUT.glob("*.png")):
        imgs[fname.stem] = img_to_base64(str(fname))

    def img_tag(name: str, caption: str = "") -> str:
        b64 = imgs.get(name, "")
        cap = f'<p class="caption">{caption}</p>' if caption else ""
        return f'<div class="figure"><img src="data:image/png;base64,{b64}" />{cap}</div>'

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Evalbids Order – Análisis de A/B Test | Workana</title>
<style>
  @page {{ size: A4; margin: 2cm; }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
    color: #1a1a2e;
    line-height: 1.65;
    max-width: 960px;
    margin: 0 auto;
    padding: 40px 32px;
    background: #fff;
    font-size: 14px;
  }}
  h1 {{
    font-size: 28px; color: #6C5CE7; border-bottom: 3px solid #6C5CE7;
    padding-bottom: 10px; margin-top: 0;
  }}
  h2 {{
    font-size: 21px; color: #2d3436; margin-top: 38px;
    border-left: 4px solid #6C5CE7; padding-left: 12px;
  }}
  h3 {{ font-size: 16px; color: #6C5CE7; margin-top: 24px; }}
  .subtitle {{ color: #636e72; font-size: 15px; margin-top: -8px; }}
  .executive-box {{
    background: #f8f7ff; border-left: 4px solid #6C5CE7;
    padding: 18px 22px; margin: 20px 0; border-radius: 0 8px 8px 0;
  }}
  .executive-box p {{ margin: 6px 0; }}
  .highlight-green {{
    background: #e8f5e9; border-left: 4px solid #2E7D32;
    padding: 14px 18px; margin: 16px 0; border-radius: 0 6px 6px 0;
  }}
  .highlight-amber {{
    background: #fff8e1; border-left: 4px solid #F9A825;
    padding: 14px 18px; margin: 16px 0; border-radius: 0 6px 6px 0;
  }}
  .highlight-red {{
    background: #fce4ec; border-left: 4px solid #c62828;
    padding: 14px 18px; margin: 16px 0; border-radius: 0 6px 6px 0;
  }}
  table {{
    border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 13px;
  }}
  th {{
    background: #6C5CE7; color: white; padding: 10px 12px;
    text-align: left; font-weight: 600;
  }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #e0e0e0; }}
  tr:nth-child(even) {{ background: #fafafa; }}
  tr:hover {{ background: #f0eeff; }}
  .figure {{
    text-align: center; margin: 24px 0;
    page-break-inside: avoid;
  }}
  .figure img {{
    max-width: 100%; border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }}
  .caption {{
    font-size: 12px; color: #888; margin-top: 6px; font-style: italic;
  }}
  .decision-box {{
    background: #6C5CE7; color: white; padding: 22px 28px;
    border-radius: 10px; margin: 24px 0; text-align: center;
  }}
  .decision-box h3 {{ color: white; margin-top: 0; font-size: 20px; }}
  .decision-box p {{ margin: 8px 0; font-size: 15px; }}
  .roadmap {{ counter-reset: step; }}
  .roadmap-item {{
    position: relative; padding: 12px 16px 12px 50px; margin: 8px 0;
    background: #f8f7ff; border-radius: 6px; counter-increment: step;
  }}
  .roadmap-item::before {{
    content: counter(step);
    position: absolute; left: 12px; top: 12px;
    background: #6C5CE7; color: white; width: 28px; height: 28px;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-weight: bold; font-size: 13px;
  }}
  .tag {{
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 11px; font-weight: 600;
  }}
  .tag-inmediato {{ background: #e8f5e9; color: #2E7D32; }}
  .tag-paralelo {{ background: #e3f2fd; color: #1565C0; }}
  .tag-siguiente {{ background: #fff8e1; color: #F57F17; }}
  .tag-post {{ background: #f3e5f5; color: #7B1FA2; }}
  .footer {{
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #ddd;
    font-size: 11px; color: #999; text-align: center;
  }}
  strong {{ color: #2d3436; }}
  .kpi-row {{
    display: flex; gap: 12px; margin: 16px 0; flex-wrap: wrap;
  }}
  .kpi-card {{
    flex: 1; min-width: 140px; background: #f8f7ff;
    border-radius: 8px; padding: 14px; text-align: center;
    border: 1px solid #e0daf7;
  }}
  .kpi-card .value {{ font-size: 22px; font-weight: 700; color: #6C5CE7; }}
  .kpi-card .label {{ font-size: 11px; color: #888; margin-top: 4px; }}
  @media print {{
    body {{ padding: 0; font-size: 12px; }}
    .figure {{ page-break-inside: avoid; }}
    h2 {{ page-break-after: avoid; }}
  }}
</style>
</head>
<body>

<h1>Evalbids Order – Análisis de A/B Test</h1>
<p class="subtitle">Workana Growth Team · Julio 2025 · Product Data Analyst Challenge</p>

<!-- ═══════════ EXECUTIVE SUMMARY ═══════════ -->
<h2>Resumen Ejecutivo</h2>
<div class="executive-box">
  <p>Se evaluó un <strong>nuevo algoritmo de ordenamiento de freelancers</strong> en la página Evalbids de Workana
  (donde los clientes revisan las propuestas recibidas para sus proyectos). Durante <strong>18 días</strong> se
  asignaron aleatoriamente 2.234 proyectos a dos grupos: Control (orden legacy) y Test (nuevo orden ponderado
  por gamificación, experiencia en categoría, skills y ranking).</p>
  <p><strong>Hallazgo principal:</strong> Todas las métricas de conversión mejoran a favor del grupo Test —Accepted
  Bid Rate +2,8 pp (+12,5%), Paid Rate +3,1 pp (+16,6%)— pero <strong>ninguna alcanza significancia estadística</strong>
  (p = 0,12 y p = 0,07 respectivamente). Un análisis de potencia revela que el test operó con solo <strong>35%
  de poder</strong> (se requiere ≥80%).</p>
  <p><strong>Recomendación:</strong> <em>Iterar</em>. Extender el experimento ~6 semanas adicionales para alcanzar
  el tamaño de muestra necesario (~3.600 proyectos por grupo) antes de decidir si escalar a producción.</p>
</div>

<!-- ═══════════ CONTEXTO ═══════════ -->
<h2>1. Contexto e Hipótesis</h2>
<p>En Workana, el <em>matching</em> entre clientes y freelancers es el motor central del marketplace. Actualmente,
el orden en que aparecen los freelancers en la página Evalbids sigue una lógica antigua que <strong>no refleja
la relevancia real</strong> del freelancer para el proyecto.</p>

<h3>Hipótesis</h3>
<p>Si reordenamos los freelancers usando un score ponderado que priorice calidad y experiencia, el cliente
encontrará más fácilmente al freelancer adecuado, <strong>impactando directamente en la conversión</strong>
del marketplace.</p>

<h3>Diseño del experimento</h3>
<table>
  <tr><th>Parámetro</th><th>Detalle</th></tr>
  <tr><td>Período</td><td>3 – 21 de julio 2025 (18 días)</td></tr>
  <tr><td>Unidad de asignación</td><td>Proyecto</td></tr>
  <tr><td>Control (segment=<code>default</code>)</td><td>1.139 proyectos · Orden legacy</td></tr>
  <tr><td>Test (segment=<code>evalbidsNewOrder</code>)</td><td>1.095 proyectos · Nuevo orden ponderado</td></tr>
  <tr><td>Categorías incluidas</td><td>10 subcategorías (Web Design, WordPress, SEO, E-commerce, Apps, entre otras)</td></tr>
</table>

<p>El nuevo algoritmo pondera:</p>
<table>
  <tr><th>Factor</th><th>Peso</th></tr>
  <tr><td>Nivel de gamificación</td><td>30%</td></tr>
  <tr><td>Proyectos trabajados en la categoría</td><td>20%</td></tr>
  <tr><td>Proyectos ganados en la subcategoría</td><td>20%</td></tr>
  <tr><td>% de skills que hacen matching</td><td>10%</td></tr>
  <tr><td>Ranking total en Workana</td><td>10%</td></tr>
  <tr><td>Proyectos exitosos (%)</td><td>5%</td></tr>
  <tr><td>The Accelerator (badge experto)</td><td>2,5%</td></tr>
  <tr><td>Membership</td><td>2,5%</td></tr>
</table>

<!-- ═══════════ METODOLOGÍA ═══════════ -->
<h2>2. Metodología</h2>

<h3>Datos</h3>
<p>Se trabajó con 7 tablas provenientes de la base de datos de Workana: <code>abtests</code>, <code>projects</code>,
<code>bids</code>, <code>threads</code>, <code>accepted_bids</code>, <code>payments</code> y <code>skills</code>.
Se construyó una <strong>tabla maestra a nivel proyecto</strong> (2.234 registros) cruzando todas las fuentes.</p>

<h3>Métrica de éxito principal: Accepted Bid Rate</h3>
<p>Proporción de proyectos donde el cliente acepta al menos una propuesta. Es la conversión
<strong>más cercana a la intervención</strong>: el nuevo orden cambia lo que el cliente ve en Evalbids, y aceptar
un bid es la acción directa que evidencia si esa experiencia mejoró. No depende de factores externos
como métodos de pago o presupuesto del proyecto.</p>

<h3>Métricas complementarias</h3>
<table>
  <tr><th>Métrica</th><th>Qué mide</th></tr>
  <tr><td><strong>Tasa EL1</strong></td><td>Engagement inicial: ¿el cliente responde al menos un mensaje?</td></tr>
  <tr><td><strong>Paid Rate</strong></td><td>Conversión monetaria real: ¿se concretó un pago?</td></tr>
  <tr><td><strong>Tasa Productiva</strong></td><td>Proyectos en estados de trabajo (working, escrowing, finished, rating)</td></tr>
  <tr><td><strong>GMV Promedio</strong></td><td>Ticket promedio de los proyectos que pagan</td></tr>
  <tr><td><strong>Mensajes Promedio</strong></td><td>Nivel de interacción cliente–freelancer</td></tr>
  <tr><td><strong>Bids Promedio</strong> (guardrail)</td><td>No debería cambiar: los bids se envían antes del reordenamiento</td></tr>
</table>

<h3>Tests estadísticos</h3>
<ul>
  <li><strong>Tasas (proporciones):</strong> z-test de dos proporciones independientes</li>
  <li><strong>Medias continuas:</strong> t-test de Welch (no asume varianzas iguales)</li>
  <li><strong>Nivel de significancia:</strong> α = 0,05 (bilateral)</li>
  <li><strong>Intervalos de confianza:</strong> 95%, método Wald</li>
  <li><strong>Análisis de potencia:</strong> Fórmula clásica para diferencia de dos proporciones</li>
</ul>

<h3>Herramientas</h3>
<p>Python 3.13 · pandas · NumPy · SciPy (stats) · Matplotlib · Seaborn · Jupyter Notebook</p>

<!-- ═══════════ RESULTADOS ═══════════ -->
<h2>3. Resultados del Experimento</h2>

<h3>3.1 Vista general: todas las métricas a favor de Test</h3>

<table>
  <tr>
    <th>Métrica</th><th>Control</th><th>Test</th><th>Δ (pp)</th>
    <th>Lift</th><th>p-value</th><th>IC 95%</th><th>Sig.</th>
  </tr>
  <tr>
    <td><strong>Accepted Bid Rate ★</strong></td><td>22,7%</td><td>25,5%</td>
    <td>+2,83</td><td>+12,5%</td><td>0,118</td><td>[−0,72 ; +6,37]</td><td>No</td>
  </tr>
  <tr>
    <td>Tasa EL1</td><td>62,3%</td><td>66,2%</td>
    <td>+3,87</td><td>+6,2%</td><td>0,056</td><td>[−0,10 ; +7,85]</td><td>No*</td>
  </tr>
  <tr>
    <td>Paid Rate</td><td>18,9%</td><td>22,0%</td>
    <td>+3,13</td><td>+16,6%</td><td>0,066</td><td>[−0,21 ; +6,48]</td><td>No*</td>
  </tr>
  <tr>
    <td>Tasa Productiva</td><td>21,5%</td><td>24,3%</td>
    <td>+2,78</td><td>+12,9%</td><td>0,118</td><td>[−0,70 ; +6,27]</td><td>No</td>
  </tr>
  <tr>
    <td>GMV Promedio (pagados)</td><td>$146,5</td><td>$137,8</td>
    <td>−8,74 USD</td><td>−6,0%</td><td>0,661</td><td>[−47,7 ; +30,3]</td><td>No</td>
  </tr>
  <tr>
    <td><strong>Mensajes Promedio</strong></td><td>48,1</td><td>54,7</td>
    <td>+6,53</td><td>+13,6%</td><td><strong>0,039</strong></td><td>[+0,33 ; +12,73]</td><td><strong>Sí</strong></td>
  </tr>
  <tr>
    <td>Bids Promedio (guardrail)</td><td>10,5</td><td>10,7</td>
    <td>+0,21</td><td>+2,0%</td><td>0,589</td><td>[−0,56 ; +0,99]</td><td>No</td>
  </tr>
</table>
<p style="font-size:12px; color:#888;">★ Métrica principal · * Borderline (p &lt; 0,07)</p>

{img_tag("01_rates_comparison", "Figura 1 — Métricas de conversión: Test vs Control")}
{img_tag("02_volume_comparison", "Figura 2 — Métricas de volumen: Test vs Control")}

<div class="highlight-amber">
  <strong>Lectura clave:</strong> Todas las tasas de conversión suben en Test, con lifts de +6% a +17%.
  Sin embargo, ninguna cruza el umbral de significancia (α = 0,05). Las más cercanas son EL1 (p = 0,056) y
  Paid Rate (p = 0,066). El guardrail (Bids Promedio) permanece estable, confirmando la integridad del
  experimento.
</div>

<!-- ═══════════ FUNNEL ═══════════ -->
<h3>3.2 El funnel mejora en cada etapa</h3>

<table>
  <tr><th>Paso del funnel</th><th>Control</th><th>Test</th><th>Δ</th></tr>
  <tr><td>Proyecto → EL1</td><td>62,3%</td><td>66,2%</td><td>+3,9 pp</td></tr>
  <tr><td>EL1 → Accepted Bid</td><td>36,3%</td><td>38,5%</td><td>+2,2 pp</td></tr>
  <tr><td>Accepted Bid → Pago</td><td>83,3%</td><td>86,4%</td><td>+3,1 pp</td></tr>
</table>

{img_tag("03_funnel_analysis", "Figura 3 — Análisis de funnel: tasas absolutas y de paso entre etapas")}

<div class="highlight-green">
  <strong>Hallazgo:</strong> La mejora no se limita a generar más aceptaciones; las propuestas aceptadas en
  Test <strong>se concretan en pagos con mayor frecuencia</strong> (86,4% vs 83,3%). Esto sugiere que el nuevo
  orden conecta al cliente con freelancers más adecuados, produciendo matches de mayor calidad.
</div>

<!-- ═══════════ GAMIFICACIÓN ═══════════ -->
<h3>3.3 Calidad del freelancer contratado</h3>

<p>El nuevo orden prioriza freelancers de mayor nivel. ¿Se refleja en quiénes terminan siendo contratados?</p>

<div class="kpi-row">
  <div class="kpi-card"><div class="value">53,0%</div><div class="label">Gold+ en Control</div></div>
  <div class="kpi-card"><div class="value" style="color:#2E7D32;">59,7%</div><div class="label">Gold+ en Test</div></div>
  <div class="kpi-card"><div class="value" style="color:#2E7D32;">+6,7 pp</div><div class="label">Incremento</div></div>
</div>

{img_tag("04_gamification_quality", "Figura 4 — Distribución de gamificación de freelancers contratados")}

<p>El cambio más notable: <strong>Bronze cae de 26,5% a 17,3%</strong> (−9,2 pp) mientras Gold sube de 6,1% a
9,9% y Platinum de 8,3% a 11,0%. El algoritmo está cumpliendo su función de priorizar mejor talento.
Un punto a investigar: Iron sube levemente (9,8% → 12,4%).</p>

<!-- ═══════════ SEGMENTACIÓN ═══════════ -->
<h3>3.4 ¿Para quién funciona mejor? Segmentación por tipo de cliente</h3>

{img_tag("05_segmentation_client_type", "Figura 5 — Métricas por tipo de cliente: New vs Rebuy")}

<table>
  <tr><th>Segmento</th><th>Control ABR</th><th>Test ABR</th><th>Lift</th><th>p-value</th></tr>
  <tr><td><strong>New</strong> (n=1.493)</td><td>17,2%</td><td>20,2%</td><td><strong>+17,7%</strong></td><td>0,132</td></tr>
  <tr><td>Rebuy (n=741)</td><td>34,3%</td><td>35,5%</td><td>+3,5%</td><td>0,731</td></tr>
</table>

<div class="highlight-green">
  <strong>Hallazgo clave:</strong> El efecto en clientes <em>New</em> es <strong>5× mayor</strong> que en
  <em>Rebuy</em>. Es lógico: un cliente nuevo no conoce la plataforma ni tiene freelancers favoritos.
  Depende completamente del orden en que se le presentan las opciones. Un cliente recurrente ya sabe qué buscar.
</div>

<!-- ═══════════ PAÍSES ═══════════ -->
<h3>3.5 Variación por país</h3>

{img_tag("06_segmentation_country", "Figura 6 — Accepted Bid Rate por país (Top 5)")}

<p>Argentina muestra la señal más fuerte (+8,8 pp, lift +52,5%), aunque con N bajo (n=125).
Brasil, el mercado principal, muestra un efecto moderado (+2,1 pp). México es el único país con
efecto negativo (−3,1 pp), aunque no significativo (p = 0,65). Ningún segmento por país alcanza
significancia estadística individualmente por insuficiente tamaño muestral.</p>

<!-- ═══════════ TEMPORAL ═══════════ -->
<h3>3.6 Evolución semanal</h3>

{img_tag("07_weekly_evolution", "Figura 7 — Evolución temporal semanal: Test vs Control")}

<table>
  <tr><th>Semana</th><th>Control</th><th>Test</th><th>Δ</th><th>N total</th></tr>
  <tr><td>Sem 27 (inicio)</td><td>28,3%</td><td>26,7%</td><td>−1,6 pp</td><td>189</td></tr>
  <tr><td>Sem 28</td><td>19,9%</td><td>26,4%</td><td><strong>+6,5 pp</strong></td><td>966</td></tr>
  <tr><td>Sem 29</td><td>23,8%</td><td>23,8%</td><td>+0,1 pp</td><td>916</td></tr>
  <tr><td>Sem 30 (final)</td><td>26,7%</td><td>28,6%</td><td>+1,8 pp</td><td>163</td></tr>
</table>

<div class="highlight-amber">
  <strong>Precaución:</strong> El efecto no es estable semana a semana. Semana 28 concentra el mayor
  delta (+6,5 pp) mientras Semana 29 es prácticamente nula. Esto refuerza la necesidad de más tiempo
  de observación antes de concluir.
</div>

<!-- ═══════════ CONCLUSIÓN ═══════════ -->
<h2>4. Conclusión y Decisión</h2>

<h3>¿Qué podemos concluir?</h3>
<p>El nuevo orden de relevancia muestra una <strong>señal positiva y consistente</strong> en todo el
funnel de conversión, pero <strong>no alcanza significancia estadística</strong> con la muestra actual.</p>

<p><strong>A favor:</strong></p>
<ul>
  <li><strong>Consistencia direccional total:</strong> las 4 métricas de conversión apuntan en la misma
  dirección. La probabilidad de que esto ocurra por azar es ~6,25%.</li>
  <li><strong>Amplificación en el funnel:</strong> el lift crece del 6% (EL1) al 17% (Paid Rate), lo que
  indica que no es ruido sino un efecto que se traduce en pagos reales.</li>
  <li><strong>Mejora en calidad:</strong> Gold+ sube de 53% a 60%, confirmando que el algoritmo funciona.</li>
  <li><strong>P-values borderline:</strong> EL1 (p = 0,056) y Paid Rate (p = 0,066) están cerca del umbral.</li>
  <li><strong>Guardrail limpio:</strong> Bids Promedio no cambió (p = 0,59).</li>
</ul>

<p><strong>En contra:</strong></p>
<ul>
  <li>Ninguna métrica de conversión es significativa a α = 0,05.</li>
  <li>Evolución semanal irregular (efecto concentrado en Semana 28).</li>
  <li>México muestra efecto negativo (aunque no significativo).</li>
</ul>

<h3>Análisis de potencia</h3>

<div class="kpi-row">
  <div class="kpi-card"><div class="value" style="color:#c62828;">35%</div><div class="label">Poder actual</div></div>
  <div class="kpi-card"><div class="value">3.586</div><div class="label">N/grupo para 80%</div></div>
  <div class="kpi-card"><div class="value">~40 días</div><div class="label">Tiempo adicional</div></div>
</div>

<p>Con ~1.100 proyectos por grupo, el test tenía solo <strong>35% de poder estadístico</strong> para
detectar un efecto de ~3 pp. Necesitamos ~3.600 por grupo (80% de poder), lo que equivale a
~40 días adicionales al ritmo actual de ~62 proyectos/día/grupo.</p>

<div class="decision-box">
  <h3>DECISIÓN: ITERAR</h3>
  <p>Extender el experimento ~6 semanas más antes de escalar.</p>
  <p style="font-size:13px; opacity:0.9;">No descartar (la señal es demasiado consistente).<br>
  No escalar aún (sin significancia, el riesgo es alto).</p>
</div>

<p><strong>Justificación del framework de costos:</strong></p>
<ul>
  <li><strong>Costo de extender = bajo:</strong> mantener el 50/50 split unas semanas más no impacta
  el negocio.</li>
  <li><strong>Costo de escalar incorrectamente = alto:</strong> si el efecto es ruido, degradamos la
  experiencia.</li>
  <li><strong>Costo de descartar incorrectamente = el más alto:</strong> si el efecto es real (+3 pp
  en ABR), dejamos ~60 conversiones adicionales por cada 2.000 proyectos sobre la mesa.</li>
</ul>

<!-- ═══════════ PRÓXIMOS PASOS ═══════════ -->
<h2>5. Próximos Pasos</h2>

<div class="roadmap">
  <div class="roadmap-item">
    <strong>Extender el test ~6 semanas</strong> <span class="tag tag-inmediato">Inmediato</span><br>
    Alcanzar ~3.600 proyectos/grupo para 80% de poder. Definir tamaño de muestra y métrica
    <em>antes</em> de extender (pre-registro) para evitar sesgo de <em>peeking</em>.
  </div>
  <div class="roadmap-item">
    <strong>Desagregar por categoría/subcategoría</strong> <span class="tag tag-paralelo">En paralelo</span><br>
    El análisis por país reveló heterogeneidad (AR +52% vs MX −15%). Es probable que exista por
    categoría. Si 3–4 categorías muestran efecto significativo, se podría escalar parcialmente.
  </div>
  <div class="roadmap-item">
    <strong>Focalizar en clientes New</strong> <span class="tag tag-siguiente">2ª iteración</span><br>
    El lift en New es 5× mayor que en Rebuy. Un test focalizado lograría significancia más rápido
    y diseñaría una mejor experiencia de primer uso.
  </div>
  <div class="roadmap-item">
    <strong>Investigar el aumento de Iron en Test</strong> <span class="tag tag-paralelo">En paralelo</span><br>
    Iron sube de 9,8% a 12,4% pese a que el algoritmo debería priorizar niveles altos. Posibles causas:
    falta de oferta Gold+ en ciertos proyectos, o efecto de contraste con los "recomendados".
  </div>
  <div class="roadmap-item">
    <strong>Medir GMV total como métrica complementaria</strong> <span class="tag tag-paralelo">En paralelo</span><br>
    El ticket promedio baja −6%, pero el GMV total sube +5,4% (~$33.200 vs ~$31.500) por mayor
    volumen de pagos. La pregunta de negocio real es cuánto genera el marketplace en total.
  </div>
  <div class="roadmap-item">
    <strong>Iterar los pesos del algoritmo</strong> <span class="tag tag-post">Post-confirmación</span><br>
    Skills matching (10%) podría tener más peso; gamificación (30%) podría estar sobredimensionada.
    Usar datos de pagos exitosos para derivar pesos óptimos por regresión.
  </div>
  <div class="roadmap-item">
    <strong>Expandir a todas las categorías</strong> <span class="tag tag-post">Post-confirmación</span><br>
    Rollout escalonado fuera de las 10 categorías actuales, monitoreando efecto en verticales
    distintas (Writing, Legal, Finance).
  </div>
</div>

<!-- ═══════════ FOOTER ═══════════ -->
<div class="footer">
  <p>Análisis realizado con Python 3.13 · pandas · SciPy · Matplotlib · Seaborn<br>
  Tests estadísticos: z-test de dos proporciones, t-test de Welch, análisis de potencia<br>
  Febrero 2026</p>
</div>

</body>
</html>"""

    return html


if __name__ == "__main__":
    print("Generando informe profesional...")
    html = build_report_html()
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Informe generado: {REPORT_PATH}")
    print(f"Tamaño: {REPORT_PATH.stat().st_size / 1024:.0f} KB")
    print("Abrir en navegador e imprimir como PDF (Ctrl+P → Guardar como PDF)")
