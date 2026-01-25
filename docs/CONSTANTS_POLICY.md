# Política del proyecto: Constantes universales y preservación de la fórmula I‑Villasmil‑Ω

Última revisión: 2026-01-24  
Autor: I. Villasmil

## Objetivo
Documentar y fijar de manera inequívoca las convenciones del marco I‑Villasmil‑Ω relativas a las constantes 0.963 y 0.037, y garantizar la preservación de la formulación como ley estructural del proyecto.

## Declaración de principios
1. Las constantes 0.963 (parte conocida/observable) y 0.037 (parte potencial/incertidumbre) son convenciones universales del marco. Deben considerarse inmutables dentro del repositorio y de cualquier implementación que declare adherencia al marco I‑Villasmil‑Ω.

2. La fórmula I‑Villasmil‑Ω es una ley estructural del marco. No se deben introducir cambios paramétricos (p. ej. pesos aprendibles, calibraciones empíricas para alterar la escala) que modifiquen su esencia matemática. Las modificaciones permitidas serán exclusivamente de carácter documental, de notación o para aclaración conceptual.

3. El factor multiplicativo 1.037 (aprox. 1 / 0.963) que aparece como corrección estructural en implementaciones es una consecuencia directa de las constantes anteriores y debe mantenerse inalterable en cualquier implementación que reclame conformidad plena con el marco.

## Convenciones de implementación
- Variables de entrada por capa (`L_i`, `phi_i`, `E_i`, `f_i`) deben normalizarse en el intervalo [0,1] según procedimientos documentados en `docs/DATA_README.md` (no se permiten normas que cambien las propiedades matemáticas esenciales del marco).
- Número de capas por defecto: N = 6 (convención del estudio). Esto puede cambiarse solo si la documentación lo explica de forma explícita y no altera las constantes universales.
- Normalización lineal recomendada (conservadora) para traducir suma de contribuciones S' a coherencia C:
  - C = C_max * (S' / S_ref), con C_max = 0.963 y S_ref declarado en la documentación.
  - S_ref debe ser una constante declarada por convención del marco; no debe ajustarse para encajar resultados empíricos.

## Valores por convención (orden del proyecto)
- C_max = 0.963
- Incertidumbre estructural = 0.037
- Factor de corrección estructural = 1.037 ≈ 1 / 0.963

## Reproducción de ejemplos del estudio
- Para reproducir los números publicados en el README, el marco admite declarar una convención histórica de escala:
  - S_ref_convenio = 1.222 (constante de escala usada en el estudio original para mapear S' → C).
- Alternativamente, la convención teórica pura puede usar:
  - S_ref_teórico = N (p. ej. 6), lo que conserva la pureza ontológica del marco pero dará escala distinta de C.

**Nota:** La elección entre `S_ref_convenio` y `S_ref_teórico` debe quedar explícita en la documentación y no debe interpretarse como “calibración” en el sentido estadístico. Es una convención de interpretación.

## Procedimiento de cambios
- Cualquier propuesta de modificación que afecte a las constantes (C_max, incertidumbre, factor 1.037) requiere aprobación formal por escrito del autor/principal del marco y su inclusión en este documento con versión y fecha.
- Las propuestas de mejora que impliquen aprendizaje automático o ajuste de parámetros deben implementarse en ramas experimentales separadas marcadas con `experimental/` y no podrán declararse conformes con la ley hasta haber sido aprobadas per la política anterior.

## Metadatos
- Versión de política: 1.0.0
- Fecha: 2026-01-24
