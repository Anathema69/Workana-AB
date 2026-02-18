# Evalbids Order: ¿Funciona el nuevo orden de relevancia?

**Análisis del A/B Test · Workana Growth Team**

---

> **TL;DR** — El nuevo algoritmo muestra mejoras consistentes en todo el funnel de conversión
> (Accepted Bid Rate +2,8 pp, Paid Rate +3,1 pp, calidad Gold+ +6,7 pp), pero el test corrió
> solo 18 días con **35% de poder estadístico**, insuficiente para declarar significancia.
> **Recomendación: extender ~6 semanas** para resolver con rigor si el efecto es real.

---

## 1. Contexto e hipótesis

En Workana, el *matching* entre clientes y freelancers es el motor central del marketplace. Cuando un cliente publica un proyecto y recibe propuestas, las ve ordenadas en la página **Evalbids**. Actualmente, ese orden sigue una lógica antigua que **no refleja la relevancia real** del freelancer para el proyecto.

**Hipótesis:** Si reordenamos los freelancers usando un score de relevancia ponderado, el cliente encontrará más fácilmente al freelancer adecuado, impactando directamente en la conversión del marketplace.

### Diseño del experimento

| Parámetro | Detalle |
|---|---|
| Período | 3 – 21 de julio 2025 (18 días) |
| Unidad de asignación | Proyecto |
| **Control** (`default`) | 1.139 proyectos · Orden legacy |
| **Test** (`evalbidsNewOrder`) | 1.095 proyectos · Nuevo orden ponderado + filtros de calidad |
| Categorías | 10 subcategorías (Web Design, WordPress, SEO, E-commerce, Apps, 3D Models, CAD, Corporate Image, 3D Modelling) |

### Nuevo algoritmo (grupo Test)

| Factor | Peso |
|---|---|
| Nivel de gamificación | 30% |
| Proyectos trabajados en la categoría | 20% |
| Proyectos ganados en la subcategoría | 20% |
| % de skills que hacen matching | 10% |
| Ranking total en Workana | 10% |
| Proyectos exitosos (%) | 5% |
| The Accelerator (badge experto) | 2,5% |
| Membership | 2,5% |

Además, en Test solo se muestran como "recomendados" los freelancers que cumplen: gamificación Gold+, top 1.000 en ranking de categoría, top 5.000 en ranking total, y al menos 1 proyecto con 5 estrellas.

---

## 2. Datos y metodología

### Fuentes de datos

Se trabajó con 7 tablas provenientes de la base de datos de Workana:

| Tabla | Registros | Descripción |
|---|---|---|
| `abtests` | 2.670 | Asignación de proyectos a grupo Control/Test |
| `projects` | 2.234 | Información del proyecto (cliente, país, categoría, estado, EL1) |
| `bids` | 23.730 | Propuestas enviadas por freelancers |
| `threads` | 23.072 | Conversaciones y mensajes cliente-freelancer |
| `accepted_bids` | 547 | Propuestas aceptadas por clientes |
| `payments` | 803 | Pagos realizados |
| `skills` | 1.045 | Catálogo de skills |

Se construyó una **tabla maestra a nivel proyecto** (2.234 registros, 1 fila por proyecto) cruzando todas las fuentes. Validaciones: sin duplicados, coherencia de datos confirmada (todo proyecto con pago tiene accepted bid).

De los 2.670 proyectos en `abtests`, 436 no aparecen en `projects` (probablemente proyectos sin bids o eliminados). Se distribuyen equitativamente: 219 Control, 217 Test.

### Métrica de éxito principal: Accepted Bid Rate

**Definición:** Proporción de proyectos donde el cliente acepta al menos una propuesta.

**¿Por qué esta métrica?** Porque es la **conversión más directa a lo que cambiamos**. El experimento modifica el orden en que el cliente ve los freelancers en Evalbids. Si ese orden es mejor, el cliente debería encontrar más fácilmente al freelancer adecuado y aceptar su propuesta.

No elegimos Paid Rate (depende de métodos de pago y presupuesto, factores externos al experimento) ni EL1 (es un paso previo, no la conversión en sí). El Accepted Bid Rate es *la* acción que refleja si el nuevo orden hizo su trabajo.

### Métricas complementarias

