# LLM Security Lab

Laboratorio de seguridad para aplicaciones LLM basado en el **OWASP Top 10 for LLM Applications 2025**.

Construido como material de formación y portfolio en el área de AI/LLM Security.

---

## Estructura del proyecto

```
llm-security-lab/
├── src/
│   └── chat.py                  # Cliente CLI con historial de conversación
├── vulnerable-lab/
│   ├── app.py                   # Flask app con vulnerabilidades intencionadas
│   └── templates/index.html
├── secure-lab/
│   ├── app.py                   # Flask app blindada con mitigaciones OWASP
│   └── templates/index.html
├── .env                         # API key (no incluido en el repo)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.10+
- Cuenta en [Anthropic Console](https://console.anthropic.com) con créditos

---

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd llm-security-lab

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Editar .env y añadir tu ANTHROPIC_API_KEY
```

---

## Uso

**Cliente CLI:**
```bash
python src/chat.py
```
El asistente mantiene historial de conversación durante la sesión. Escribe `salir` para terminar.

**Lab vulnerable** (puerto 5000):
```bash
python vulnerable-lab/app.py
```

**Lab seguro** (puerto 5001):
```bash
python secure-lab/app.py
```

---

## Fases del laboratorio

| Fase | Contenido | Estado |
|------|-----------|--------|
| Semanas 1-2 | Teoría OWASP Top 10 for LLM Applications | ✅ Completado |
| Semanas 3-4 | App básica con API de Claude + historial | ✅ Completado |
| Semanas 5-8 | Lab Flask vulnerable + ataques + mitigaciones | ✅ Completado |

---

## Vulnerabilidades cubiertas

- **LLM01** — Prompt Injection
- **LLM02** — Sensitive Information Disclosure
- **LLM05** — Improper Output Handling
- **LLM06** — Excessive Agency
- **LLM07** — System Prompt Leakage

---

## Seguridad

La API key nunca se incluye en el repositorio. Se carga desde un archivo `.env` local mediante `python-dotenv`. El archivo `.env` está excluido por `.gitignore`.
