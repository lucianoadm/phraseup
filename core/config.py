# core/config.py

import os

try:
    import streamlit as st
    SECRETS = st.secrets
except:
    SECRETS = {}

def get_key(name):
    """
    Prioridade:
    1. Streamlit Secrets (produção)
    2. Variável de ambiente (.env local)
    """
    return SECRETS.get(name) or os.getenv(name, "")


class Settings:
    PROVIDER: str = "google"  # pode trocar depois

    OPENAI_KEY: str = get_key("OPENAI_API_KEY")
    GOOGLE_KEY: str = get_key("GOOGLE_API_KEY")
    ANTHROPIC_KEY: str = get_key("ANTHROPIC_API_KEY")


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
