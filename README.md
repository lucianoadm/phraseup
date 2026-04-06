✦ PhraseUp — Refinador de Linguagem com IA
Transforme textos simples em comunicação clara, profissional e persuasiva com o poder da Inteligência Artificial multimodelo.
O PhraseUp é uma ferramenta avançada de apoio à escrita que utiliza múltiplos provedores de LLM (Large Language Models) para refinar textos em diferentes níveis de formalidade e impacto, oferecendo também um ecossistema de treino e métricas de evolução.
🚀 Funcionalidades Principais
Tela	O que faz?
💬 Refinador	Interface principal para inserir textos e selecionar o nível de refinamento (Básico, Profissional ou Persuasivo).
📚 Biblioteca	Repositório centralizado com o histórico de todos os seus textos refinados para consulta rápida.
🔁 Modo Treino	Ambiente interativo para praticar a reescrita manual e comparar seu desempenho com as sugestões da IA.
📈 Evolução	Dashboard com métricas de progresso, score de clareza e análise de desenvolvimento da escrita.
🧠 Diferenciais Técnicos
Arquitetura Multi-IA: Sistema inteligente de fallback automático. Se um provedor falhar, o app alterna entre OpenAI, Anthropic e Google sem interromper a experiência.
Refinamento por Nível: Prompts otimizados para converter a intenção do usuário em resultados técnicos, executivos ou de vendas.
Persistência Inteligente: Banco de dados SQLite local integrado para gestão de histórico e progresso.
🗂 Estrutura do Projeto
bash
phraseup/
├── app.py                # Ponto de entrada (Main)
├── core/
│   ├── config.py         # Gestão de variáveis e validação de ambiente
│   └── llm.py            # Engine de IA (Multi-provider + Fallback logic)
├── services/
│   └── refinement.py     # Regras de negócio e lógica de refinamento
├── pages/                # Navegação multi-página do Streamlit
│   ├── chat.py           # Interface de refinamento
│   ├── library.py        # Gestão de histórico
│   ├── training.py       # Módulo de exercícios
│   └── evolution.py      # Painel de métricas
├── utils/
│   ├── db.py             # Interface SQLite
│   └── styles.py         # Customização de CSS/UI
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação
Use o código com cuidado.

⚙️ Instalação Local
Clone o repositório:
bash
git clone https://github.com/seu-usuario/phraseup.git
cd phraseup
Use o código com cuidado.

Crie e ative seu ambiente virtual:
bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
Use o código com cuidado.

Instale as dependências:
bash
pip install -r requirements.txt
Use o código com cuidado.

Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto:
env
OPENAI_API_KEY="sua_chave_aqui"
ANTHROPIC_API_KEY="sua_chave_aqui"
GOOGLE_API_KEY="sua_chave_aqui"
Use o código com cuidado.

Inicie a aplicação:
bash
streamlit run app.py
Use o código com cuidado.

☁️ Deploy no Streamlit Cloud
Faça o Push do código para seu repositório GitHub.
Acesse share.streamlit.io.
Selecione o repositório e o arquivo app.py.
Em Advanced Settings > Secrets, insira suas chaves no formato TOML:
toml
OPENAI_API_KEY = "sk-xxxx"
ANTHROPIC_API_KEY = "sk-ant-xxxx"
GOOGLE_API_KEY = "xxxx"
Use o código com cuidado.

📊 Banco de Dados
O sistema utiliza um banco SQLite local (phraseup.db) criado automaticamente no primeiro acesso.
Tabela history: Armazena textos originais, refinados, nível escolhido e timestamp.
⚠️ Nota sobre Deploy: No Streamlit Cloud, o banco .db é volátil. Para persistência permanente, recomenda-se integrar com Streamlit Connections.
👤 Autor
Luciano Paiva
Projeto focado em análise de dados, IA aplicada e evolução da comunicação escrita.
