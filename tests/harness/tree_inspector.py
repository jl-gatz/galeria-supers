# tests/harness/tree_inspector.py


from rich.tree import Tree


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

    def __init__(self, root):
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

    def children(self, control):
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

        kids = []

        if hasattr(control, "controls") and control.controls:
            kids.extend(control.controls)

        if hasattr(control, "content") and control.content:
            kids.append(control.content)

        if hasattr(control, "items") and control.items:
            kids.extend(control.items)

        if hasattr(control, "tabs") and control.tabs:
            kids.extend(control.tabs)

        if hasattr(control, "actions") and control.actions:
            kids.extend(control.actions)

        return [k for k in kids if k]

    # -------------------------
    # traversal
    # -------------------------

    def walk(self, node=None):
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

        node = node or self.root

        yield node

        for child in self.children(node):
            yield from self.walk(child)

    # -------------------------
    # selector helpers
    # -------------------------

    def _matches(self, node, selector):
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

    def find(self, selector):
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

    def first(self, selector):
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

    def one(self, selector):
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

    def count(self, selector):
        """
        Conta quantos elementos correspondem ao seletor.
        """

        return len(self.find(selector))

    # -------------------------
    # property queries
    # -------------------------

    def find_prop(self, prop, value):
        """
        Encontra elementos com um valor específico de propriedade.

        Example
        -------
        inspector.find_prop("key", "logo")
        """

        return [n for n in self.walk() if hasattr(n, prop) and getattr(n, prop) == value]

    def find_where(self, predicate):
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

    def find_children(self, node, selector):
        """
        Retorna os filhos diretos de um nó que correspondem ao seletor.
        """

        return [child for child in self.children(node) if self._matches(child, selector)]

    def find_descendants(self, node, selector):
        """
        Retorna todos os descendentes de um nó que correspondem ao seletor.
        """

        results = []

        for child in self.children(node):
            if self._matches(child, selector):
                results.append(child)

            results.extend(self.find_descendants(child, selector))

        return results

    def path_to(self, target):
        """
        Retorna o caminho da raiz até um nó específico.
        """

        def search(node, path):

            if node is target:
                return [*path, node]

            for child in self.children(node):
                result = search(child, [*path, node])

                if result:
                    return result

            return None

        return search(self.root, []) or []

    def find_ancestors(self, node):
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

    def find_path(self, path):
        """
        Encontra nós que correspondem a um caminho estrutural.

        O caminho pode ser fornecido como string ou lista.

        Example
        -------
        inspector.find_path("GalleryView GalleryRow Image")
        """

        if isinstance(path, str):
            path = path.split()

        def search(node, remaining):

            if not remaining:
                return [node]

            results = []

            for child in self.children(node):
                if self._matches(child, remaining[0]):
                    results.extend(search(child, remaining[1:]))

            return results

        results = []

        for node in self.walk():
            if self._matches(node, path[0]):
                results.extend(search(node, path[1:]))

        return results

    def count_path(self, path):
        """
        Conta quantas ocorrências existem para um caminho estrutural.
        """

        return len(self.find_path(path))

    # -------------------------
    # debug (plain)
    # -------------------------

    def print_tree(self):
        """
        Imprime a árvore de componentes em formato simples.
        """

        def _print(node, depth=0):

            indent = " " * depth
            print(f"{indent}{node.__class__.__name__}")

            for child in self.children(node):
                _print(child, depth + 2)

        _print(self.root)

    # -------------------------
    # debug (formatted)
    # -------------------------

    def format_tree(self, show_props=True, max_depth=None):
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

        lines = []

        def node_label(node):

            name = node.__class__.__name__

            if not show_props:
                return name

            props = []

            if hasattr(node, "key") and node.key:
                props.append(f"key='{node.key}'")

            if hasattr(node, "text") and node.text:
                props.append(f"text='{node.text}'")

            if hasattr(node, "src") and node.src:
                props.append(f"src='{node.src}'")

            if props:
                return f"{name} ({', '.join(props)})"

            return name

        def walk(node, depth=0):

            if max_depth is not None and depth > max_depth:
                return

            indent = " " * depth
            lines.append(f"{indent}{node_label(node)}")

            for child in self.children(node):
                walk(child, depth + 2)

        walk(self.root)

        return "\n".join(lines)

    def rich_tree(self, show_props=True, max_depth=None):
        """
        Retorna uma árvore visual usando a biblioteca Rich.

        Útil para debugging interativo nos testes.
        """

        def node_label(node):

            name = node.__class__.__name__

            if not show_props:
                return name

            props = []

            if hasattr(node, "key") and node.key:
                props.append(f"key='{node.key}'")

            if hasattr(node, "text") and node.text:
                props.append(f"text='{node.text}'")

            if hasattr(node, "src") and node.src:
                props.append(f"src='{node.src}'")

            if props:
                return f"{name} ({', '.join(props)})"

            return name

        def build(node, branch, depth=0):

            if max_depth is not None and depth > max_depth:
                return

            for child in self.children(node):
                child_branch = branch.add(node_label(child))
                build(child, child_branch, depth + 1)

        root = Tree(node_label(self.root))

        build(self.root, root)

        return root

    def descendants(self, node):
        """
        Iterador que retorna todos os descendentes de um nó.
        """

        for child in self.children(node):
            yield child
            yield from self.descendants(child)
