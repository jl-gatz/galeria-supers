from pathlib import Path

import flet as ft

from tests.debug.rich_node import render_node
from tests.debug.rich_query import render_query
from tests.debug.rich_tree import render_tree
from tests.harness.tree_inspector import TreeInspector
from tests.stubs.fake_page import FakePage


class FletTestHarness:
    """
    Harness de testes para componentes de UI baseados em Flet.

    O `FletTestHarness` fornece uma camada de infraestrutura para testes de
    interface, permitindo montar componentes em uma página de teste e
    inspecionar a árvore de controles renderizada.

    Ele encapsula:

    - montagem de componentes em uma `Page` ou `FakePage`
    - navegação pela árvore de componentes
    - queries estruturais
    - visualização de debug (texto ou Rich)
    - snapshot testing da árvore de UI

    O harness delega a navegação estrutural ao `TreeInspector`, expondo uma
    API simplificada para uso direto nos testes.

    Uso típico
    ----------
    Normalmente o harness é utilizado via fixture do pytest:

    ```python
    async def test_gallery(mounted_gallery: FletTestHarness):
        assert mounted_gallery.count("GalleryRow") == 1
        assert mounted_gallery.count("Image") == 12
    ```

    Attributes
    ----------
    page : FakePage | ft.Page
        Página usada para montar os controles durante o teste.

    root : ft.Control | None
        Controle raiz atualmente montado.

    inspector : TreeInspector | None
        Utilitário responsável por percorrer e consultar a árvore de
        componentes.
    """

    def __init__(self, page: FakePage):
        """
        Inicializa o harness com uma página de teste.

        Parameters
        ----------
        page : FakePage | ft.Page
            Página onde os componentes serão montados.
        """
        self.page = page
        self.root = None
        self.inspector = None

    async def mount(self, control: ft.Control):
        """
        Monta um controle na página de teste.

        O método remove quaisquer controles existentes da página, adiciona o
        controle fornecido e executa atualização da página caso o método
        exista (`update_async` ou `update`).

        Após a montagem, um `TreeInspector` é criado para permitir consultas
        estruturais na árvore de componentes.

        Parameters
        ----------
        control : ft.Control
            Componente raiz a ser montado.
        """

        self.page.controls.clear()
        self.page.add(control)

        # suporta Page real e FakePage
        if hasattr(self.page, "update_async"):
            await self.page.update_async()
        elif hasattr(self.page, "update"):
            self.page.update()

        self.root = control
        self.inspector = TreeInspector(control)

    # ------------------------------------------------------------------
    # Query facade (TreeInspector delegation)
    # ------------------------------------------------------------------

    def find(self, selector: str):
        """
        Retorna todos os nós da árvore que correspondem ao seletor.

        Parameters
        ----------
        selector : str | type
            Nome da classe ou tipo do controle.

        Returns
        -------
        list[ft.Control]
        """
        self._ensure_mounted()
        return self.inspector.find(selector)

    def one(self, selector: str):
        """
        Retorna exatamente um nó correspondente ao seletor.

        Levanta erro se nenhum ou mais de um nó for encontrado.
        """
        self._ensure_mounted()
        return self.inspector.one(selector)

    def count(self, selector: str):
        """
        Conta quantos nós correspondem ao seletor.
        """
        self._ensure_mounted()
        return self.inspector.count(selector)

    def find_descendants(self, node, selector):
        """
        Busca descendentes de um nó específico que correspondem ao seletor.
        """
        return self.inspector.find_descendants(node, selector)

    def find_children(self, node, selector):
        """
        Busca apenas filhos diretos de um nó que correspondem ao seletor.
        """
        return self.inspector.find_children(node, selector)

    def count_path(self, path):
        """
        Conta ocorrências de uma sequência estrutural na árvore.

        Exemplo
        -------
        ```python
        harness.count_path(["GalleryView", "GalleryRow", "Image"])
        ```
        """
        return self.inspector.count_path(path)

    def _ensure_mounted(self):
        """
        Garante que um componente foi montado antes de executar queries.

        Muitos métodos do harness dependem da existência de um `TreeInspector`,
        que é inicializado apenas após a chamada de `mount()`.

        Este método atua como uma proteção interna (guard clause), impedindo que
        operações de inspeção da árvore sejam executadas antes da montagem do
        componente sob teste.

        Raises
        ------
        RuntimeError
            Caso o harness ainda não tenha sido inicializado com `mount()`.
        """

        if self.inspector is None:
            raise RuntimeError(
                "FletTestHarness não montado.\n"
                "Use: await harness.mount(control) antes de executar queries."
            )

    # ------------------------------------------------------------------
    # Selector engine
    # ------------------------------------------------------------------

    def select(self, selector: str):
        """
        Executa uma query hierárquica simples baseada em nomes de classe.

        O seletor usa uma sintaxe semelhante a CSS simplificado,
        representando uma sequência de descendência.

        Exemplos
        --------

        ```python
        harness.select("Image")

        harness.select("GalleryRow Image")

        harness.select("Column GalleryRow Image")
        ```

        Returns
        -------
        list[ft.Control]
        """
        self._ensure_mounted()
        parts = selector.split()
        current = [self.root]

        for part in parts:
            next_nodes = []

            for node in current:
                descendants = self.inspector.descendants(node)

                for d in descendants:
                    if d.__class__.__name__ == part:
                        next_nodes.append(d)

            current = next_nodes

        return current

    # ------------------------------------------------------------------
    # Debug utilities
    # ------------------------------------------------------------------

    def debug_tree(self):
        """
        Imprime uma representação textual simples da árvore de componentes.
        """
        print(self.inspector.format_tree())

    def rich_tree(self):
        """
        Retorna uma representação Rich da árvore de componentes.
        """
        return self.inspector.rich_tree()

    def rich_debug_tree(self):
        """
        Renderiza a árvore usando utilitários Rich customizados.
        """
        render_tree(self.root, self.inspector)

    def rich_query(self, selector):
        """
        Renderiza visualmente os resultados de uma query.
        """
        nodes = self.select(selector)
        render_query(nodes)

    def rich_node(self, node):
        """
        Exibe informações detalhadas de um nó específico.
        """
        render_node(node)

    # ------------------------------------------------------------------
    # Snapshot testing
    # ------------------------------------------------------------------

    def assert_tree_snapshot(self, snapshot_name: str):
        """
        Verifica se a árvore atual corresponde a um snapshot salvo.

        Se o snapshot ainda não existir, ele é criado automaticamente em
        `tests/snapshots/` e o teste falha para permitir revisão manual.

        Parameters
        ----------
        snapshot_name : str
            Nome do snapshot (sem extensão).

        Raises
        ------
        AssertionError
            Caso o snapshot não exista ou a árvore atual seja diferente.
        """

        tree = self.inspector.format_tree().strip()

        snapshot_path = Path("tests/snapshots") / f"{snapshot_name}.snap"

        if not snapshot_path.exists():
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_text(tree)

            raise AssertionError(
                f"Snapshot criado em {snapshot_path}. Revise o arquivo e rode os testes novamente."
            )

        expected = snapshot_path.read_text().strip()

        assert tree == expected
