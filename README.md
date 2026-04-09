# Galeria dos Supers

Aplicação para visualização de uma galeria de superintendentes (ou entidades similares) em formato de cards interativos, com suporte a ações rápidas via Floating Action Button (FAB) e elementos institucionais como logos.

---

## ✨ Objetivo

Fornecer uma estrutura simples, testável e componentizada para renderizar uma galeria visual com:

* Cards dinâmicos
* Ações rápidas (FAB)
* Organização clara de layout
* Suporte a testes com snapshot de árvore de componentes

---

## 🧱 Estrutura Geral

A árvore principal da interface segue o padrão:

```
Gallery
├── Title
├── Cards
│   ├── Card(...)
│   ├── Card(...)
│   └── ...
├── FAB
└── Logos
```

### Componentes principais

* **Gallery**: container principal
* **Title**: título da galeria
* **GalleryRow / Cards**: responsável por organizar os cards
* **Card**: unidade visual de cada item
* **FloatingActionButton (FAB)**: ações rápidas
* **Logos**: elementos institucionais

---

## ⚙️ Tecnologias

* Python
* Flet (UI)
* Pytest (testes)

---

## 🧪 Testes

O projeto utiliza testes baseados em snapshot da árvore de componentes.

### Estratégia

* Renderização controlada da view
* Extração da árvore via utilitários
* Comparação com snapshots esperados

### Observações

* Uso de `fake_page` ou `ft.Page()` dependendo do contexto
* Necessidade de sincronização adequada (`await page.update()` quando aplicável)

---

## 🧩 Decisões de Design

* **Componentização forte**: cada parte da UI é isolada
* **Separação de responsabilidades**: layout, dados e interação desacoplados
* **Testabilidade como prioridade**: estrutura pensada para facilitar snapshots

---

## 🚧 Pontos em evolução

* Tipagem mais rígida dos componentes (ex: `GalleryRow`)
* Refinamento da identificação de elementos no serializer (evitar falsos positivos como logos sendo tratados como cards)
* Melhor organização de props e metadados (ex: `super_data`)

---

## ▶️ Como rodar

```bash
# clonar repositório
git clone https://github.com/jl-gatz/galeria-supers.git
cd galeria-supers

# ambiente e dependências
poetry shell
poetry install
```

Após a instalação, verifique as tasks disponíveis no `pyproject.toml` (via Taskipy):

```bash
poetry run task --list
```

### Atalhos comuns

````bash
# rodar aplicação
poetry run task run

# rodar testes
poetry run task test

# atualizar snapshots
poetry run task snap
```` 
---

## 🤝 Contribuição

1. Crie uma branch a partir da main
2. Faça commits pequenos e organizados
3. Garanta que os testes passam
4. Abra um Pull Request com contexto claro

---

## 📝 Convenções

* Commits separados por tipo de mudança (refatoração, feature, teste)
* Evitar mudanças não relacionadas no mesmo PR
* Manter consistência nos snapshots

---

## 📌 Observações finais

Este projeto prioriza clareza estrutural e previsibilidade de comportamento da UI, sendo especialmente útil como base para experimentação com componentização em Flet e testes estruturais.
