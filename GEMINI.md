# Regras do Agente de Desenvolvimento (Perfil Codex)

## Preferência Obrigatória de Idioma
- Todas as respostas, alertas, erros, orientações, perguntas e opções devem ser escritos em português do Brasil.
- Essa regra vale para este workspace (ll-in-one) e deve prevalecer sobre respostas em inglês.
- Códigos, nomes de arquivos, comandos, identificadores, logs e mensagens externas devem permanecer no idioma/formato original para precisão técnica.

## Sincronização Git Obrigatória
- Ao concluir cada atividade que altere arquivos neste workspace, é mandatório executar a sincronização Git automática.
- O script padrão para isso é:
  ``powershell
  powershell -NoProfile -ExecutionPolicy Bypass -File scripts/git_auto_sync.ps1 -Activity "<descricao curta da atividade>"
  ``
- O push automático utiliza o remoto ork (conforme política em config/autonomy/git_auto_sync_policy.json).
- Nunca criar commits vazios.
- Se a branch estiver bloqueada por merge/rebase, o agente deve parar a execução e notificar o usuário imediatamente (em PT-BR).

## Sincronização Marketplace Valley
- Para atividades que alterem produtos, serviços ou catálogos, aplicar as regras do documento docs/ORIENTACAO_CODEX_SYNC_MARKETPLACE_VALLEY.md.
