from core.config import Settings

def get_providers():
    if Settings.PROVIDER == "auto":
        # Ordem de prioridade (mais barato/rápido primeiro)
        return ["google", "openai", "anthropic"]
    
    # Validação
    if Settings.PROVIDER not in ["openai", "google", "anthropic"]:
        return ["google"]  # fallback seguro
    
    return [Settings.PROVIDER]