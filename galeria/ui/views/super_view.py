# galeria/ui/views/super_view.py

from collections.abc import Callable
from typing import override

import flet as ft

from galeria.core.config import ANIMATE_OPACITY, AUTO_TIME_VIEW_BACK
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
from galeria.ui.controllers import SuperDetailController
from galeria.ui.theme.manager import ThemeManager


class SuperDetail(ft.Container):
    def __init__(
        self,
        controller: SuperDetailController,
        on_request_close: Callable[[], None],
        theme_manager: ThemeManager,
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

        timeline_controller = TimelineController(model)

        renderer = TimelineRenderer(TimelineStyle())  # 🔜 próximo passo: tematizar

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
    def apply_theme(self, theme):
        if not hasattr(self, "inner_container"):
            return

        self.inner_container.bgcolor = theme.base.surface
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
        self.opacity = 1

        if self._mounted:
            self.update()
            self.auto_close.start()

    def _fade_out(self) -> None:
        self.auto_close.stop()
        self.opacity = 0
        self.update()

    # =========================================================
    # 🧱 BUILDERS
    # =========================================================

    def _build_main_container(self):
        self.inner_container = ft.Container(
            expand=True,
            padding=60,
            border_radius=20,
            bgcolor=self.theme_manager.theme.base.surface,
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
        return ft.Stack(
            expand=True,
            controls=[
                self.main_container,
            ],
        )

    def _build_main_column(self):
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
        return ft.Container(
            expand=True,
            height=300,
            content=ft.Stack(
                expand=True,
                controls=[
                    self.timeline_view.control,
                    self._build_fab(),
                ],
            ),
        )

    def _build_fab(self):
        return FloatingNavButton.back(
            on_click=self._handle_voltar,
            key="detail_back",
        )

    # =========================================================
    # 🧩 SUBCOMPONENTES
    # =========================================================

    def _build_header(self):
        return SuperHeader(
            theme_manager=self.theme_manager,
            image_src=self.controller.image_src,
            nome=self.controller.nome,
            texto_inicial=self.controller.current,
            expand=True,
        )

    def _build_navigation(self):
        return NavigationControls(
            on_prev=self.prev,
            on_next=self.next,
        )

    # =========================================================
    # 🎮 INTERAÇÕES
    # =========================================================

    def next(self, e=None):
        if self.controller.next():
            self._refresh_slide()
            self.auto_close.reset()

    def prev(self, e=None):
        if self.controller.prev():
            self._refresh_slide()
            self.auto_close.reset()

    def _goto_slide(self, index: int):
        if self.controller.goto(index):
            self._refresh_slide()

    def _handle_voltar(self, e):
        self.auto_close.stop()
        self._on_request_close()

    def _timeout_close(self):
        self._on_request_close()

    # =========================================================
    # 🔄 ATUALIZAÇÃO
    # =========================================================

    def _refresh_slide(self):
        if not self._mounted:
            return

        self.header.update_text(self.controller.current)

    # =========================================================
    # 🎬 LIFECYCLE
    # =========================================================
    @override
    def did_mount(self):
        self._mounted = True

        self.apply_theme(self.theme_manager.theme)

        self._fade_in()
        self.timeline_view.refresh()