| Métrica | Qué nos dice |
|---|---|
| **Tasa EL1** | ¿El cliente siquiera responde un mensaje? (engagement inicial) |
| **Paid Rate** | ¿La aceptación se convirtió en dinero real? (conversión monetaria) |
| **Tasa Productiva** | ¿El proyecto avanzó a trabajo real? (estados working/escrowing/finished/rating) |
| **GMV Promedio** | ¿Cambia el ticket promedio de los pagos? |
| **Mensajes Promedio** | ¿Hay más o menos interacción? (engagement vs. fricción) |
| **Bids Promedio** *(guardrail)* | No debería cambiar — los bids se envían antes de que el cliente vea el orden |

### Tests estadísticos utilizados

- **Tasas (proporciones):** z-test de dos proporciones independientes
- **Medias continuas:** t-test de Welch (no asume varianzas iguales)
- **Nivel de significancia:** α = 0,05 (bilateral)
- **Intervalos de confianza:** 95%, método Wald
- **Análisis de potencia:** fórmula clásica para diferencia de dos proporciones

### Balance de grupos

Los grupos están razonablemente balanceados:

| Dimensión | Control | Test |
|---|---|---|
| client_type New | 68,0% | 65,6% |
| client_type Rebuy | 32,0% | 34,4% |
| País #1: Brasil | 57,1% | 55,6% |
| País #2: España | 6,1% | 6,8% |
| País #3: Argentina | 5,8% | 5,4% |

---

## 3. Resultados del experimento

### 3.1 Vista general

| Métrica | Control | Test | Δ | Lift | p-value | IC 95% | Sig. |
|---|---|---|---|---|---|---|---|
| **Accepted Bid Rate ★** | **22,7%** | **25,5%** | **+2,83 pp** | **+12,5%** | **0,118** | **[−0,72; +6,37]** | **No** |
| Tasa EL1 | 62,3% | 66,2% | +3,87 pp | +6,2% | 0,056 | [−0,10; +7,85] | No* |
| Paid Rate | 18,9% | 22,0% | +3,13 pp | +16,6% | 0,066 | [−0,21; +6,48] | No* |
| Tasa Productiva | 21,5% | 24,3% | +2,78 pp | +12,9% | 0,118 | [−0,70; +6,27] | No |
| GMV Prom. (pagados) | $146,5 | $137,8 | −8,7 USD | −6,0% | 0,661 | [−47,7; +30,3] USD | No |
| **Mensajes Promedio** | **48,1** | **54,7** | **+6,53** | **+13,6%** | **0,039** | **[+0,33; +12,73]** | **Sí** |
| Bids Promedio (guardrail) | 10,5 | 10,7 | +0,21 | +2,0% | 0,589 | [−0,56; +0,99] | No |

*★ Métrica principal · \* Borderline (p < 0,07)*

**Lectura:** Todas las métricas de conversión suben en Test (lifts de +6% a +17%), pero ninguna cruza α = 0,05. Las más cercanas: EL1 (p = 0,056) y Paid Rate (p = 0,066). El guardrail (Bids Promedio) permanece estable (+2%, p = 0,59), confirmando la integridad del experimento.

La única métrica estadísticamente significativa es Mensajes Promedio (p = 0,039): Test genera +6,5 mensajes por proyecto. Combinado con la mejora en EL1 y conversión, apunta a **más engagement genuino**, no a fricción.

### 3.2 Análisis de funnel: la mejora es en cada etapa

| Paso del funnel | Control | Test | Δ |
|---|---|---|---|
| Proyecto → EL1 | 62,3% | 66,2% | +3,9 pp |
| EL1 → Accepted Bid | 36,3% | 38,5% | +2,2 pp |
| **Accepted Bid → Pago** | **83,3%** | **86,4%** | **+3,1 pp** |

El funnel mejora en **cada etapa**, y el efecto se amplifica hacia abajo. La mejora en la tasa Accepted→Pago es particularmente reveladora: no solo se aceptan más propuestas en Test, sino que esas aceptaciones **se concretan en pagos con mayor frecuencia** (86,4% vs 83,3%). Esto sugiere que el nuevo orden genera matches de mejor calidad — el cliente no solo acepta, realmente paga.

### 3.3 Calidad del freelancer contratado

El algoritmo prioriza freelancers de mayor nivel. ¿Se refleja en quiénes terminan siendo contratados?

**Distribución de gamificación (% de accepted bids):**

| Nivel | Control | Test | Δ |
|---|---|---|---|
| Iron | 9,8% | 12,4% | +2,6 pp |
| Bronze | 26,5% | 17,3% | **−9,2 pp** |
| Silver | 10,6% | 10,6% | 0,0 pp |
| Gold | 6,1% | 9,9% | +3,8 pp |
| Platinum | 8,3% | 11,0% | +2,7 pp |
| Hero | 38,6% | 38,9% | +0,3 pp |

