# # tests/debug/test_rich_tree_examples.py

# """
# Exemplos de uso das Rich Trees para debug da UI.

# Esses testes não validam comportamento. Eles servem como
# ferramentas de inspeção da árvore de controles durante o
# desenvolvimento.

# Execute com:

#     pytest -m debug -s

# O flag -s permite visualizar o output do Rich no terminal.
# """

# import pytest

# # pytestmark = pytest.mark.debug

# # ---------------------------------------------------------
# # 1. árvore estrutural básica
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_structure(mounted_gallery):
#     """
#     Imprime a árvore estrutural completa da GalleryView.

#     Útil para visualizar a hierarquia geral da interface.
#     """

#     mounted_gallery.rich_tree()


# # ---------------------------------------------------------
# # 2. árvore com propriedades
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_with_props(mounted_gallery):
#     """
#     Imprime a árvore exibindo propriedades relevantes
#     dos controles.
#     """

#     mounted_gallery.rich_tree(show_props=True)


# # ---------------------------------------------------------
# # 3. árvore filtrada por tipo
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_filter_supercards(mounted_gallery):
#     """
#     Mostra apenas controles do tipo SuperCard.

#     Útil para verificar carregamento de cards na galeria.
#     """

#     mounted_gallery.rich_tree(filter_type="SuperCard")


# # ---------------------------------------------------------
# # 4. árvore com índices de navegação
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_with_paths(mounted_gallery):
#     """
#     Imprime a árvore com índices de navegação.

#     Esses índices podem ser usados para localizar controles
#     específicos dentro da árvore.
#     """

#     mounted_gallery.rich_tree(show_index=True)


# # ---------------------------------------------------------
# # 5. árvore destacando um controle
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_highlight(mounted_gallery):
#     """
#     Destaca um controle específico na árvore.
#     """

#     card = mounted_gallery.select("SuperCard")

#     mounted_gallery.rich_tree(highlight=card)


# # ---------------------------------------------------------
# # 6. subárvore de um controle específico
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_subtree(mounted_gallery):
#     """
#     Mostra apenas a subárvore de um controle.

#     Útil para debugar containers específicos.
#     """

#     grid = mounted_gallery.select("GridView")

#     mounted_gallery.rich_tree(context=grid)


# # ---------------------------------------------------------
# # 7. estatísticas da árvore
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_stats(mounted_gallery):
#     """
#     Mostra estatísticas da árvore de controles.
#     """

#     mounted_gallery.rich_tree_stats()


# # ---------------------------------------------------------
# # 8. captura da árvore (snapshot manual)
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_capture(mounted_gallery):
#     """
#     Captura a árvore como string para inspeção manual.
#     """

#     tree = mounted_gallery.tree_string()

#     print()
#     print(tree)


# # ---------------------------------------------------------
# # 9. diff entre árvores
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_diff(mounted_gallery):
#     """
#     Exemplo de comparação entre duas árvores.
#     """

#     before = mounted_gallery.capture_tree()

#     # aqui normalmente ocorreria alguma ação de UI
#     # ex: mounted_gallery.load_more()

#     after = mounted_gallery.capture_tree()

#     mounted_gallery.rich_tree_diff(before, after)


# # ---------------------------------------------------------
# # 10. exploração manual da árvore
# # ---------------------------------------------------------


# @pytest.mark.debug
# def test_debug_tree_explore(mounted_gallery):
#     """
#     Teste livre para exploração da árvore durante o
#     desenvolvimento.
#     """

#     inspector = mounted_gallery.inspector

#     root = inspector.root

#     print("\nRoot:", root)

#     children = inspector.children(root)

#     print("\nChildren:", children)

#     mounted_gallery.rich_tree()
