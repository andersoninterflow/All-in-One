# Guia de Configuração: Ubuntu (Termux) & Codex CLI à Distância

Este guia documenta o processo de ativação da sua Chave SSH segura (Ed25519) no ambiente **Ubuntu em execução no Termux**. Essa configuração permite acesso direto ao GitHub e ao seu Desktop (Windows), viabilizando o uso do **Codex CLI** pelo celular para evoluir o projeto All-in-One de forma remota.

---

## Passo 1: Receba a Chave Privada
Pelo seu desktop (Windows), copie todo o bloco de texto da **Chave Privada** que forneci anteriormente e envie para o seu próprio **Telegram** (na seção de Mensagens Salvas ou para um chat seguro). 

*A chave começa com `-----BEGIN OPENSSH PRIVATE KEY-----` e termina com `-----END OPENSSH PRIVATE KEY-----`.*

---

## Passo 2: Configure a Chave no Ubuntu (Termux)

1. No seu telefone, abra o Termux e inicie sua máquina virtual **Ubuntu**.
2. Garanta que o diretório oculto SSH existe e tenha a permissão certa:
   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ```
3. Crie o arquivo que vai guardar a sua chave privada:
   ```bash
   nano ~/.ssh/termux_mobile_key
   ```
4. Cole todo o bloco da chave privada (que você resgatou do Telegram) dentro desse arquivo.
5. Salve e saia do editor Nano (pressione `Ctrl+O`, dê `Enter`, e depois pressione `Ctrl+X`).
6. **OBRIGATÓRIO:** O SSH rejeitará a chave se as permissões dela estiverem públicas. Trave o arquivo apenas para leitura do seu usuário do Ubuntu:
   ```bash
   chmod 600 ~/.ssh/termux_mobile_key
   ```

---

## Passo 3: Automatize o Uso da Chave (Arquivo Config)

Para que o Git, o SSH e o Codex CLI achem sua chave automaticamente sem que você precise digitar o caminho toda vez, crie um arquivo de configuração do SSH:

1. Edite ou crie o arquivo `config`:
   ```bash
   nano ~/.ssh/config
   ```
2. Cole a configuração abaixo (substituindo `<IP_DO_SEU_DESKTOP>` pelo IP real do seu PC Windows na rede VPN ou local):
   ```text
   # Configuração para clonar/push do GitHub
   Host github.com
       HostName github.com
       User git
       IdentityFile ~/.ssh/termux_mobile_key
       IdentitiesOnly yes

   # Configuração para acesso SSH direto no Windows
   Host pc
       HostName <IP_DO_SEU_DESKTOP>
       User ereta
       IdentityFile ~/.ssh/termux_mobile_key
   ```
3. Salve e feche (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

## Passo 4: Evolua o Projeto à Distância

Agora você tem duas formas de usar o Codex CLI remotamente pelo celular:

### Opção A: Executar o Codex CLI dentro do Ubuntu (Local)
1. Clone o repositório diretamente no Ubuntu do celular (ele usará a chave automaticamente):
   ```bash
   git clone git@github.com:andersoninterflow/All-in-One.git
   cd All-in-One
   ```
2. Instale/inicie o Codex CLI localmente no Ubuntu do celular e programe de onde estiver. Toda vez que fizer _Push_, a sua chave o conectará ao GitHub de forma transparente.

### Opção B: Acessar seu Desktop Windows via SSH e rodar lá
1. Conecte-se remotamente no seu Windows (ele pedirá sua senha `@Aa3135930253` apenas para descriptografar a chave):
   ```bash
   ssh pc
   ```
2. Uma vez conectado pelo terminal no Windows, navegue para o repositório (`cd .codex/worktrees/all-in-one`) e acione o Codex CLI como se estivesse sentado na cadeira da sua casa.
