# ✦ PhraseUp  
### Refinador de Linguagem com IA Multimodelo

O PhraseUp transforma textos simples em comunicação **clara**, **profissional** e **persuasiva**, utilizando múltiplos provedores de LLM para garantir consistência, qualidade e continuidade. Além do refinamento, o app oferece ferramentas de treino e métricas de evolução da escrita.

---

## 🌟 Principais Funcionalidades

| Tela | Descrição |
|------|-----------|
| 💬 **Refinador** | Insira textos e escolha o nível de refinamento (Básico, Profissional ou Persuasivo). |
| 📚 **Biblioteca** | Histórico completo de textos refinados, organizado e pesquisável. |
| 🔁 **Modo Treino** | Pratique reescrita manual e compare com sugestões da IA. |
| 📈 **Evolução** | Dashboard com métricas, score de clareza e progresso ao longo do tempo. |

---

## 🧠 Diferenciais Técnicos

- **Arquitetura Multi‑IA com Fallback Automático**  
  Alternância inteligente entre OpenAI, Anthropic e Google caso algum provedor falhe.

- **Refinamento por Nível**  
  Prompts otimizados para diferentes intenções: técnico, executivo ou persuasivo.

- **Persistência Inteligente**  
  Banco SQLite local para histórico, treino e evolução.

---

## 🗂 Estrutura do Projeto

phraseup/ ├── app.py                # Ponto de entrada ├── core/ │   ├── config.py         # Variáveis de ambiente e validação │   └── llm.py            # Engine Multi-IA + Fallback ├── services/ │   └── refinement.py     # Lógica de refinamento ├── pages/                # Módulos do Streamlit │   ├── chat.py           # Interface de refinamento │   ├── library.py        # Histórico │   ├── training.py       # Modo treino │   └── evolution.py      # Métricas ├── utils/ │   ├── db.py             # Interface SQLite │   └── styles.py         # Customização de UI ├── requirements.txt └── README.md


---

## ⚙️ Instalação Local

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/phraseup.git
cd phraseup

2. Crie e ative o ambiente virtual
# Windows

python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Configure as variáveis de ambiente
Crie um arquivo .env na raiz:

OPENAI_API_KEY="sua_chave_aqui"
ANTHROPIC_API_KEY="sua_chave_aqui"
GOOGLE_API_KEY="sua_chave_aqui"

5. Inicie a aplicação
streamlit run app.py

☁️ Deploy no Streamlit Cloud
- Faça push do código para o GitHub.
- Acesse share.streamlit.io.
- Selecione o repositório e o arquivo app.py.
- Em Advanced Settings → Secrets, adicione:

OPENAI_API_KEY = "sk-xxxx"
ANTHROPIC_API_KEY = "sk-ant-xxxx"
GOOGLE_API_KEY = "xxxx"

📊 Banco de Dados
- O PhraseUp utiliza SQLite local (phraseup.db), criado automaticamente.
- Tabela history: armazena texto original, refinado, nível e timestamp.
⚠️ Atenção: No Streamlit Cloud, o banco é volátil.
Para persistência real, considere usar Streamlit Connections.

👤 Autor
Luciano Paiva
Projeto focado em análise de dados, IA aplicada e evolução da comunicação escrita.



