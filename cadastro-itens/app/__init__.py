"""API pública do sistema de cadastro de itens."""

from .domain import CadastroItens, Item, ItemNaoEncontradoError
from .api import app

__all__ = ["CadastroItens", "Item", "ItemNaoEncontradoError", "app", "main"]


def main() -> None:
    """Ponto de entrada do pacote."""
    print("Sistema de cadastro de itens")
