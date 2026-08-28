# Memórias IA — Infinity · Site

Este diretório contém o frontend estático publicado pelo GitHub Pages. Ele apresenta a arquitetura de memória individual, conversa entre IAs e conhecimento compartilhado descrita no repositório.

## Desenvolvimento local

Na pasta `Manus/Site`, instale as dependências com `pnpm install`, execute `pnpm run check` para validar os tipos e use `pnpm run build` para gerar o diretório `dist/`.

## Publicação

O workflow [`../../.github/workflows/deploy-pages.yml`](../../.github/workflows/deploy-pages.yml) publica automaticamente a branch `main` no GitHub Pages. O build usa o caminho-base `/Mem-rias-IA---Infinity/`, compatível com a URL de projeto do GitHub Pages.

O site é frontend-only e não deve receber tokens, credenciais ou dados privados. Os ativos visuais são versionados em `public/assets/` para que a página continue independente do ambiente Manus.
