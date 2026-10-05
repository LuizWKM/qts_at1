"""Regras de negócio do cadastro de itens."""

from dataclasses import dataclass
from math import isfinite
from typing import Optional


class ItemNaoEncontradoError(LookupError):
    """Indica que o identificador informado não pertence a um item cadastrado."""


@dataclass(frozen=True, slots=True)
class Item:
    """Representa um item disponível no cadastro."""

    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int


class CadastroItens:
    """Gerencia itens em memória e aplica as validações do domínio."""

    def __init__(self) -> None:
        self._itens: dict[int, Item] = {}
        self._proximo_id = 1

    def cadastrar(
        self,
        nome: str,
        descricao: str,
        preco: float,
        estoque: int,
    ) -> Item:
        """Cadastra um item e retorna a entidade criada."""
        nome_validado = self._validar_texto(nome, "nome")
        descricao_validada = self._validar_texto(descricao, "descrição")
        preco_validado = self._validar_preco(preco)
        estoque_validado = self._validar_estoque(estoque)

        item = Item(
            id=self._proximo_id,
            nome=nome_validado,
            descricao=descricao_validada,
            preco=preco_validado,
            estoque=estoque_validado,
        )
        self._itens[item.id] = item
        self._proximo_id += 1
        return item

    def listar(self) -> list[Item]:
        """Retorna os itens cadastrados ordenados pelo identificador."""
        return list(self._itens.values())

    def buscar(self, item_id: int) -> Item:
        """Busca um item pelo identificador."""
        self._validar_id(item_id)
        try:
            return self._itens[item_id]
        except KeyError as error:
            raise ItemNaoEncontradoError(
                f"Item com id {item_id} não foi encontrado."
            ) from error

    def atualizar(
        self,
        item_id: int,
        *,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
        preco: Optional[float] = None,
        estoque: Optional[int] = None,
    ) -> Item:
        """Atualiza os campos informados e retorna o item atualizado."""
        item = self.buscar(item_id)

        item_atualizado = Item(
            id=item.id,
            nome=item.nome if nome is None else self._validar_texto(nome, "nome"),
            descricao=(
                item.descricao
                if descricao is None
                else self._validar_texto(descricao, "descrição")
            ),
            preco=item.preco if preco is None else self._validar_preco(preco),
            estoque=(
                item.estoque
                if estoque is None
                else self._validar_estoque(estoque)
            ),
        )
        self._itens[item_id] = item_atualizado
        return item_atualizado

    def remover(self, item_id: int) -> None:
        """Remove um item do cadastro."""
        self.buscar(item_id)
        del self._itens[item_id]

    @staticmethod
    def _validar_id(item_id: int) -> None:
        if isinstance(item_id, bool) or not isinstance(item_id, int) or item_id <= 0:
            raise ValueError("O id deve ser um inteiro positivo.")

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"O campo {campo} deve ser um texto não vazio.")
        return valor.strip()

    @staticmethod
    def _validar_preco(preco: float) -> float:
        if isinstance(preco, bool) or not isinstance(preco, (int, float)):
            raise ValueError("O preço deve ser um número.")
        if not isfinite(preco) or preco < 0:
            raise ValueError("O preço deve ser um número finito não negativo.")
        return float(preco)

    @staticmethod
    def _validar_estoque(estoque: int) -> int:
        if isinstance(estoque, bool) or not isinstance(estoque, int):
            raise ValueError("O estoque deve ser um inteiro.")
        if estoque < 0:
            raise ValueError("O estoque não pode ser negativo.")
        return estoque