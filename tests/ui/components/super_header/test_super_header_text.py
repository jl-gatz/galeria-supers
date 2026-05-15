from galeria.ui.components.super_header import SuperHeader


def test_update_text_applies_theme_to_new_paragraphs(super_header, super_header_theme):
    super_header.did_mount()

    super_header.update_text("Novo texto.\n\nOutro bloco.")

    assert len(super_header.text_list.controls) == 2

    for paragraph in super_header.text_list.controls:
        assert paragraph.color == super_header_theme.text.secondary
        assert paragraph.size == super_header_theme.typography.super_header_body_size
        assert (
            paragraph.font_family
            == super_header_theme.typography.super_header_body_font_family
        )
        assert paragraph.style.height == super_header_theme.typography.super_header_body_line_height


def test_super_header_disables_mask_for_placeholder(super_header_manager):
    header = SuperHeader(
        theme_manager=super_header_manager,
        image_src=None,
        nome="Ada",
        texto_inicial="Texto",
    )

    assert header.portrait_image.apply_mask is False
    assert header.portrait_image.mask_image.visible is False
