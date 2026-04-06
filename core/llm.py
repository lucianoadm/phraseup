# core/llm.py

from core.config import OPENAI_KEY, ANTHROPIC_KEY, GOOGLE_KEY

# Ordem de prioridade (pode ajustar depois)
PROVIDERS = ["openai", "anthropic", "google"]


def generate_with_provider(provider, prompt):
    """
    Executa geração de texto com base no provider escolhido.
    """

    if provider == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    elif provider == "anthropic":
        from anthropic import Anthropic

        client = Anthropic(api_key=ANTHROPIC_KEY)

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text

    elif provider == "google":
        import google.generativeai as genai

        genai.configure(api_key=GOOGLE_KEY)

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return response.text

    else:
        raise ValueError(f"Provider não suportado: {provider}")


def generate_with_fallback(prompt):
    """
    Tenta gerar resposta usando múltiplos providers.
    Se um falhar, tenta o próximo.
    """

    for provider in PROVIDERS:
        try:
            return generate_with_provider(provider, prompt)

        except Exception as e:
            print(f"[ERRO] Provider {provider} falhou: {e}")

    return "⚠️ Erro: nenhum provedor de IA disponível no momento."