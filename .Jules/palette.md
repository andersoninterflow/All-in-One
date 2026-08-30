## 2024-05-18 - Acessibilidade em botões de ação repetitivos em listas
**Learning:** Botões como "Abrir suporte" ou "Avaliar" dentro de listas de itens tornam-se ambíguos para usuários de leitores de tela quando não fornecem o contexto específico do item que estão acionando.
**Action:** Utilizar template literals para incorporar identificadores únicos/títulos (`aria-label={\`Abrir suporte para ${item.title}\`}`) aos atributos `aria-label` sempre que houver ações repetidas em elementos de lista.