**Gold+ (Gold + Platinum + Hero):**
- Control: **53,0%**
- Test: **59,7%**
- **Δ: +6,7 pp**

El cambio más drástico: Bronze cae de 26,5% a 17,3% (−9,2 pp), mientras Gold sube de 6,1% a 9,9% y Platinum de 8,3% a 11,0%. **El algoritmo cumple su función de priorizar mejor talento.**

Punto a investigar: Iron sube levemente (9,8% → 12,4%). Podría indicar que en ciertos proyectos no hay suficiente oferta Gold+ y el algoritmo rellena con niveles bajos, o un efecto de contraste donde los no-recomendados parecen más accesibles.

### 3.4 Segmentación por tipo de cliente

| Segmento | N | Control ABR | Test ABR | Lift | p-value |
|---|---|---|---|---|---|
| **New** | 1.493 | 17,2% | 20,2% | **+17,7%** | 0,132 |
| Rebuy | 741 | 34,3% | 35,5% | +3,5% | 0,731 |

**Hallazgo más importante del análisis: el efecto en clientes New es 5× mayor que en Rebuy.**

Esto tiene lógica causal directa: un cliente nuevo no conoce la plataforma, no tiene freelancers favoritos, y depende completamente del orden en que se le presentan las opciones. Un cliente recurrente ya sabe qué buscar y navega con criterio propio. **El nuevo orden ayuda más a quienes más lo necesitan.**

Detalle por segmento:
- **New:** EL1 57,0%→59,5% | Paid Rate 12,9%→15,6%
- **Rebuy:** EL1 73,6%→79,0% | Paid Rate 31,6%→34,2%

### 3.5 Segmentación por país (Top 5)

| País | N | Control ABR | Test ABR | Δ | Lift | p-value |
|---|---|---|---|---|---|---|
| BR | 1.259 | 26,3% | 28,4% | +2,1 pp | +8,0% | 0,403 |
| ES | 144 | 21,7% | 22,7% | +0,9 pp | +4,3% | 0,894 |
| MX | 130 | 20,0% | 16,9% | **−3,1 pp** | −15,4% | 0,651 |
| **AR** | **125** | **16,7%** | **25,4%** | **+8,8 pp** | **+52,5%** | 0,229 |
| US | 123 | 18,8% | 22,0% | +3,3 pp | +17,5% | 0,651 |

Argentina muestra la señal más fuerte (+8,8 pp, lift +52,5%) pero con N insuficiente (n=125). Brasil, el mercado principal, tiene un efecto moderado (+2,1 pp). México es el único país con efecto negativo (−3,1 pp), algo a investigar, aunque no significativo (p = 0,65).

Ningún país alcanza significancia individualmente — necesitamos más volumen.

### 3.6 Evolución temporal semanal

| Semana | Control ABR | Test ABR | Δ | N total |
|---|---|---|---|---|
| Sem 27 (inicio) | 28,3% | 26,7% | −1,6 pp | 189 |
| **Sem 28** | **19,9%** | **26,4%** | **+6,5 pp** | **966** |
| Sem 29 | 23,8% | 23,8% | +0,1 pp | 916 |
| Sem 30 (final) | 26,7% | 28,6% | +1,8 pp | 163 |

**Precaución:** El efecto no es estable semana a semana. Semana 28 concentra el mayor delta (+6,5 pp) mientras Semana 29 es prácticamente nula (+0,1 pp). Con ~250 proyectos/semana/grupo la varianza semanal es alta, pero esta inconsistencia refuerza que necesitamos **más tiempo de observación** antes de concluir.

---

## 4. ¿Por qué no alcanzamos significancia? Power analysis

| Parámetro | Valor |
|---|---|
| Efecto observado | 22,7% → 25,5% (Δ = +2,83 pp) |
| **Poder estadístico actual** | **34,6%** (se requiere ≥80%) |
| N actual por grupo | ~1.100 |
| N necesario para 80% de poder | 3.586 por grupo |
| N necesario para 90% de poder | 4.800 por grupo |
| Ritmo actual | ~124 proyectos/día (~62 por grupo) |
| Tiempo adicional para 80% | ~40 días (5,7 semanas) |
| Tiempo adicional para 90% | ~59 días (8,5 semanas) |

