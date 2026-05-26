# Contexto del proyecto: Formación en AI/LLM Security

## Quién soy
Soy un estudiante de Grado Superior ASIR enfocándome en ciberseguridad,
con experiencia previa en Python y Flask (he construido una app Flask real
que automatiza envío de fichas técnicas leyendo Excel, localizando PDFs en
un NAS y enviándolos por email). Mi objetivo es trabajar en remoto en
seguridad de IA / LLM Security.

## Qué estoy haciendo
Estoy en la FASE 1 de un roadmap de formación en seguridad de aplicaciones
LLM, basado en el OWASP Top 10 for LLM Applications 2025. La fase tiene
tres tramos:
- Semanas 1-2: Teoría OWASP Top 10 (la hago por separado, no aquí)
- Semanas 3-4: Construir una app básica con la API de Claude en Python
- Semanas 5-8: Construir un laboratorio Flask intencionadamente vulnerable,
  atacarlo (prompt injection, system prompt leakage), documentar los
  ataques que funcionan y luego blindarlo aplicando mitigaciones del OWASP

## Cómo quiero que me ayudes
- Actúa como mi mentor de código, no solo como generador. Explícame el
  porqué de cada decisión técnica, especialmente las implicaciones de
  seguridad.
- Avanza paso a paso. No me des todo el proyecto de golpe; guíame por
  hitos y espera a que confirme antes de seguir.
- Cuando construyamos la app vulnerable, conéctame cada vulnerabilidad con
  su entrada correspondiente del OWASP Top 10 LLM (LLM01 Prompt Injection,
  LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling,
  LLM06 Excessive Agency, LLM07 System Prompt Leakage, etc.)
- La API key de Anthropic debe ir SIEMPRE en variable de entorno o archivo
  .env, nunca hardcodeada. Asegúrate de que el .env esté en .gitignore.
- Quiero que cada cosa que construyamos sirva como material de portfolio:
  código limpio, comentado y con un README explicativo.

## Por dónde empezar
Pregúntame primero qué versión de Python tengo y si ya tengo entorno
montado. Después, ayúdame a:
1. Crear la estructura del proyecto y el entorno virtual
2. Instalar el SDK de Anthropic de forma segura
3. Escribir mi primer script que defina un system prompt, reciba input del
   usuario y devuelva la respuesta del modelo
4. Añadir gestión del historial de conversación (array messages[])
5. Preparar el repo para GitHub (README + .gitignore)

Empieza saludándome y haciéndome la primera pregunta.