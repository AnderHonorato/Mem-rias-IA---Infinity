# Lumina Notes — evolução Android v2

**Atualizado em:** 2026-09-03

## Repositório
- Projeto: `AnderHonorato/lumina`
- Branch de evolução: `feat/lumina-mobile-android-v2`
- Backup anterior: `backup/lumina-before-mobile-20260902`
- Base original preservada: `2c9195fcccd0582f3e36e9ae5f5151995edebc95`

## Decisões e implementação
- Preservar o aplicativo Electron/desktop existente e adicionar Android via Capacitor, sem reescrever o projeto do zero.
- Android usa `@capacitor-community/sqlite`, notificações locais, Filesystem, Share, Geolocation, Preferences e armazenamento seguro.
- Corrigido travamento infinito em “Preparando seu espaço”: a causa era um deadlock no bootstrap SQLite, em que uma operação de banco aguardava a própria Promise de inicialização.
- Criado `src/renderer/js/mobile-platform-v2.js`, que usa operações SQLite diretas durante o bootstrap e só libera a API móvel após concluir a inicialização.
- Adicionada tela de diagnóstico de boot com barra de progresso, porcentagem, etapa atual, detalhes técnicos, campo de erro, copiar erro e tentar novamente.
- Interface móvel passa a ser carregada somente após o evento `lumina:mobile-ready`.

## Testes Android
- Workflow: `.github/workflows/android-build.yml`.
- Smoke test real: `scripts/android-smoke.sh`.
- O teste instala o APK em emulador Android API 35, inicia `com.lumina.notes/.MainActivity`, verifica processo ativo, ausência de falha nativa e exige o marcador `[Lumina] Android v2.1 pronto`.
- Run validado: `33710962559`, retry do job Android `100510449711`.
- Resultado do smoke test: sucesso.
- Evidência registrada no CI: `Bootstrap Android confirmado: 100% e processo ativo (2190)` e `[Lumina] Android v2.1 pronto`.
- APK testado: 17.906.250 bytes.
- SHA-256: `1838d9dd6b99c1cdf7c5bdd334ec377ea292744e47f77a9a85ae9ff1bfebfc37`.
- Artifact GitHub Actions: `Lumina-Notes-apk`, ID `9876978937`.

## Observações
- Erros anteriores no smoke test eram de infraestrutura/script do GitHub Actions (`/bin/sh` sem `pipefail`, loop multiline dividido pela action e falta de permissão KVM), não falhas comprovadas do APK. Foram corrigidos com script Bash único e KVM habilitado.
- Houve também um timeout transitório ao baixar Gradle; o retry posterior concluiu com sucesso.
- O build Windows ainda possui uma regressão independente a ser tratada separadamente; não bloqueia o APK Android validado.
