import anthropic
import json
import streamlit as st

SYSTEM_PROMPT = """Você é um especialista em comunicação refinada, inspirado no método de Ezequiel Mafra.

Quando o usuário enviar uma frase crua ou informal, você deve:
1. Identificar o contexto (profissional, acadêmico ou cotidiano)
2. Devolver APENAS um JSON válido com duas reescritas da frase

JSON OBRIGATÓRIO (sem texto fora dele):
{
  "contexto": "profissional|acadêmico|cotidiano",
  "v1": {
    "tag": "Refinamento Profissional",
    "frase": "versão refinada para contexto formal/profissional",
    "motivo": "frase curta sobre o impacto desta escolha de palavras"
  },
  "v2": {
    "tag": "Tom Positivo",
    "frase": "versão com linguagem mais positiva e empática",
    "motivo": "frase curta sobre a psicologia desta escolha"
  }
}

Regras:
- Nunca use gírias ou informalidades nas versões reescritas
- Prefira verbos de ação e afirmação em vez de negação
- Substitua vícios de linguagem (eu acho, tipo, entendeu?) por expressões assertivas
- Mantenha o sentido original
- Responda SOMENTE o JSON"""

def refine_phrase(phrase: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": phrase}]
    )
    raw = message.content[0].text.strip()
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)

def score_answer(original: str, refined: str, user_answer: str, api_key: str) -> dict:
    """Avalia a resposta do usuário no modo treino reverso."""
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""Avalie a resposta do usuário no exercício de treino reverso de linguagem.

Frase refinada (dada ao usuário): "{refined}"
Frase original real: "{original}"
Resposta do usuário: "{user_answer}"

Responda APENAS um JSON:
{{
  "score": <número de 0 a 100>,
  "feedback": "<uma frase de feedback construtivo>",
  "dica": "<uma palavra ou expressão que o usuário poderia ter usado>"
}}

Critérios: similaridade semântica, informalidade adequada, naturalidade."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = message.content[0].text.strip()
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)
