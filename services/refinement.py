# services/refinement.py
from core.config import settings, validate_keys
import logging

logger = logging.getLogger(__name__)


def refine_with_google(text: str, level: str = "profissional") -> str:
    try:
        import google.generativeai as genai
        
        if not settings.GOOGLE_KEY:
            raise Exception("GOOGLE_API_KEY não configurada")
        
        genai.configure(api_key=settings.GOOGLE_KEY)
        
        # Prompt dinâmico conforme o nível
        level_prompts = {
            "basico": "Reescreva de forma clara, simples e natural.",
            "profissional": "Reescreva de forma profissional, clara, educada e com linguagem formal.",
            "persuasivo": "Reescreva de forma persuasiva, convincente, mantendo tom profissional e impactante."
        }
        
        system_instruction = level_prompts.get(level, level_prompts["profissional"])
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(text)
        
        if not hasattr(response, "text") or not response.text:
            raise Exception("Resposta vazia do Gemini")
            
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        raise


def refine_text(text: str, level: str = "profissional") -> str:
    """Função principal - agora aceita level"""
    if not text or not text.strip():
        return "Texto vazio."

    try:
        validate_keys()
    except ValueError as e:
        return f"⚠️ {str(e)}"

    try:
        return refine_with_google(text, level)
    except Exception as e:
        return f"⚠️ Erro ao refinar: {str(e)}"