"""API HTTP do cadastro de itens."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from .domain import CadastroItens, Item, ItemNaoEncontradoError


class ItemEntrada(BaseModel):
    """Dados necessários para cadastrar ou atualizar um item."""

    model_config = ConfigDict(extra="forbid")

    nome: str
    descricao: str
    preco: float
    estoque: int


class ItemAtualizacao(BaseModel):
    """Campos opcionais para uma atualização parcial."""

    model_config = ConfigDict(extra="forbid")

    nome: str | None = None
    descricao: str | None = None
    preco: float | None = Field(default=None, ge=0)
    estoque: int | None = Field(default=None, ge=0)


class ItemResposta(ItemEntrada):
    """Representação de um item retornado pela API."""

    id: int

    model_config = ConfigDict(from_attributes=True)


app = FastAPI(title="Cadastro de Itens", version="1.0.0")
cadastro = CadastroItens()


def _resposta(item: Item) -> ItemResposta:
    return ItemResposta.model_validate(item)


@app.post("/itens", response_model=ItemResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_item(dados: ItemEntrada) -> ItemResposta:
    """Cadastra um novo item."""
    try:
        item = cadastro.cadastrar(**dados.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return _resposta(item)


@app.get("/itens", response_model=list[ItemResposta])
def listar_itens() -> list[ItemResposta]:
    """Lista todos os itens cadastrados."""
    return [_resposta(item) for item in cadastro.listar()]


@app.get("/itens/{item_id}", response_model=ItemResposta)
def buscar_item(item_id: int) -> ItemResposta:
    """Busca um item pelo identificador."""
    try:
        return _resposta(cadastro.buscar(item_id))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except ItemNaoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.put("/itens/{item_id}", response_model=ItemResposta)
def atualizar_item(item_id: int, dados: ItemAtualizacao) -> ItemResposta:
    """Atualiza os campos enviados de um item."""
    try:
        item = cadastro.atualizar(item_id, **dados.model_dump(exclude_unset=True))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except ItemNaoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return _resposta(item)


@app.delete("/itens/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item(item_id: int) -> None:
    """Remove um item pelo identificador."""
    try:
        cadastro.remover(item_id)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except ItemNaoEncontradoError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error