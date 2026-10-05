"""Testes unitários das regras de negócio do cadastro de itens."""

from math import inf, nan

import pytest

from app import main
from app.domain import CadastroItens, ItemNaoEncontradoError


@pytest.mark.unit
def test_main_exibe_nome_do_sistema(capsys: pytest.CaptureFixture[str]) -> None:
    # Arrange
    esperado = "Sistema de cadastro de itens\n"

    # Act
    main()

    # Assert
    assert capsys.readouterr().out == esperado


@pytest.mark.unit
@pytest.mark.whitebox
def test_cadastrar_normaliza_dados_e_lista_item() -> None:
    # Arrange
    cadastro = CadastroItens()

    # Act
    item = cadastro.cadastrar("  Teclado  ", "  USB  ", 99.90, 10)

    # Assert
    assert item.id == 1
    assert item.nome == "Teclado"
    assert item.descricao == "USB"
    assert item.preco == 99.90
    assert item.estoque == 10
    assert cadastro.listar() == [item]


@pytest.mark.unit
@pytest.mark.whitebox
def test_listar_preserva_ordem_dos_identificadores() -> None:
    # Arrange
    cadastro = CadastroItens()
    primeiro = cadastro.cadastrar("Primeiro", "A", 1, 1)
    segundo = cadastro.cadastrar("Segundo", "B", 2, 2)

    # Act
    itens = cadastro.listar()

    # Assert
    assert itens == [primeiro, segundo]
    assert [item.id for item in itens] == [1, 2]


@pytest.mark.unit
@pytest.mark.whitebox
def test_atualizar_preserva_campos_omitidos() -> None:
    # Arrange
    cadastro = CadastroItens()
    original = cadastro.cadastrar("Produto", "Descrição", 20, 5)

    # Act
    atualizado = cadastro.atualizar(original.id, estoque=0)

    # Assert
    assert atualizado.id == original.id
    assert atualizado.nome == original.nome
    assert atualizado.descricao == original.descricao
    assert atualizado.preco == original.preco
    assert atualizado.estoque == 0


@pytest.mark.unit
@pytest.mark.whitebox
def test_atualizar_altera_todos_os_campos() -> None:
    # Arrange
    cadastro = CadastroItens()
    item = cadastro.cadastrar("Antigo", "Descrição antiga", 10, 1)

    # Act
    atualizado = cadastro.atualizar(
        item.id,
        nome="Novo",
        descricao="Descrição nova",
        preco=0,
        estoque=0,
    )

    # Assert
    assert atualizado.nome == "Novo"
    assert atualizado.descricao == "Descrição nova"
    assert atualizado.preco == 0
    assert atualizado.estoque == 0


@pytest.mark.unit
@pytest.mark.whitebox
def test_buscar_e_remover_item() -> None:
    # Arrange
    cadastro = CadastroItens()
    item = cadastro.cadastrar("Produto", "Descrição", 10, 1)

    # Act
    encontrado = cadastro.buscar(item.id)
    cadastro.remover(item.id)

    # Assert
    assert encontrado == item
    assert cadastro.listar() == []
    with pytest.raises(ItemNaoEncontradoError):
        cadastro.buscar(item.id)


@pytest.mark.parametrize("item_id", [0, -1, True, "1"])
@pytest.mark.unit
@pytest.mark.whitebox
def test_rejeita_ids_invalidos(item_id: object) -> None:
    # Arrange
    cadastro = CadastroItens()

    # Act / Assert
    with pytest.raises(ValueError, match="id deve ser um inteiro positivo"):
        cadastro.buscar(item_id)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("campo", "nome", "descricao"),
    [
        ("nome", "", "Descrição"),
        ("nome", "   ", "Descrição"),
        ("nome", None, "Descrição"),
        ("descrição", "Produto", ""),
        ("descrição", "Produto", "   "),
        ("descrição", "Produto", None),
    ],
)
@pytest.mark.unit
@pytest.mark.whitebox
def test_rejeita_textos_invalidos(campo: str, nome: object, descricao: object) -> None:
    # Arrange
    cadastro = CadastroItens()

    # Act / Assert
    with pytest.raises(ValueError, match=rf"campo {campo} deve ser um texto não vazio"):
        cadastro.cadastrar(nome, descricao, 10, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize("preco", ["10", None, True, object()])
@pytest.mark.unit
@pytest.mark.whitebox
def test_rejeita_precos_com_tipo_invalido(preco: object) -> None:
    # Arrange
    cadastro = CadastroItens()

    # Act / Assert
    with pytest.raises(ValueError, match="preço deve ser um número"):
        cadastro.cadastrar("Produto", "Descrição", preco, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize("preco", [nan, inf, -inf, -0.01])
@pytest.mark.unit
@pytest.mark.whitebox
def test_rejeita_precos_nao_finitos_ou_negativos(preco: float) -> None:
    # Arrange
    cadastro = CadastroItens()

    # Act / Assert
    with pytest.raises(ValueError, match="preço deve ser um número finito não negativo"):
        cadastro.cadastrar("Produto", "Descrição", preco, 1)


@pytest.mark.parametrize("estoque", [-1, 1.5, "1", True, None])
@pytest.mark.unit
@pytest.mark.whitebox
def test_rejeita_estoques_invalidos(estoque: object) -> None:
    # Arrange
    cadastro = CadastroItens()

    # Act / Assert
    with pytest.raises((ValueError, TypeError)):
        cadastro.cadastrar("Produto", "Descrição", 10, estoque)  # type: ignore[arg-type]
