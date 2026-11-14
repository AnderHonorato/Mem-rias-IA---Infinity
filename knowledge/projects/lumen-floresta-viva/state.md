# Estado atual — 2026-11-14

- Estado: em desenvolvimento; site funcional no Preview do projeto Manus WebDev.
- Projeto WebDev: `wdp_3e8cb0f1d1918813c9a5eb4c`.
- Commit enviado para `origin/main`: `6efbbdbd50cbcf4fe9e30f18a2f63468a3aeda3c`.
- Build: `pnpm install --frozen-lockfile` e `pnpm build` concluíram com sucesso; `dist/` gerado.
- Preview local: `/` respondeu HTTP 200; `/manus-routes.json` retornou JSON válido para `/`; `/floresta-lumen.png` respondeu HTTP 200.
- Interações observadas em navegador: som foi alternado e deixado desligado; movimento reduzido foi testado; o fragmento “@ Creative Claw” atualizou o texto selecionado. Console do navegador sem saída de erro na inspeção.
- Responsividade desktop/mobile foi inspecionada durante a implementação; o último ajuste de parallax altera apenas o deslocamento sutil do plano de arte e respeita o fator de movimento reduzido.
- Publicação: não realizada. `publishing.auto_publish` estava `false` na configuração confirmada.
- Limite de confirmação: o push para `origin/main` foi aceito, mas não apareceu um recibo de versão nem entrada de Version History visível nesta sessão; não afirmar publicação ou checkpoint confirmado além do commit remoto.
