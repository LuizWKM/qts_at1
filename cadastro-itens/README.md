# qts_at1
Engenharia de Testes Unitários, Cobertura de Código e Governança de IA

# Utilização da IA no projeto:
- Criação do sistema simples de cadastro de itens.
- Criação, sob supervisão dos testes, levando em consideração o AGENTS.MD e o PRD.MD.
- Verificado manualmente que estão funcionando todas as funcionalidades implementadas, para manter auditoria sobre o que é feito pela IA.

# IA utilizada:
- Github Copilot

# Arquivo gerados com IA:
- app\api.py
- app\domain.py
- tests\test_api.py
- tests\test_domain.py

# Texto utilizado para criar os tests via Github Copilot(AI):
- Agora lendo o AGENTS.MD, faça testes unitário com Pytest estruturados no Padrão Arrange, Act, Assert. Aplique particionamento de equivalência EP e Analise de vfalor limite (BVA). Testes de Error Guessing para cenários de entradas inválidas ou inesperadas. Utilize @pytest.mark.parametrize e marcações @pytest.mark.unit, além de utilizar os markers do pyproject.toml quando necessário. Suíte com quantidade considerável de cenários/asserções de teste em torno de 15 a 20 testes e Medição com **pytest-cov** (`--cov-branch`) atingindo **100% de cobertura de código e ramificações** nas regras de negócio.

# Execução dos comandos
- Executar os comandos abaixo dentro da pasta cadastro-itens:

# Instalar/sincronizar dependências
uv sync --dev

# Executar os testes
uv run pytest -v

# Executar os testes com cobertura de linhas e branches
uv run pytest --cov=app --cov-branch --cov-report=term-missing

# Para executar a api:
- uv run fastapi dev app/api.py

# Swagger fica disponível em:
- http://127.0.0.1:8000/docs