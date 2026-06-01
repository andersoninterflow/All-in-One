# Identidade Visual All-in-One E Valley

## Regra Mandatoria

Toda tela, app, mockup, documento visual e entrega gerada no Stitch deve usar a
marca All-in-One como marca guarda-chuva. Apps Valley tambem devem exibir a logo
Valley de forma consistente.

## Ativos Canonicos

- All-in-One oficial: `assets/brand/all-in-one-logo-official.png`
- All-in-One claro: `assets/brand/all-in-one-logo-light-official.png`
- Valley oficial: `assets/brand/valley-logo-official.png`
- Contrato versionado: `config/branding/brand_identity.json`

## Aplicacao No Stitch

O `scripts/stitch_orchestrator.py` injeta o contrato de marca nos prompts. Toda
tela deve posicionar a marca All-in-One no shell/header global. Quando a tela
atender `valley`, `valley-business` ou `valley-rider`, o prompt tambem exige a
logo Valley padronizada, sem distorcer, recolorir, cortar ou recriar o ativo.

## Regras De Uso

- Preservar area de respiro minima de 16 px.
- Usar largura minima de 120 px para All-in-One e 104 px para Valley.
- Manter texto alternativo `All-in-One` e `Valley`.
- Nao colocar dados sensiveis, documentos, biometria, chaves ou tokens em
  exemplos de marca.
