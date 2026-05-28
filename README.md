# Galeria dos Supers

A **Galeria dos Supers** é uma aplicação em **Flet/Python** para apresentar, de forma visual e navegável, a trajetória dos superintendentes ligados à história da informática institucional da Unicamp.

O projeto combina galeria visual, navegação por perfis, temas por período histórico e uma linha do tempo interativa. A proposta é construir uma experiência de consulta com aparência museológica, preservando a memória institucional em uma interface elegante, responsiva e expansível.



## Status do projeto

O projeto está em fase de consolidação da primeira versão funcional.

### Estado atual

- Galeria principal funcional.
- Tela de detalhe dos superintendentes funcional.
- Sistema de temas aplicado à galeria e à tela de detalhe.
- Aplicação automática de temas por era já implementada na Galeria e na tela de detalhe.
- Linha do tempo funcional, com pontos clicáveis e exibição simples dos anos junto aos pontos.
- Estrutura de testes em expansão.
- Organização inicial em camadas: domínio, infraestrutura, interface, tema e dados.
- Preparação para uma primeira release `v0.1.0`.

### Próximos passos previstos

- Documentação e limpeza geral dos arquivos.
- Revisão da estrutura de dados.
- Refinamento visual da linha do tempo.
- Refinamento da aplicação de temas por era.
- Melhor organização da transição visual entre eras.
- Possível deploy demonstrativo em branch separada.

---

## Como rodar localmente

O projeto utiliza **Poetry** para gerenciamento de dependências e ambiente.

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Instalar dependências

```bash
poetry install
```

### 3. Ativar o ambiente do Poetry

Se a sua instalação do Poetry tiver suporte a `poetry shell`:

```bash
poetry shell
```

Caso `poetry shell` não esteja disponível, use:

```bash
poetry env activate
```

Também é possível executar os comandos diretamente com `poetry run`, sem ativar o shell.

### 4. Executar a aplicação

Com o ambiente ativado:

```bash
python -m galeria.main
```

Ou diretamente via Poetry:

```bash
poetry run python -m galeria.main
```

Há também tasks do taskipy disponíveis no pyproject.toml:

```bash
task runb
```
---
## Como rodar os testes

O projeto usa `pytest`.

Para rodar todos os testes:

```bash
pytest
```

Também é possível rodar os testes via taskipy (já com relatório de cobertura):

```bash
task test
```

Para rodar com relatório de cobertura:

```bash
pytest --cov=galeria
```

Para rodar um subconjunto específico:

```bash
pytest tests/unit
pytest tests/ui
pytest tests/integration
```

Para rodar um teste específico:

```bash
pytest tests/ui/gallery_view/test_gallery_tree_snapshot.py
```

---

## Estrutura geral do projeto

A estrutura principal do pacote `galeria` está organizada em camadas e módulos especializados:

```text
galeria/
├── application/
├── assets/
├── core/
├── data/
├── debug/
├── domain/
├── infrastructure/
├── ui/
└── main.py
```

### `application/`

Camada reservada para coordenação de casos de uso e fluxos de aplicação.

Atualmente, a maior parte da lógica ainda está distribuída entre controladores, serviços e componentes de interface.

### `assets/`

Contém recursos estáticos da aplicação.

```text
assets/
├── fonts/
└── images/
```

Aqui ficam fontes, logotipos, imagens dos superintendentes e demais recursos visuais.

### `core/`

Configurações centrais do projeto.

Exemplos:

```text
core/
├── config.py
└── paths.py
```

Esse módulo deve concentrar caminhos, constantes globais e configurações compartilhadas.

### `data/`

Contém os dados usados pela aplicação.

Atualmente, o principal arquivo é:

```text
data/supers.json
```

Esse arquivo concentra os dados dos superintendentes exibidos na galeria, incluindo informações textuais, imagens e dados associados à linha do tempo.

### `domain/`

Camada de domínio da aplicação.

```text
domain/
├── models.py
├── services.py
├── super_repository.py
└── protocols/
```

Aqui ficam modelos, serviços e contratos que representam as entidades centrais do projeto.

### `infrastructure/`

Camada de infraestrutura.

```text
infrastructure/
└── repositories/
```

Responsável por implementações concretas de acesso a dados e repositórios.

### `ui/`

Camada de interface.

```text
ui/
├── behaviors/
├── components/
├── config/
├── controllers/
├── layout/
├── navigation/
├── theme/
├── utils/
└── views/
```

Essa é a camada mais ativa do projeto no momento. Ela contém componentes visuais, telas, controladores, navegação, tema e utilitários de interface.

---

## Dados

Os dados principais ficam em:

```text
galeria/data/supers.json
```

Esse arquivo descreve os superintendentes exibidos na aplicação.

Cada registro pode incluir informações como:

- nome;
- imagem;
- textos históricos;
- dados da linha do tempo;
- metadados relacionados à era ou ao período institucional.

Exemplo conceitual:

```json
{
  "id": 1,
  "nome": "Nome do Superintendente",
  "foto": "imagem.png",
  "timeline_points": [
    {
      "year": 1967,
      "label": "Ingresso",
      "x": 0.08,
      "y": 0.96
    }
  ],
  "historias": [
    "Texto histórico associado ao superintendente."
  ]
}
```

A estrutura de dados ainda deve evoluir para representar melhor as eras institucionais, como CCUEC, DETIC e possíveis períodos futuros.

---

## Imagens

As imagens ficam em:

```text
galeria/assets/images/
```

### Superintendentes

```text
galeria/assets/images/supers/
```

