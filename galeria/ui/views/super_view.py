# galeria/ui/views/super_view.py
"""Overlay de detalhe de um superintendente e sua linha do tempo."""

from collections.abc import Callable
from typing import Any, cast, override

import flet as ft

from galeria.core.config import ANIMATE_OPACITY, AUTO_TIME_VIEW_BACK
from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.behaviors import AutoCloseBehavior
from galeria.ui.components import (
    FloatingNavButton,
    NavigationControls,
    SuperHeader,
)
from galeria.ui.components.timeline import (
    PathBuilder,
    TimelineController,
    TimelineModel,
    TimelineRenderer,
    TimelineStyle,
    TimelineView,
    extract_points_from_super,
)
from galeria.ui.components.timeline.models import TimelinePoint
from galeria.ui.controllers import SuperDetailController
from galeria.ui.theme.models import Theme


class SuperDetail(ft.Container):
    """Visão em overlay que apresenta um superintendente em detalhe.

    O componente coordena cabeçalho, navegação anterior/próxima, seleção na
    linha do tempo, atualização de tema e fechamento automático enquanto está
    montado sobre a galeria.
    """

    def __init__(
        self,
        controller: SuperDetailController,
        on_request_close: Callable[[], None],
        theme_manager: ThemeManagerLike,
    ):
        super().__init__()

        # 🎯 Dependências
        self.controller = controller
        self._on_request_close = on_request_close
        self.theme_manager = theme_manager

        # 🔗 tema reativo
        self.theme_manager.subscribe(self.apply_theme)

        # ⏱️ Timeout
        self.auto_close = AutoCloseBehavior(
            seconds=AUTO_TIME_VIEW_BACK,
            on_timeout=self._timeout_close,
        )

        # 🎬 Estado visual
        self.opacity = 0
        self.expand = True
        self.alignment = ft.Alignment.CENTER
        self.animate_opacity = ft.Animation(ANIMATE_OPACITY)

        # 🎨 Timeline
        points = extract_points_from_super(self.controller.timeline_points)
        model = TimelineModel(points)

        timeline_controller = TimelineController(model, on_point_selected=self._handle_timeline_point)

        self.timeline_style = TimelineStyle(self.theme_manager.theme)
        renderer = TimelineRenderer(self.timeline_style)

        self.timeline_view = TimelineView(
            controller=timeline_controller,
            path_builder=PathBuilder(),
            renderer=renderer,
        )

        # 🧩 Componentes
        self.header = self._build_header()
        self.navigation = self._build_navigation()

        # 🧱 Layout
        self.main_container = self._build_main_container()
        self.content = self._build_layout()

        # 🚀 Lifecycle
        self._mounted = False

    # =========================================================
    # 🎨 THEME
    # =========================================================
    def apply_theme(self, theme: Theme) -> None:
        """Aplica uma atualização de tema à superfície e à timeline."""
        if not hasattr(self, "inner_container"):
            return

        cast(Any, self.timeline_style).apply_theme(theme)

        if hasattr(self, "timeline_view"):
            self.timeline_view.refresh()

        self.inner_container.bgcolor = getattr(
            theme.super_detail,
            "background",
            theme.base.surface,
        )
        self.inner_container.shadow = ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
            color=theme.ui.shadow,
        )

        if self._mounted:
            self.update()

    # -------------------------
    # 🎬 Animações
    # -------------------------
    def _fade_in(self) -> None:
        """Exibe o overlay e inicia o autofechamento apenas após a montagem."""
        self.opacity = 1

        if self._mounted:
            self.update()
            self.auto_close.start()

    def _fade_out(self) -> None:
        """Oculta o overlay e interrompe o temporizador de autofechamento."""
        self.auto_close.stop()
        self.opacity = 0
        self.update()

    # =========================================================
    # 🧱 BUILDERS
    # =========================================================

    def _build_main_container(self):
        """Monta a superfície temática que contém o detalhe."""
        self.inner_container = ft.Container(
            expand=True,
            padding=60,
            border_radius=20,
            bgcolor=getattr(
                self.theme_manager.theme.super_detail,
                "background",
                self.theme_manager.theme.base.surface,
            ),
            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=2,
                color=self.theme_manager.theme.ui.shadow,
            ),
            content=self._build_main_column(),
        )

        return ft.Container(
            alignment=ft.Alignment.CENTER,
            expand=True,
            content=self.inner_container,
        )

    def _build_layout(self):
        """Monta a pilha raiz do overlay."""
        return ft.Stack(
            expand=True,
            controls=[
                self.main_container,
            ],
        )

    def _build_main_column(self):
        """Monta a composição vertical de cabeçalho, navegação e timeline."""
        return ft.Column(
            expand=True,
            spacing=40,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.header,
                self.navigation,
                self._build_timeline_section(),
            ],
        )

    def _build_timeline_section(self):
        """Monta a área da timeline e sobrepõe a ação de voltar."""
        return ft.Container(
            expand=True,
            height=300,
            content=ft.Stack(
                expand=True,
                fit=ft.StackFit.EXPAND,
                controls=[
                    self.timeline_view.control,
                    ft.Container(
                        right=0,
                        bottom=0,
                        width=96,
                        height=96,
                        content=self._build_fab(),
                    ),
                ],
            ),
        )

    def _build_fab(self):
        """Monta o botão flutuante de voltar da visão de detalhe."""
        return FloatingNavButton.back(
            on_click=self._handle_voltar,
            key="detail_back",
            theme_manager=self.theme_manager,
        )

    # =========================================================
    # 🧩 SUBCOMPONENTES
    # =========================================================

    def _build_header(self):
        """Monta o cabeçalho do superintendente com o texto do slide atual."""
        return SuperHeader(
            theme_manager=self.theme_manager,
            image_src=self.controller.image_src,
            nome=self.controller.nome,
            periodo=self.controller.periodo,
            texto_inicial=self.controller.current,
            expand=True,
        )

    def _build_navigation(self):
        """Monta controles anterior/próximo ligados ao controlador de slides."""
        return NavigationControls(
            on_prev=self.prev,
            on_next=self.next,
            theme_manager=self.theme_manager,
        )

    # =========================================================
    # 🎮 INTERAÇÕES
    # =========================================================

    def next(self, e: ft.ControlEvent | None = None) -> None:
        """Avança para o próximo slide e reinicia o timeout de inatividade."""
        if self.controller.next():
            self._refresh_slide()
            self.auto_close.reset()

    def prev(self, e: ft.ControlEvent | None = None) -> None:
        """Retorna ao slide anterior e reinicia o timeout de inatividade."""
        if self.controller.prev():
            self._refresh_slide()
            self.auto_close.reset()

    def _goto_slide(self, index: int) -> None:
        """Vai para um slide pelo índice e atualiza o texto visível."""
        if self.controller.goto(index):
            self._refresh_slide()

    def _handle_voltar(self, e: ft.ControlEvent) -> None:
        """Fecha o overlay a partir da ação explícita de voltar."""
        self.auto_close.stop()
        self._on_request_close()

    def _timeout_close(self) -> None:
        """Fecha o overlay quando o temporizador de inatividade expira."""
        self._on_request_close()

    def _handle_timeline_point(self, point: TimelinePoint) -> None:
        """Reflete no cabeçalho o ponto selecionado na timeline."""
        # print(
        #     "SUPER DETAIL TIMELINE CALLBACK:",
        #     f"id={point.id}",
        #     f"year={point.year}",
        #     f"label={point.label}",
        # )
        self.header.set_timeline_event(point.year, point.label, point.text)
        self.auto_close.reset()

    # =========================================================
    # 🔄 ATUALIZAÇÃO
    # =========================================================

    def _refresh_slide(self) -> None:
        """Atualiza o texto do cabeçalho a partir do slide atual."""
        if not self._mounted:
            return

        self.header.update_text(self.controller.current)

    # =========================================================
    # 🎬 LIFECYCLE
    # =========================================================
    @override
    def did_mount(self):
        """Finaliza tema e animação depois que o Flet monta o overlay."""
        self._mounted = True

        self.apply_theme(self.theme_manager.theme)

        self._fade_in()
        self.timeline_view.refresh()
