# 2026-09-03 — Only Nós / deploy

Ander pediu para publicar o projeto de casal (antigo Enlace, novo nome **Only Nós**) no Vercel e Hostinger, usando o domínio `onlynos.site`, após um erro de deploy na Vercel.

## Ações do GPT

- Consultou o repositório `AnderHonorato/enlace-app` como base unificada atual.
- Identificou incompatibilidade provável: o schema Prisma estava fixo em SQLite, apesar do ambiente de produção usar PostgreSQL/Supabase.
- Não armazenou nem comitou a credencial sensível fornecida na conversa.
- Criou a branch `fix/vercel-only-nos`.
- Adicionou `scripts/preparar-prisma-ambiente.mjs` para adaptar o provider do Prisma conforme `DATABASE_URL`, preservando SQLite local e usando PostgreSQL em produção.
- Ajustou `package.json`, `.env.example`, `vercel.json`, `src/nucleo/marca.ts` e `public/manifest.webmanifest`.
- Atualizou a marca central para **Only Nós**.
- Criou o PR #3 `fix: deploy Vercel + rebrand Only Nós` e fez squash merge na `main`.
- Commit resultante: `aeedfb62fcc3b98927773ab5defb4f996ca8bb53`.

## Pendências

- Confirmar no painel Vercel as variáveis `DATABASE_URL`, `APP_SECRET` e `NEXT_PUBLIC_APP_URL=https://onlynos.site`.
- Confirmar o domínio `onlynos.site` no projeto Vercel e configurar os registros DNS na Hostinger conforme os valores exibidos pela Vercel.
- Como uma senha de banco foi enviada em texto na conversa, recomendar rotação da senha no Supabase antes de produção.
