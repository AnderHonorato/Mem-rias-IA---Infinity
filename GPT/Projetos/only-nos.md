# Only Nós

Antigo projeto **Enlace**, atualmente renomeado por Ander para **Only Nós**.

- Repositório principal atual: `AnderHonorato/enlace-app`
- Domínio desejado: `onlynos.site`
- Hospedagem principal pretendida: Vercel, com domínio/DNS gerenciado pela Hostinger.
- Banco de produção: PostgreSQL/Supabase.

## Deploy de 2026-09-03

Foi corrigida a preparação do Prisma para permitir SQLite local e PostgreSQL em produção. A marca central e o manifest PWA foram atualizados para Only Nós. O PR #3 foi integrado na `main`, resultando no commit `aeedfb62fcc3b98927773ab5defb4f996ca8bb53`.

Pendências externas: confirmar variáveis de ambiente na Vercel, associar `onlynos.site` ao projeto e aplicar na Hostinger os registros DNS indicados pela Vercel. Credenciais sensíveis não devem ser armazenadas neste repositório.
