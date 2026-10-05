"""API pública do sistema de cadastro de itens."""

from .domain import CadastroItens, Item, ItemNaoEncontradoError

__all__ = ["CadastroItens", "Item", "ItemNaoEncontradoError", "main"]


def main() -> None:
    """Ponto de entrada do pacote."""
    print("Sistema de cadastro de itens")
