# Deploy de apresentação no Render

Este projeto possui uma branch específica para apresentação pública no Render:

```text
presentation/web-demo
```

Essa branch existe apenas para demonstração do app em ambiente web hospedado.

## Regra importante

A branch `presentation/web-demo` não deve ser mergeada em `main` nem em `dev`.

O fluxo correto é:

```text
main/dev -> presentation/web-demo
```

E não:

```text
presentation/web-demo -> main/dev
```

Ou seja: a branch de apresentação pode receber atualizações da base principal, mas
alterações específicas de deploy/demo não devem voltar automaticamente para as
branches canônicas do projeto.

## Motivo

A branch de apresentação pode conter adaptações específicas para hospedagem web,
Render, Flet server, variáveis de ambiente e comportamento de demonstração.

Essas adaptações não representam necessariamente o modo final de produção/quiosque
do projeto.

## Atualização da branch de apresentação

Para atualizar a apresentação com mudanças recentes da base principal:

```bash
git checkout presentation/web-demo
git merge dev
```

Ou, se a base escolhida for `main`:

```bash
git checkout presentation/web-demo
git merge main
```

Depois disso, publicar normalmente a branch no GitHub para que o Render faça o
novo deploy.

## Proteção de branch

O workflow `Block presentation branch merges` bloqueia Pull Requests de branches
com prefixos `presentation/`, `demo-only/` ou `no-merge/` para `main` ou `dev`.

Esse bloqueio só é efetivo se o workflow estiver presente nas branches protegidas
`main` e/ou `dev`, e se o check for marcado como obrigatório nas regras de
proteção de branch do GitHub.