**Ahí está la respuesta.** Con ~1.100 proyectos por grupo, el test tenía solo **35% de poder estadístico** — lo que significa que *aunque el efecto sea real*, teníamos solo un 35% de probabilidad de detectarlo. Es como buscar algo en la oscuridad con una linterna demasiado débil: que no lo veamos no significa que no esté ahí.

---

## 5. Conclusión: ¿Qué hacemos con esto?

### La evidencia a favor de que el efecto es real

1. **Consistencia direccional total.** Las 4 métricas de conversión apuntan en la misma dirección. La probabilidad de que esto ocurra por azar es ~6,25% (0,5⁴) si fueran independientes.

2. **El efecto se amplifica en el funnel.** El lift crece de EL1 (+6%) a Paid Rate (+17%). Esto no es ruido aleatorio — es un patrón coherente donde las aceptaciones se concretan más en pagos.

3. **Mejora verificable en calidad.** Gold+ sube de 53% a 60%. Bronze cae de 27% a 17%. El algoritmo produce el efecto esperado en la composición del talento contratado.

4. **P-values borderline.** EL1 (p = 0,056) y Paid Rate (p = 0,066) están muy cerca del umbral.

5. **Guardrail limpio.** Bids promedio no cambió (p = 0,59), confirmando integridad experimental.

### La evidencia que pide cautela

1. Ninguna métrica de conversión es significativa a α = 0,05.
2. Evolución semanal irregular (Sem 28: +6,5 pp vs Sem 29: +0,1 pp).
3. México con efecto negativo (−3,1 pp), aunque no significativo.
4. **El test estaba underpowered** (35% de poder).

### Decisión: **ITERAR — Extender el test antes de escalar**

**No descartar:** la señal es demasiado consistente (4 métricas, funnel completo, calidad Gold+) como para atribuirla a ruido.

**No escalar hoy:** sin significancia estadística, el IC 95% del Accepted Bid Rate incluye cero (−0,72 pp a +6,37 pp). El efecto *podría* ser nulo.

**Extender ~6 semanas más** para llegar a ~3.600 proyectos/grupo y 80% de poder.

**Framework de costos:**

| Escenario | Costo |
|---|---|
| **Extender** | Bajo — mantener el 50/50 split no impacta el negocio |
| **Escalar incorrectamente** | Alto — si es ruido, degradamos la experiencia para todas las categorías |
| **Descartar incorrectamente** | El más alto — si es real (+3 pp en ABR), dejamos ~60 conversiones adicionales por cada 2.000 proyectos sobre la mesa |

---

## 6. Próximos pasos

| # | Acción | Horizonte | Fundamento |
|---|---|---|---|
| **1** | **Extender el test ~6 semanas** | Inmediato | Poder = 35%. Necesitamos 3.586/grupo para 80%. Pre-registrar tamaño y métrica para evitar sesgo de *peeking*. |
| **2** | **Desagregar por categoría** | En paralelo | Heterogeneidad por país (AR +52% vs MX −15%) sugiere heterogeneidad por vertical. Si 3-4 categorías son significativas, escalar parcialmente. |
| **3** | **Focalizar en clientes New** | 2ª iteración | Lift 5× mayor (+17,7% vs +3,5%). Un test solo para New lograría significancia más rápido y mejoraría la experiencia de primer uso. |
| **4** | **Investigar Iron en Test** | En paralelo | Sube 9,8%→12,4% pese al algoritmo. ¿Falta de oferta Gold+ en ciertos proyectos? ¿Efecto de contraste con los recomendados? |
| **5** | **Medir GMV total** | En extensión | Ticket baja −6% pero GMV total sube +5,4% (~$33.200 vs ~$31.500) por mayor volumen de pagos. La pregunta de negocio real es cuánto genera el marketplace, no cuánto paga cada proyecto individual. |
| **6** | **Iterar pesos del algoritmo** | Post-confirmación | Skills matching (10%) podría tener más peso, ya que es la señal más directa de fit. Gamificación (30%) podría estar sobredimensionada. Derivar pesos óptimos por regresión sobre datos de pagos exitosos. |
| **7** | **Expandir a todas las categorías** | Post-confirmación | Rollout escalonado a verticales fuera del scope actual (Writing, Legal, Finance), monitoreando que el efecto se mantenga. |

---

*Herramientas: Python 3.13 · pandas · SciPy (stats) · Matplotlib · Seaborn*
*Tests estadísticos: z-test de dos proporciones · t-test de Welch · Análisis de potencia estadística*