Contém as imagens usadas nos cards da galeria e na tela de detalhe.

### Logotipos

```text
galeria/assets/images/logos/
```

Contém logotipos usados pela interface.

A estrutura de logotipos pode ser organizada por tema ou era, permitindo variações visuais conforme o período institucional exibido.

---

## Fontes

As fontes ficam em:

```text
galeria/assets/fonts/
```

O projeto utiliza famílias tipográficas incluídas diretamente nos assets, como:

- Lora;
- Manrope;
- Montserrat;
- Source Sans 3.

Essas fontes dão suporte ao estilo visual institucional e museológico da aplicação.

---

## Temas

O sistema de temas fica em:

```text
galeria/ui/theme/
```

Principais arquivos:

```text
theme/
├── manager.py
├── models.py
├── spacing.py
├── styles.py
├── theme.py
├── themes.py
└── typography.py
```

O tema centraliza decisões visuais como:

- cores;
- tipografia;
- espaçamentos;
- estilos de texto;
- dimensões de componentes;
- raios de borda;
- aparência da galeria;
- aparência da tela de detalhe.

A aplicação já possui componentes que respondem ao tema, incluindo galeria, tela de detalhe, placeholders, botões de navegação, FAB e timeline.

---

## Componentes principais

Os principais componentes de interface ficam em:

```text
galeria/ui/components/
```

Exemplos:

```text
components/
├── floating_nav_button.py
├── gallery_row.py
├── logos_row.py
├── navigation_controls.py
├── placeholders_row.py
├── responsive_timeline.py
├── super_header.py
└── timeline/
```

### Galeria

A galeria é responsável pela apresentação visual dos superintendentes em sequência navegável.

Arquivos relacionados:

```text
ui/views/gallery_view.py
ui/components/gallery_row.py
ui/controllers/gallery_controller.py
ui/controllers/gallery_scroll_controller.py
```

### Tela de detalhe

A tela de detalhe apresenta um superintendente específico, combinando imagem, textos, navegação e linha do tempo.

Arquivos relacionados:

```text
ui/views/super_view.py
ui/components/super_header.py
ui/controllers/super_detail_controller.py
```

### Linha do tempo

A linha do tempo possui estrutura própria:

```text
ui/components/timeline/
├── controller/
├── models/
├── utils/
└── view/
```

Principais responsabilidades:

- modelar pontos da linha do tempo;
- mapear dados para coordenadas visuais;
- renderizar caminho e pontos;
- controlar progresso e estado ativo;
- responder a eventos de interação.

---

## Testes

A estrutura de testes fica em:

```text
tests/
```

Ela inclui:

```text
tests/
├── behavior/
├── debug/
├── factories/
├── fixtures/
├── harness/
├── integration/
├── snapshots/
├── stubs/
├── ui/
├── unit/
└── utils/
```

### Organização dos testes

- `unit/`: testes unitários de serviços, domínio e lógica isolada.
- `ui/`: testes de componentes e views.
- `integration/`: testes de fluxos maiores.
- `fixtures/`: dados reutilizáveis para testes.
- `factories/`: fábricas de objetos para testes.
- `stubs/`: implementações falsas para isolar dependências.
- `harness/`: utilitários para inspecionar e testar árvores Flet.
- `snapshots/`: snapshots estruturais da interface.
- `debug/`: ferramentas auxiliares para depuração dos testes.

---

## Convenções do projeto

### Organização

O projeto busca separar responsabilidades entre:

- domínio;
- infraestrutura;
- interface;
- tema;
- dados;
- assets.

### Estilo

A interface segue uma linha visual inspirada em museologia contemporânea, com foco em:

- fundos escuros ou neutros;
- destaque visual para retratos;
- uso controlado de cor;
- tipografia institucional;
- sensação de galeria histórica digital.

### Dados antes de lógica

Sempre que possível, decisões como era, período, imagens e textos devem vir dos dados, evitando regras visuais rígidas espalhadas nos componentes.

---

## Checklist antes de abrir PR

Antes de abrir um Pull Request, rode localmente:

```bash
poetry run pytest
poetry run task lint
poetry run task typecheck
git status --short
```

---

## Release atual

A primeira release planejada é:

```text
v0.1.0 - Galeria mínima funcional
```

Escopo sugerido da release:

- galeria navegável;
- tela de detalhe funcional;
- temas aplicados;
- linha do tempo mínima funcional;
- testes principais em funcionamento;
- documentação básica;
- estrutura de dados inicial.

Essa versão marca o primeiro estado estável do projeto, antes da evolução para transições de era mais sofisticadas, refinamento da timeline e deploy demonstrativo.

---

## Roadmap próximo

### v0.1.0

- Consolidar documentação.
- Limpar arquivos experimentais ou obsoletos.
- Revisar estrutura de testes.
- Registrar primeira release.

### v0.2.0

- Refinar linha do tempo.
- Melhorar estados visuais dos pontos.
- Melhorar transições visuais.

### v0.3.0

- Estruturar eras em dados próprios.
- Aplicar temas automaticamente por era.
- Melhorar transições entre CCUEC, DETIC e períodos futuros.

### Futuro

- Deploy demonstrativo.
- Página pública.
- Expansão de dados históricos.
- Melhorias de acessibilidade.
- Possível painel editorial para manutenção dos dados.

## Créditos

Projeto desenvolvido como iniciativa de preservação e apresentação visual da história institucional da informática na Unicamp.

A completar com créditos de pesquisa, desenvolvimento, imagens, fontes e acervo.