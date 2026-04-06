✦ PhraseUp — Refinador de Linguagem

Transforme textos simples em comunicação clara, profissional e persuasiva com apoio de IA.

🚀 Funcionalidades
Tela	O que faz
💬 Refinador	Insere um texto → recebe versão refinada por nível (básico, profissional, persuasivo)
📚 Biblioteca	Histórico dos textos refinados
🔁 Modo Treino	Pratique reescrita e compare com a IA
📈 Evolução	Métricas de progresso e score de desenvolvimento
⚙️ Instalação local
# 1. Clone o repositório
git clone https://github.com/seu-usuario/phraseup.git
cd phraseup

# 2. Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente (.env)
# Crie um arquivo .env na raiz com:

OPENAI_API_KEY=sk-xxxx
ANTHROPIC_API_KEY=sk-ant-xxxx
GOOGLE_API_KEY=xxxx

# 5. Rode o app
streamlit run app.py
🔐 Configuração de API

O app utiliza múltiplos provedores de IA com fallback automático:

OpenAI
Anthropic
Google

Basta configurar pelo menos uma chave no .env.

☁️ Deploy no Streamlit Cloud
Faça push para seu repositório no GitHub
Acesse https://share.streamlit.io
Clique em New app → selecione app.py
Em Secrets, adicione:
OPENAI_API_KEY = "sk-xxxx"
ANTHROPIC_API_KEY = "sk-ant-xxxx"
GOOGLE_API_KEY = "xxxx"
Deploy
🗂 Estrutura do projeto
phraseup/
├── app.py
├── core/
│   ├── config.py          # Variáveis e validação de ambiente
│   └── llm.py             # Engine de IA (multi-provider + fallback)
├── services/
│   └── refinement.py      # Lógica de refinamento por nível
├── pages/
│   ├── chat.py
│   ├── library.py
│   ├── training.py
│   └── evolution.py
├── utils/
│   ├── db.py              # SQLite
│   └── styles.py
├── requirements.txt
├── .gitignore
└── README.md
📊 Banco de dados

SQLite local (phraseup.db) criado automaticamente com:

history — textos refinados + nível + timestamp
🧠 Diferenciais
Refinamento por nível (básico, profissional, persuasivo)
Sistema de treino ativo
Métricas de evolução do usuário
Arquitetura multi-IA com fallback automático
👤 Autor

Luciano Paiva
Projeto desenvolvido com foco em análise de dados, IA aplicada e evolução da comunicação escrita.

⚠️ Observações
O arquivo .env não deve ser versionado
O banco .db é local e não persistente em deploy gratuito
