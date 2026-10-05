# Requisitos de Segurança e Eficiência - Cadastro de itens

# Requisitos de Segurança (ISO 25010)
- O nome do produto e descricao não devem ser vazios.
- O preco deve ser um número e não pode ser não finito e nem negativo
- O estoque deve ser um número e não pode ser negativo.
- Se o nome ou descricao forem vazios, o sistema deve lançar um erro `ValueError` com a mensagem: "O campo {campo} deve ser um texto não vazio."
- Espaços extras no início ou no fim da nome do produto e descricao devem ser removidos (sanitização) antes da validação.
- Se o preco não for um número deve lançar um erro `ValueError` com a mensagem: "O preço deve ser um número."
- Se o preco for um número não finito ou negativo deve lançar um erro `ValueError` com a mensagem: "O preço deve ser um número finito não negativo."
- Se o estoque não for um número deve lançar um erro `ValueError` com a mensagem: "O estoque deve ser um inteiro."
- Se o estoque for um número negativo deve lançar um erro `ValueError` com a mensagem: "O estoque não pode ser negativo."

## Requisitos de Eficiência (ISO 25010)
- Os itens devem ser armazenados em memória associados aos seus identificadores únicos.
- As operações de busca, atualização e remoção devem localizar o item pelo identificador sem percorrer todos os itens cadastrados.
- A listagem deve retornar somente os itens cadastrados, mantendo a ordem dos identificadores.
- O sistema deve manter uma estrutura principal de armazenamento, sem estruturas auxiliares permanentes desnecessárias, mantendo o consumo de memória proporcional à quantidade de itens cadastrados.