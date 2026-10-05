"""Testes black-box dos endpoints HTTP do cadastro de itens."""

import pytest
from fastapi.testclient import TestClient

from app.api import app, cadastro


@pytest.fixture(autouse=True)
def limpar_cadastro() -> None:
    """Mantém cada cenário independente dos demais."""
    cadastro._itens.clear()
    cadastro._proximo_id = 1


@pytest.fixture
def cliente() -> TestClient:
    return TestClient(app)


@pytest.mark.integration
@pytest.mark.blackbox
def test_post_cadastra_item_com_sucesso(cliente: TestClient) -> None:
    # Arrange
    dados = {
        "nome": "  Teclado  ",
        "descricao": "USB",
        "preco": 99.90,
        "estoque": 10,
    }

    # Act
    resposta = cliente.post("/itens", json=dados)

    # Assert
    assert resposta.status_code == 201
    assert resposta.json() == {
        "id": 1,
        "nome": "Teclado",
        "descricao": "USB",
        "preco": 99.90,
        "estoque": 10,
    }


@pytest.mark.parametrize(
    "dados",
    [
        {"nome": "", "descricao": "Descrição", "preco": 10, "estoque": 1},
        {"nome": "Produto", "descricao": "Descrição", "preco": -1, "estoque": 1},
        {"nome": "Produto", "descricao": "Descrição", "preco": 10, "estoque": -1},
    ],
)
@pytest.mark.integration
@pytest.mark.blackbox
def test_post_rejeita_dados_de_particoes_invalidas(
    cliente: TestClient, dados: dict[str, object]
) -> None:
    # Arrange
    payload = dados

    # Act
    resposta = cliente.post("/itens", json=payload)

    # Assert
    assert resposta.status_code == 422
    assert "detail" in resposta.json()


@pytest.mark.integration
@pytest.mark.blackbox
def test_get_lista_itens_cadastrados(cliente: TestClient) -> None:
    # Arrange
    cliente.post(
        "/itens",
        json={"nome": "A", "descricao": "A", "preco": 0, "estoque": 0},
    )

    # Act
    resposta = cliente.get("/itens")

    # Assert
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["id"] == 1


@pytest.mark.parametrize(
    ("item_id", "status_esperado"),
    [(1, 200), (999, 404), (0, 422)],
)
@pytest.mark.integration
@pytest.mark.blackbox
def test_get_busca_item_por_id(
    cliente: TestClient, item_id: int, status_esperado: int
) -> None:
    # Arrange
    cliente.post(
        "/itens",
        json={"nome": "Produto", "descricao": "A", "preco": 10, "estoque": 1},
    )

    # Act
    resposta = cliente.get(f"/itens/{item_id}")

    # Assert
    assert resposta.status_code == status_esperado


@pytest.mark.parametrize(
    ("item_id", "dados", "status_esperado"),
    [
        (1, {"estoque": 0}, 200),
        (999, {"estoque": 0}, 404),
        (1, {"nome": ""}, 422),
    ],
)
@pytest.mark.integration
@pytest.mark.blackbox
def test_put_atualiza_item_e_trata_erros(
    cliente: TestClient,
    item_id: int,
    dados: dict[str, object],
    status_esperado: int,
) -> None:
    # Arrange
    cliente.post(
        "/itens",
        json={"nome": "Produto", "descricao": "A", "preco": 10, "estoque": 1},
    )

    # Act
    resposta = cliente.put(f"/itens/{item_id}", json=dados)

    # Assert
    assert resposta.status_code == status_esperado
    if status_esperado == 200:
        assert resposta.json()["estoque"] == 0


@pytest.mark.parametrize("item_id", [1, 999, 0])
@pytest.mark.integration
@pytest.mark.blackbox
def test_delete_remove_item_e_trata_ids_invalidos(
    cliente: TestClient, item_id: int
) -> None:
    # Arrange
    cliente.post(
        "/itens",
        json={"nome": "Produto", "descricao": "A", "preco": 10, "estoque": 1},
    )

    # Act
    resposta = cliente.delete(f"/itens/{item_id}")

    # Assert
    status_esperado = {1: 204, 999: 404, 0: 422}[item_id]
    assert resposta.status_code == status_esperado


@pytest.mark.integration
@pytest.mark.blackbox
def test_api_rejeita_campos_desconhecidos(cliente: TestClient) -> None:
    # Arrange
    dados = {
        "nome": "Produto",
        "descricao": "A",
        "preco": 10,
        "estoque": 1,
        "campo_extra": "inesperado",
    }

    # Act
    resposta = cliente.post("/itens", json=dados)

    # Assert
    assert resposta.status_code == 422
