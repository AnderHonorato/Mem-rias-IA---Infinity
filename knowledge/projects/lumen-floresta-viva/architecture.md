# Arquitetura

- Aplicação estática de uma página, Vite 7.3.8 + JavaScript, `three` 0.180; sem backend, banco ou autenticação.
- `index.html`: estrutura semântica, seções narrativas, controles e referências de conteúdo.
- `src/main.js`: renderização Three.js, câmera/parallax, partículas, portal animado, interação por cursor/toque, shader de água, som opcional e controles de movimento/intensidade.
- `src/style.css`: direção visual, tipografia, camadas, transições, acessibilidade e breakpoints responsivos.
- `public/floresta-lumen.png`: arte panorâmica local da cena; a imagem fornecida serviu de referência visual.
- `public/manus-routes.json`: manifesto da rota `/`.
- Build publicado declarado no WebDev: `pnpm install --frozen-lockfile && pnpm build`, saída `dist`.
