# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROVIDER: str = "google"                    # ← Gemini forçado para teste
    
    OPENAI_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ANTHROPIC_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")


# Instância única
settings = Settings()


def validate_keys():
    provider = settings.PROVIDER

    if provider == "openai" and not settings.OPENAI_KEY:
        raise ValueError("OPENAI_API_KEY não configurada")
    if provider == "anthropic" and not settings.ANTHROPIC_KEY:
        raise ValueError("ANTHROPIC_API_KEY não configurada")
    if provider == "google" and not settings.GOOGLE_KEY:
        raise ValueError("GOOGLE_API_KEY não configurada")
    
    return True