# Guia seguro: Ubuntu no Termux e Codex CLI remoto

Este guia mantém Codex CLI, Antigravity e os demais agentes alinhados pelo Git,
sem transportar senhas ou chaves privadas por mensageiros.

## 1. Use uma chave exclusiva no telefone

No Ubuntu do Termux, gere uma chave própria para esse dispositivo:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/all_in_one_termux -C "all-in-one-termux"
```

Nunca copie a chave privada do desktop. Cadastre somente o conteúdo de
`~/.ssh/all_in_one_termux.pub` no GitHub, com o menor escopo necessário.

## 2. Configure o SSH

Crie `~/.ssh/config`:

```text
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/all_in_one_termux
    IdentitiesOnly yes

Host all-in-one-desktop
    HostName <HOST_VPN_OU_REDE_PRIVADA>
    User <USUARIO_WINDOWS>
    IdentityFile ~/.ssh/all_in_one_termux
    IdentitiesOnly yes
```

Proteja os arquivos:

```bash
chmod 600 ~/.ssh/config ~/.ssh/all_in_one_termux
chmod 644 ~/.ssh/all_in_one_termux.pub
```

O acesso ao desktop deve usar uma VPN privada ou rede confiável, autenticação
por chave e firewall restrito. Senhas nunca devem aparecer neste repositório.

## 3. Clone e alinhe antes de trabalhar

```bash
git clone git@github.com:andersoninterflow/All-in-One.git
cd All-in-One
git fetch origin main
git status --short --branch
```

Antes de editar, confirme que `main` contém o estado remoto esperado. Se houver
divergência ou mudanças locais, integre-as sem `reset --hard`, `clean` destrutivo
ou force-push.

## 4. Respeite os contratos do workspace

- Leia `AGENTS.md`, `GEMINI.md` e
  `config/autonomy/multi_agent_sync_policy.json`.
- Use Git como fonte compartilhada de verdade.
- Não sobrescreva alterações locais ou commits de outro agente.
- Mantenha Gemini CLI e integrações Google desativados enquanto
  `config/autonomy/google_integrations_policy.json` estiver com
  `enabled=false`.
- Nunca versione tokens, senhas, chaves privadas ou arquivos `.env` reais.

## 5. Valide e sincronize

```bash
python3 scripts/validate_repository.py
git status --short
```

No Windows, o fechamento obrigatório usa:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/git_auto_sync.ps1 -Activity "<descricao>"
```

No Ubuntu/Termux, faça commit intencional e push somente depois de buscar e
integrar o estado remoto mais recente.
