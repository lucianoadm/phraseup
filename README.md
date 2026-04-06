# ✦ PhraseUp — Refinador de Linguagem

> Inspirado no método de **Ezequiel Mafra**. Transforme frases do dia a dia em comunicação elegante e assertiva.

---

## 🚀 Funcionalidades

| Tela | O que faz |
|---|---|
| 💬 **Refinador** | Cola uma frase crua → recebe 2 versões refinadas com explicação |
| 📚 **Biblioteca** | Salva suas frases favoritas · busca · exporta em CSV |
| 🔁 **Modo Treino** | Recebe a versão refinada → tenta descobrir o original · recebe pontuação |
| 📈 **Evolução** | Vícios detectados · atividade · score ao longo do tempo |

---

## ⚙️ Instalação local

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/phraseup.git
cd phraseup

# 2. Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o app
streamlit run app.py
```

Na barra lateral, insira sua **chave API da Anthropic** (obtenha em [console.anthropic.com](https://console.anthropic.com)).

---

## ☁️ Deploy no Streamlit Cloud

1. Faça o fork/push para seu GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em **New app** → aponte para `app.py`
4. Em **Secrets**, adicione:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Clique em **Deploy**

> O banco SQLite (`data/phraseup.db`) persiste enquanto o app estiver ativo. Para persistência permanente, migre para [Supabase](https://supabase.com) (gratuito).

---

## 🗂 Estrutura do projeto

```
phraseup/
├── app.py                  # Entry point — navegação entre páginas
├── pages/
│   ├── chat.py             # Refinador de frases (chat)
│   ├── library.py          # Biblioteca pessoal
│   ├── training.py         # Modo treino reverso
│   └── evolution.py        # Dashboard de evolução
├── utils/
│   ├── db.py               # SQLite — todas as queries
│   ├── claude_api.py       # Integração com a API Anthropic
│   └── styles.py           # CSS global
├── data/                   # Banco gerado automaticamente (gitignore)
├── .streamlit/
│   └── config.toml         # Tema do Streamlit
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Banco de dados (SQLite)

O banco é criado automaticamente em `data/phraseup.db` com 3 tabelas:

- **`history`** — cada frase refinada (original + v1 + v2 + contexto)
- **`library`** — frases salvas como favoritas
- **`training_sessions`** — resultado de cada rodada de treino

Para exportar o CSV da biblioteca, use o botão na tela **Minha Biblioteca**.

---

## 🧠 Créditos

Método de comunicação inspirado em [@ezequielmafra](https://www.tiktok.com/@ezequielmafra) no TikTok.  
Desenvolvido com [Streamlit](https://streamlit.io) + [Anthropic Claude](https://anthropic.com).
