from collections.abc import Callable, Iterator, Sequence

from rich.tree import Tree

from tests.utils.tree_helpers import get_children
from tests.utils.types import HasKey, HasSrc, HasText, Selector


class TreeInspector:
    """
    Utilitário para inspeção e navegação na árvore de componentes Flet.

    O TreeInspector fornece um conjunto de métodos para percorrer,
    consultar e depurar a estrutura de controles de uma interface.

    Ele é utilizado principalmente pelo FletTestHarness para permitir
    assertions estruturais nos testes de UI.

    Exemplos
    --------
    inspector.find("Image")
    inspector.one("GalleryRow")
    inspector.count("Text")
    inspector.find_path("GalleryView GalleryRow Image")
    """

    def __init__(self, root: object) -> None:
        """
        Inicializa o inspector com o nó raiz da árvore.

        Parameters
        ----------
        root : Control
            Controle raiz da árvore de componentes.
        """
        self.root = root

    # -------------------------
    # child discovery
    # -------------------------

    def children(self, control: object) -> list[object]:
        """
        Retorna os filhos diretos de um controle.

        Diferentes componentes Flet expõem seus filhos em atributos
        distintos. Este método normaliza o acesso a esses filhos,
        verificando atributos comuns como:

        - controls
        - content
        - items
        - tabs
        - actions

        Parameters
        ----------
        control : Control
            Controle a ser inspecionado.

        Returns
        -------
        list[Control]
            Lista de filhos diretos do controle.
        """
        return get_children(control)

    # -------------------------
    # traversal
    # -------------------------

    def walk(self, node: object | None = None) -> Iterator[object]:
        """
        Percorre a árvore de controles em profundidade (DFS).

        Itera recursivamente sobre todos os nós da árvore,
        começando pelo nó fornecido ou pela raiz.

        Parameters
        ----------
        node : Control | None
            Nó inicial da travessia. Se None, usa a raiz.

        Yields
        ------
        Control
            Cada nó da árvore.
        """

        if node is None:
            node = self.root

        yield node

        for child in self.children(node):
            yield from self.walk(child)

    # -------------------------
    # selector helpers
    # -------------------------

    def _matches(self, node: object, selector: Selector) -> bool:
        """
        Verifica se um nó corresponde a um seletor.

        O seletor pode ser:

        - uma string (nome da classe)
        - um tipo/classe Python

        Examples
        --------
        inspector.find("Image")
        inspector.find(ft.Image)
        """

        if isinstance(selector, str):
            return node.__class__.__name__ == selector

        return isinstance(node, selector)

    # -------------------------
    # base queries
    # -------------------------

    def find(self, selector: Selector) -> list[object]:
        """
        Retorna todos os nós que correspondem ao seletor.

        Parameters
        ----------
        selector : str | type

        Returns
        -------
        list[Control]
        """

        return [n for n in self.walk() if self._matches(n, selector)]

    def first(self, selector: Selector) -> object:
        """
        Retorna o primeiro elemento que corresponde ao seletor.

        Raises
        ------
        AssertionError
            Se nenhum elemento for encontrado.
        """

        results = self.find(selector)

        if not results:
            raise AssertionError(f"No element found for {selector}")

        return results[0]

    def one(self, selector: Selector) -> object:
        """
        Retorna exatamente um elemento que corresponde ao seletor.

        Raises
        ------
        AssertionError
            Se nenhum ou mais de um elemento for encontrado.
        """

        results = self.find(selector)

        if len(results) != 1:
            name = selector if isinstance(selector, str) else selector.__name__
            raise AssertionError(f"Expected 1 {name}, got {len(results)}")

        return results[0]

    def count(self, selector: Selector) -> int:
        """
        Conta quantos elementos correspondem ao seletor.
        """

        return len(self.find(selector))

    # -------------------------
    # property queries
    # -------------------------

    def find_prop(self, prop: str, value: object) -> list[object]:
        """
        Encontra elementos com um valor específico de propriedade.

        Example
        -------
        inspector.find_prop("key", "logo")
        """

        return [n for n in self.walk() if hasattr(n, prop) and getattr(n, prop) == value]

    def find_where(self, predicate: Callable[[object], bool]) -> list[object]:
        """
        Encontra elementos que satisfaçam um predicado.

        Parameters
        ----------
        predicate : Callable[[Control], bool]
        """

        return [n for n in self.walk() if predicate(n)]

    # -------------------------
    # structural queries
    # -------------------------

    def find_children(self, node: object, selector: Selector) -> list[object]:
        """
        Retorna os filhos diretos de um nó que correspondem ao seletor.
        """

        return [child for child in self.children(node) if self._matches(child, selector)]

    def find_descendants(self, node: object, selector: Selector) -> list[object]:
        """
        Retorna todos os descendentes de um nó que correspondem ao seletor.
        """

        results: list[object] = []

        for child in self.children(node):
            if self._matches(child, selector):
                results.append(child)

            results.extend(self.find_descendants(child, selector))

        return results

    def path_to(self, target: object) -> list[object]:
        """
        Retorna o caminho da raiz até um nó específico.
        """

        def search(node: object, path: list[object]) -> list[object] | None:

            if node is target:
                return [*path, node]

            for child in self.children(node):
                result = search(child, [*path, node])

                if result:
                    return result

            return None

        return search(self.root, []) or []

    def find_ancestors(self, node: object) -> list[object]:
        """
        Retorna todos os ancestrais de um nó.
        """

        path = self.path_to(node)

        if not path:
            return []

        return path[:-1]

    # -------------------------
    # path queries
    # -------------------------

    def find_path(self, path: str | Sequence[str]) -> list[object]:
        """
        Encontra nós que correspondem a um caminho estrutural.

        O caminho pode ser fornecido como string ou lista.

        Example
        -------
        inspector.find_path("GalleryView GalleryRow Image")
        """

        if isinstance(path, str):
            path = path.split()

        def search(node: object, remaining: Sequence[str]) -> list[object]:

            if not remaining:
                return [node]

            results: list[object] = []

            for child in self.children(node):
                if self._matches(child, remaining[0]):
                    results.extend(search(child, remaining[1:]))

            return results

        results: list[object] = []

        for node in self.walk():
            if self._matches(node, path[0]):
                results.extend(search(node, path[1:]))

        return results

    def count_path(self, path: str | Sequence[str]) -> int:
        """
        Conta quantas ocorrências existem para um caminho estrutural.
        """

        return len(self.find_path(path))

    # -------------------------
    # debug (plain)
    # -------------------------

    def print_tree(self) -> None:
        """
        Imprime a árvore de componentes em formato simples.
        """

        def _print(node: object, depth: int = 0) -> None:

            indent = " " * depth
            print(f"{indent}{node.__class__.__name__}")

            for child in self.children(node):
                _print(child, depth + 2)

        _print(self.root)

    # -------------------------
    # debug (formatted)
    # -------------------------

    def format_tree(self, show_props: bool = True, max_depth: int | None = None) -> str:
        """
        Retorna uma representação textual formatada da árvore.

        Pode incluir propriedades úteis como:
        - key
        - text
        - src

        Parameters
        ----------
        show_props : bool
        max_depth : int | None
        """

        lines: list[str] = []

        def node_label(node: object) -> str:

            name = node.__class__.__name__

            if not show_props:
                return name

            props: list[str] = []

            if isinstance(node, HasKey) and node.key:
                props.append(f"key='{node.key}'")

            if isinstance(node, HasText) and node.text:
                props.append(f"text='{node.text}'")

            if isinstance(node, HasSrc) and node.src:
                props.append(f"src='{node.src}'")

            if props:
                return f"{name} ({', '.join(props)})"

            return name

        def walk(node: object, depth: int = 0) -> None:

            if max_depth is not None and depth > max_depth:
                return

            indent = " " * depth
            lines.append(f"{indent}{node_label(node)}")

            for child in self.children(node):
                walk(child, depth + 2)

        walk(self.root)

        return "\n".join(lines)

    def rich_tree(self, show_props: bool = True, max_depth: int | None = None) -> Tree:
        """
        Retorna uma árvore visual usando a biblioteca Rich.

        Útil para debugging interativo nos testes.
        """

        def node_label(node: object) -> str:

            name = node.__class__.__name__

            if not show_props:
                return name

            props: list[str] = []

            if isinstance(node, HasKey) and node.key:
                props.append(f"key='{node.key}'")

            if isinstance(node, HasText) and node.text:
                props.append(f"text='{node.text}'")

            if isinstance(node, HasSrc) and node.src:
                props.append(f"src='{node.src}'")

            if props:
                return f"{name} ({', '.join(props)})"

            return name

        def build(node: object, branch: Tree, depth: int = 0) -> None:

            if max_depth is not None and depth > max_depth:
                return

            for child in self.children(node):
                child_branch = branch.add(node_label(child))
                build(child, child_branch, depth + 1)

        root = Tree(node_label(self.root))

        build(self.root, root)

        return root

    def descendants(self, node: object) -> Iterator[object]:
        """
        Iterador que retorna todos os descendentes de um nó.
        """

        for child in self.children(node):
            yield child
            yield from self.descendants(child)
