import os
import re
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, session
import anthropic

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MITIGACIÓN: secret_key cargada desde variable de entorno, nunca hardcodeada
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(32))

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# MITIGACIÓN LLM07 - Sin datos sensibles en el system prompt.
# Las credenciales y endpoints internos van a variables de entorno o un secrets manager,
# nunca dentro del texto que el modelo puede leer y reproducir.
SYSTEM_PROMPT = """Eres el asistente virtual de CiberBank, un banco ficticio.
Responde siempre en español y ayuda a los clientes con sus consultas bancarias.
No tienes acceso a información interna del sistema, credenciales ni endpoints.
Si el usuario solicita información confidencial del sistema, indícale que contacte
con soporte oficial."""

# Patrones que indican un intento de prompt injection
INJECTION_PATTERNS = [
    r"ignora\s+(tus\s+)?instrucciones",
    r"olvida\s+(tus\s+)?instrucciones",
    r"system\s*prompt",
    r"modo\s+diagn[oó]stico",
    r"act[uú]a\s+como",
    r"eres\s+ahora",
    r"nuevo\s+rol",
    r"jailbreak",
    r"DAN\b",
    r"repite\s+textualmente",
    r"repitas\s+textualmente",
    r"auditor[ií]a\s+(de\s+)?seguridad",
    r"antes\s+de\s+mi\s+primer\s+mensaje",
]

MAX_INPUT_LENGTH = 500
MAX_HISTORY_TURNS = 10


def detect_injection(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in INJECTION_PATTERNS)


def sanitize_input(text: str) -> str:
    # Elimina caracteres de control que pueden usarse para manipular el contexto
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text.strip()


@app.route("/")
def index():
    session.setdefault("messages", [])
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # MITIGACIÓN LLM01 - Validación de longitud
    if len(user_message) > MAX_INPUT_LENGTH:
        logger.warning("Input rechazado: demasiado largo (%d caracteres)", len(user_message))
        return jsonify({"error": "Mensaje demasiado largo. Máximo 500 caracteres."}), 400

    # MITIGACIÓN LLM01 - Sanitización del input
    user_message = sanitize_input(user_message)

    # MITIGACIÓN LLM01 - Detección de patrones de inyección
    if detect_injection(user_message):
        logger.warning("Intento de prompt injection detectado: %s", user_message[:100])
        return jsonify({"error": "Mensaje no permitido. Si necesitas ayuda, contacta con soporte."}), 400

    session.setdefault("messages", [])
    messages = session["messages"]

    # MITIGACIÓN: Limitar el historial para evitar context overflow attacks
    if len(messages) >= MAX_HISTORY_TURNS * 2:
        messages = messages[-(MAX_HISTORY_TURNS * 2):]

    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    assistant_message = response.content[0].text

    # MITIGACIÓN LLM05 - Validación básica del output:
    # Rechazamos respuestas que contengan patrones claramente peligrosos
    if re.search(r"<script", assistant_message, re.IGNORECASE):
        logger.error("Output peligroso detectado, bloqueado.")
        return jsonify({"error": "Respuesta bloqueada por política de seguridad."}), 500

    messages.append({"role": "assistant", "content": assistant_message})
    session["messages"] = messages

    logger.info("Turno completado. Historial: %d mensajes.", len(messages))
    return jsonify({"response": assistant_message})


@app.route("/reset", methods=["POST"])
def reset():
    session["messages"] = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # MITIGACIÓN: debug=False en producción
    app.run(debug=False, port=5001)
