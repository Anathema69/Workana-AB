"""
Genera un HTML interactivo personal con navegación,
colapso de secciones y resaltado de datos clave.
Para uso interno — no será enviado como entregable.
"""
import base64
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"
HTML_PATH = BASE / "Interactive_Evalbids_Personal.html"


def img_b64(name: str) -> str:
    path = OUTPUT / f"{name}.png"
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def build():
    imgs = {
        "01": img_b64("01_rates_comparison"),
        "02": img_b64("02_volume_comparison"),
        "03": img_b64("03_funnel_analysis"),
        "04": img_b64("04_gamification_quality"),
        "05": img_b64("05_segmentation_client_type"),
        "06": img_b64("06_segmentation_country"),
        "07": img_b64("07_weekly_evolution"),
    }

    def img(key, cap=""):
        return f'<div class="fig"><img src="data:image/png;base64,{imgs[key]}"/><p class="cap">{cap}</p></div>'

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Evalbids Order — Guía Interactiva (Personal)</title>
<style>
  :root {{ --purple: #6C5CE7; --gray: #A0A0A0; --bg: #0f0f1a; --card: #1a1a2e; --text: #e0e0e0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 24px; }}
  h1 {{ color: var(--purple); font-size: 26px; margin-bottom: 4px; }}
  .subtitle {{ color: #888; font-size: 14px; margin-bottom: 24px; }}

  /* Navigation */
  nav {{ position: sticky; top: 0; background: #16162b; z-index: 100; padding: 10px 0;
         border-bottom: 1px solid #333; margin-bottom: 24px; }}
  nav a {{ color: var(--purple); text-decoration: none; margin: 0 12px; font-size: 13px;
           font-weight: 600; opacity: 0.8; transition: opacity 0.2s; }}
  nav a:hover {{ opacity: 1; text-decoration: underline; }}

  /* Collapsible sections */
  .section {{ background: var(--card); border-radius: 10px; margin-bottom: 16px;
              border: 1px solid #2a2a4a; overflow: hidden; }}
  .section-header {{
    padding: 16px 20px; cursor: pointer; display: flex; justify-content: space-between;
    align-items: center; user-select: none; transition: background 0.2s;
  }}
  .section-header:hover {{ background: #222240; }}
  .section-header h2 {{ font-size: 17px; color: var(--purple); margin: 0; }}
  .section-header .arrow {{ font-size: 18px; transition: transform 0.3s; color: #888; }}
  .section-header.open .arrow {{ transform: rotate(180deg); }}
  .section-body {{ padding: 0 20px 20px; display: none; }}
  .section-body.open {{ display: block; }}

  /* Cards & highlights */
  .kpi-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0; }}
  .kpi {{ flex: 1; min-width: 120px; background: #222240; padding: 16px; border-radius: 8px; text-align: center; }}
  .kpi .val {{ font-size: 24px; font-weight: 700; color: var(--purple); }}
  .kpi .lab {{ font-size: 11px; color: #888; margin-top: 4px; }}
  .kpi.green .val {{ color: #4CAF50; }}
  .kpi.red .val {{ color: #ef5350; }}
  .kpi.amber .val {{ color: #FFB300; }}

  .insight {{
    background: #1e1e3a; border-left: 3px solid var(--purple);
    padding: 12px 16px; margin: 12px 0; border-radius: 0 6px 6px 0; font-size: 13px;
  }}
  .insight.positive {{ border-color: #4CAF50; }}
  .insight.caution {{ border-color: #FFB300; }}
  .insight.negative {{ border-color: #ef5350; }}

  table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin: 12px 0; }}
  th {{ background: var(--purple); color: white; padding: 8px 10px; text-align: left; }}
  td {{ padding: 7px 10px; border-bottom: 1px solid #2a2a4a; }}
  tr:hover {{ background: #222240; }}

  .fig {{ text-align: center; margin: 16px 0; }}
  .fig img {{ max-width: 100%; border-radius: 6px; }}
  .cap {{ font-size: 11px; color: #666; margin-top: 4px; }}

  .decision {{ background: linear-gradient(135deg, #6C5CE7, #a29bfe);
    color: white; padding: 24px; border-radius: 12px; text-align: center; margin: 20px 0; }}
  .decision h3 {{ margin-bottom: 8px; font-size: 22px; }}
  .decision p {{ opacity: 0.9; }}

  p {{ margin: 8px 0; line-height: 1.6; font-size: 14px; }}
  strong {{ color: #ccc; }}
  ul {{ margin: 8px 0 8px 20px; }}
  li {{ margin: 4px 0; font-size: 13px; }}
</style>
</head>
<body>
<nav>
  <div class="container" style="padding:0;">
    <a href="#contexto">Contexto</a>
    <a href="#metricas">Métricas</a>
    <a href="#resultados">Resultados</a>
    <a href="#funnel">Funnel</a>
    <a href="#calidad">Calidad</a>
    <a href="#segmentos">Segmentos</a>
    <a href="#temporal">Temporal</a>
    <a href="#conclusion">Conclusión</a>
    <a href="#pasos">Próximos pasos</a>
  </div>
</nav>

<div class="container">
<h1>Evalbids Order — Guía Interactiva</h1>
<p class="subtitle">Documento personal de referencia · No para enviar · Febrero 2026</p>

<!-- CONTEXTO -->
<div class="section" id="contexto">
  <div class="section-header open" onclick="toggle(this)">
    <h2>Contexto del Experimento</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body open">
    <p><strong>¿Qué se probó?</strong> Un nuevo algoritmo de ordenamiento de freelancers en la página Evalbids
    (donde el cliente ve las propuestas). El algoritmo pondera gamificación (30%), experiencia en categoría (20%),
    experiencia en subcategoría (20%), skills matching (10%), ranking total (10%), y otros factores menores.</p>
    <p><strong>¿Por qué?</strong> El orden actual es legacy y no refleja la relevancia real del freelancer.
    La hipótesis es que un mejor orden facilita la selección y mejora la conversión.</p>
    <div class="kpi-row">
      <div class="kpi"><div class="val">2.234</div><div class="lab">Proyectos totales</div></div>
      <div class="kpi"><div class="val">1.139</div><div class="lab">Control</div></div>
      <div class="kpi"><div class="val">1.095</div><div class="lab">Test</div></div>
      <div class="kpi"><div class="val">18 días</div><div class="lab">3-21 Jul 2025</div></div>
      <div class="kpi"><div class="val">10</div><div class="lab">Categorías</div></div>
    </div>
  </div>
</div>

<!-- MÉTRICAS -->
<div class="section" id="metricas">
  <div class="section-header" onclick="toggle(this)">
    <h2>Definición de Métricas</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <p><strong>Métrica principal:</strong> <em>Accepted Bid Rate</em> — proporción de proyectos con al menos
    una propuesta aceptada. Es la conversión más cercana a la intervención (el cambio de orden).</p>
    <table>
      <tr><th>Métrica</th><th>Tipo</th><th>Qué mide</th></tr>
      <tr><td><strong>Accepted Bid Rate</strong></td><td>Principal</td><td>Conversión directa del reordenamiento</td></tr>
      <tr><td>Tasa EL1</td><td>Complementaria</td><td>Engagement inicial (cliente responde mensaje)</td></tr>
      <tr><td>Paid Rate</td><td>Complementaria</td><td>Conversión monetaria real</td></tr>
      <tr><td>Tasa Productiva</td><td>Complementaria</td><td>Proyectos en estados de trabajo</td></tr>
      <tr><td>GMV Promedio</td><td>Complementaria</td><td>Ticket promedio de pagos</td></tr>
      <tr><td>Mensajes Promedio</td><td>Complementaria</td><td>Nivel de interacción</td></tr>
      <tr><td>Bids Promedio</td><td>Guardrail</td><td>No debería cambiar (integridad del test)</td></tr>
    </table>
  </div>
</div>

<!-- RESULTADOS -->
<div class="section" id="resultados">
  <div class="section-header" onclick="toggle(this)">
    <h2>Resultados Estadísticos</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <div class="kpi-row">
      <div class="kpi green"><div class="val">+12,5%</div><div class="lab">Lift ABR</div></div>
      <div class="kpi green"><div class="val">+16,6%</div><div class="lab">Lift Paid Rate</div></div>
      <div class="kpi amber"><div class="val">p=0,118</div><div class="lab">ABR p-value</div></div>
      <div class="kpi red"><div class="val">35%</div><div class="lab">Poder actual</div></div>
    </div>
    <table>
      <tr><th>Métrica</th><th>Control</th><th>Test</th><th>Lift</th><th>p-value</th><th>Sig.</th></tr>
      <tr><td><strong>Accepted Bid Rate</strong></td><td>22,7%</td><td>25,5%</td><td>+12,5%</td><td>0,118</td><td>No</td></tr>
      <tr><td>Tasa EL1</td><td>62,3%</td><td>66,2%</td><td>+6,2%</td><td>0,056</td><td>No*</td></tr>
      <tr><td>Paid Rate</td><td>18,9%</td><td>22,0%</td><td>+16,6%</td><td>0,066</td><td>No*</td></tr>
      <tr><td>Tasa Productiva</td><td>21,5%</td><td>24,3%</td><td>+12,9%</td><td>0,118</td><td>No</td></tr>
      <tr><td><strong>Mensajes Prom.</strong></td><td>48,1</td><td>54,7</td><td>+13,6%</td><td><strong>0,039</strong></td><td><strong>Sí</strong></td></tr>
      <tr><td>GMV Prom.</td><td>$146,5</td><td>$137,8</td><td>−6,0%</td><td>0,661</td><td>No</td></tr>
      <tr><td>Bids Prom.</td><td>10,5</td><td>10,7</td><td>+2,0%</td><td>0,589</td><td>No</td></tr>
    </table>
    <div class="insight caution">Todas las métricas de conversión suben, pero ninguna alcanza α=0,05.
    EL1 (p=0,056) y Paid Rate (p=0,066) están borderline. El test estaba underpowered (35% de poder).</div>
    {img("01", "Métricas de conversión")}
    {img("02", "Métricas de volumen")}
  </div>
</div>

<!-- FUNNEL -->
<div class="section" id="funnel">
  <div class="section-header" onclick="toggle(this)">
    <h2>Análisis de Funnel</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <table>
      <tr><th>Paso</th><th>Control</th><th>Test</th><th>Δ</th></tr>
      <tr><td>Proyecto → EL1</td><td>62,3%</td><td>66,2%</td><td>+3,9 pp</td></tr>
      <tr><td>EL1 → Accepted Bid</td><td>36,3%</td><td>38,5%</td><td>+2,2 pp</td></tr>
      <tr><td>Accepted Bid → Pago</td><td>83,3%</td><td>86,4%</td><td>+3,1 pp</td></tr>
    </table>
    <div class="insight positive">El funnel mejora en CADA etapa. La tasa Accepted→Pago sube de 83,3% a 86,4%:
    las propuestas aceptadas en Test se concretan más en pagos reales.</div>
    {img("03", "Funnel completo")}
  </div>
</div>

<!-- CALIDAD -->
<div class="section" id="calidad">
  <div class="section-header" onclick="toggle(this)">
    <h2>Calidad del Freelancer Contratado</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <div class="kpi-row">
      <div class="kpi"><div class="val">53,0%</div><div class="lab">Gold+ Control</div></div>
      <div class="kpi green"><div class="val">59,7%</div><div class="lab">Gold+ Test</div></div>
      <div class="kpi green"><div class="val">+6,7 pp</div><div class="lab">Mejora</div></div>
    </div>
    <div class="insight positive">Bronze cae de 26,5% a 17,3%. Gold sube de 6,1% a 9,9%.
    El algoritmo cumple su función de priorizar mejor talento.</div>
    <div class="insight caution">Iron sube de 9,8% a 12,4%. Investigar por qué (¿falta de oferta Gold+
    en ciertos proyectos? ¿efecto de contraste?).</div>
    {img("04", "Distribución de gamificación")}
  </div>
</div>

<!-- SEGMENTOS -->
<div class="section" id="segmentos">
  <div class="section-header" onclick="toggle(this)">
    <h2>Segmentación</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <h3 style="color:#aaa; margin-top:8px;">Por tipo de cliente</h3>
    <table>
      <tr><th>Segmento</th><th>Control ABR</th><th>Test ABR</th><th>Lift</th><th>p-value</th></tr>
      <tr><td><strong>New</strong> (n=1.493)</td><td>17,2%</td><td>20,2%</td><td><strong>+17,7%</strong></td><td>0,132</td></tr>
      <tr><td>Rebuy (n=741)</td><td>34,3%</td><td>35,5%</td><td>+3,5%</td><td>0,731</td></tr>
    </table>
    <div class="insight positive">El efecto en New es 5× mayor que en Rebuy. Los nuevos dependen más del orden
    porque no conocen la plataforma.</div>
    {img("05", "Segmentación por tipo de cliente")}

    <h3 style="color:#aaa; margin-top:20px;">Por país (Top 5)</h3>
    <table>
      <tr><th>País</th><th>Control</th><th>Test</th><th>Δ</th><th>Lift</th></tr>
      <tr><td>BR (n=1.259)</td><td>26,3%</td><td>28,4%</td><td>+2,1 pp</td><td>+8,0%</td></tr>
      <tr><td>ES (n=144)</td><td>21,7%</td><td>22,7%</td><td>+0,9 pp</td><td>+4,3%</td></tr>
      <tr><td style="color:#ef5350">MX (n=130)</td><td>20,0%</td><td>16,9%</td><td>−3,1 pp</td><td>−15,4%</td></tr>
      <tr><td style="color:#4CAF50">AR (n=125)</td><td>16,7%</td><td>25,4%</td><td>+8,8 pp</td><td><strong>+52,5%</strong></td></tr>
      <tr><td>US (n=123)</td><td>18,8%</td><td>22,0%</td><td>+3,3 pp</td><td>+17,5%</td></tr>
    </table>
    {img("06", "Accepted Bid Rate por país")}
  </div>
</div>

<!-- TEMPORAL -->
<div class="section" id="temporal">
  <div class="section-header" onclick="toggle(this)">
    <h2>Evolución Temporal</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <table>
      <tr><th>Semana</th><th>Control</th><th>Test</th><th>Δ</th><th>N</th></tr>
      <tr><td>Sem 27</td><td>28,3%</td><td>26,7%</td><td>−1,6 pp</td><td>189</td></tr>
      <tr><td style="color:#4CAF50"><strong>Sem 28</strong></td><td>19,9%</td><td>26,4%</td><td><strong>+6,5 pp</strong></td><td>966</td></tr>
      <tr><td>Sem 29</td><td>23,8%</td><td>23,8%</td><td>+0,1 pp</td><td>916</td></tr>
      <tr><td>Sem 30</td><td>26,7%</td><td>28,6%</td><td>+1,8 pp</td><td>163</td></tr>
    </table>
    <div class="insight caution">El efecto NO es estable semana a semana. Se concentra en Sem 28.
    Esto refuerza la necesidad de más tiempo de observación.</div>
    {img("07", "Evolución semanal")}
  </div>
</div>

<!-- CONCLUSIÓN -->
<div class="section" id="conclusion">
  <div class="section-header open" onclick="toggle(this)">
    <h2>Conclusión y Decisión</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body open">
    <div class="decision">
      <h3>DECISIÓN: ITERAR</h3>
      <p>Extender el test ~6 semanas más (llegar a ~3.600 proyectos/grupo)</p>
      <p style="font-size:13px;">No descartar (señal consistente) · No escalar (sin significancia)</p>
    </div>
    <div class="kpi-row">
      <div class="kpi red"><div class="val">35%</div><div class="lab">Poder actual</div></div>
      <div class="kpi"><div class="val">3.586</div><div class="lab">N/grupo para 80%</div></div>
      <div class="kpi"><div class="val">~40 días</div><div class="lab">Adicionales</div></div>
    </div>
    <p><strong>A favor de iterar:</strong></p>
    <ul>
      <li>4 métricas de conversión apuntan en la misma dirección (prob. azar ~6%)</li>
      <li>EL1 (p=0,056) y Paid Rate (p=0,066) borderline</li>
      <li>Gold+ sube 53% → 60%, el algoritmo funciona</li>
      <li>Guardrail limpio (bids no cambiaron)</li>
    </ul>
    <p><strong>Precauciones:</strong></p>
    <ul>
      <li>Ninguna métrica de conversión significativa a α=0,05</li>
      <li>Evolución semanal irregular</li>
      <li>México con efecto negativo (pero N bajo)</li>
    </ul>
  </div>
</div>

<!-- PRÓXIMOS PASOS -->
<div class="section" id="pasos">
  <div class="section-header" onclick="toggle(this)">
    <h2>Próximos Pasos (Roadmap)</h2><span class="arrow">▼</span>
  </div>
  <div class="section-body">
    <table>
      <tr><th>#</th><th>Acción</th><th>Horizonte</th><th>Impacto</th></tr>
      <tr><td>1</td><td>Extender test 6 semanas</td><td style="color:#4CAF50">Inmediato</td><td>Confirmar/descartar con rigor</td></tr>
      <tr><td>2</td><td>Desagregar por categoría</td><td style="color:#2196F3">En paralelo</td><td>Escalar parcialmente</td></tr>
      <tr><td>3</td><td>Focalizar en clientes New</td><td style="color:#FFB300">2ª iteración</td><td>Maximizar donde el efecto es 5× mayor</td></tr>
      <tr><td>4</td><td>Investigar Iron en Test</td><td style="color:#2196F3">En paralelo</td><td>Mejorar algoritmo</td></tr>
      <tr><td>5</td><td>Medir GMV total</td><td style="color:#2196F3">En paralelo</td><td>Validar revenue (+5,4% estimado)</td></tr>
      <tr><td>6</td><td>Iterar pesos del algoritmo</td><td style="color:#9C27B0">Post-confirm.</td><td>Optimizar</td></tr>
      <tr><td>7</td><td>Expandir categorías</td><td style="color:#9C27B0">Post-confirm.</td><td>Escalar al marketplace</td></tr>
    </table>
  </div>
</div>

</div><!-- container -->

<script>
function toggle(header) {{
  header.classList.toggle('open');
  const body = header.nextElementSibling;
  body.classList.toggle('open');
}}
</script>
</body>
</html>"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML interactivo generado: {HTML_PATH}")


if __name__ == "__main__":
    build()
