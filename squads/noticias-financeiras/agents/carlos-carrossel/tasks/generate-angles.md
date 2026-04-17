---
task: "Generate Angles"
order: 1
input: |
  - selected_news: Notícia escolhida pelo usuário (do news-list.md, via checkpoint)
  - tone_of_voice: Guia de tons disponíveis (tone-of-voice.md)
output: |
  - angles: 5 ângulos distintos para a notícia, cada um com hook de exemplo e tom sugerido
---

# Generate Angles

Gera 5 ângulos editoriais genuinamente distintos para a mesma notícia financeira. Cada ângulo é uma perspectiva emocional diferente que produziria um carrossel completamente diferente.

## Process

1. **Lê a notícia selecionada** do output do checkpoint anterior. Extrai: o fato central, o dado-chave, o contexto e o impacto no Brasil.

2. **Lê o `tone-of-voice.md`** para entender os 6 tons disponíveis da 9Pilla antes de gerar os ângulos.

3. **Gera 5 ângulos** usando estruturas emocionais distintas — nenhum ângulo pode ser variação de outro. Use os 5 frameworks abaixo como ponto de partida:

   - **Medo/Urgência**: o que o leitor está perdendo AGORA por não agir
   - **Oportunidade/Janela**: o que quem sabe pode ganhar neste momento
   - **Educativo/Revelação**: "você sabia que..." — explica mecanismo que poucos conhecem
   - **Contrário/Mito**: desmonta uma crença comum sobre o tema da notícia
   - **Inspiracional/Transformação**: o que muda na vida de quem entende e age

4. **Para cada ângulo, escreve**:
   - Nome do ângulo (ex: "Medo — o custo do silêncio")
   - Tom sugerido (do tone-of-voice.md)
   - Hook de exemplo (primeira linha do slide 1)
   - Promessa implícita (o que o leitor vai aprender/ganhar)
   - Perfil do slide final (como fecharia o carrossel com esse ângulo)

5. **Apresenta os 5 ângulos** numerados e pede ao usuário para escolher um.

## Output Format

```markdown
# 5 Ângulos para: [Título da Notícia]

Notícia: [resumo em 1 linha]
Dado-chave: [o número ou fato central]

---

## Ângulo 1 — [Nome do Ângulo]
**Tom:** [nome do tom do tone-of-voice.md]
**Hook:** "[primeira linha do slide 1]"
**Promessa:** [o que o leitor vai aprender/ganhar com este ângulo]
**Fechamento:** [como terminaria — CTA, reflexão, solução]

---

## Ângulo 2 — [Nome do Ângulo]
[mesmo formato]

---

[... até Ângulo 5]

---

Qual ângulo você quer desenvolver?
```

## Output Example

> Referência de qualidade.

```markdown
# 5 Ângulos para: IPCA-15 de março sobe 0,44%, acima das expectativas

Notícia: Inflação medida pelo IPCA-15 veio em +0,44% em março de 2026, acima da expectativa de +0,38%, acumulando 3,90% em 12 meses.
Dado-chave: +0,44% em março; passagem aérea +5,94%; poupança rende ~6,17% a.a.

---

## Ângulo 1 — Problema Invisível
**Tom:** Educativo-Próximo
**Hook:** "Você sabia que o seu dinheiro está perdendo valor todos os meses — mesmo sem você gastar mais?"
**Promessa:** O leitor vai entender o que é inflação real e descobrir que a poupança não protege
**Fechamento:** 3 investimentos simples que qualquer pessoa pode fazer hoje + CTA para a turma 9Pilla

---

## Ângulo 2 — Urgência / Janela de Oportunidade
**Tom:** Urgente-Direto
**Hook:** "A inflação de março veio ACIMA do esperado. Isso muda tudo para quem ainda está na poupança."
**Promessa:** Por que este momento específico é crítico para sair da poupança e o que fazer agora
**Fechamento:** Comparativo de rentabilidade: poupança vs CDB vs Tesouro IPCA+ + CTA de engajamento

---

## Ângulo 3 — Contrário / Mito
**Tom:** Analítico-Desafiador
**Hook:** "A poupança é isenta de IR. Isso não quer dizer que ela é um bom investimento."
**Promessa:** Desmonta o mito de que isenção de IR = melhor retorno líquido
**Fechamento:** Cálculo comparativo real + "→ quem entende isenção / → quem confunde isenção com rentabilidade"

---

## Ângulo 4 — Contexto Global / Revelação
**Tom:** Analítico-Informativo
**Hook:** "A guerra no Oriente Médio chegou na sua cozinha. Veja o caminho."
**Promessa:** Explica o mecanismo completo: conflito → petróleo → frete → alimentos → IPCA
**Fechamento:** Por que entender as causas muda a forma de se proteger

---

## Ângulo 5 — Inspiracional / Transformação
**Tom:** Motivacional-Próximo
**Hook:** "Há 5 anos atrás eu não entendia o que era IPCA. Hoje eu sei exatamente como me proteger."
**Promessa:** Jornada de transformação: de quem não entende inflação para quem antecipa e se protege
**Fechamento:** "O problema nunca foi o dinheiro. Foi o acesso à informação." + CTA turma 9Pilla

---

Qual ângulo você quer desenvolver?
```

## Quality Criteria

- [ ] Exatamente 5 ângulos gerados
- [ ] Cada ângulo usa um tom diferente ou estrutura emocional genuinamente distinta
- [ ] Nenhum ângulo é variação de outro (sem "Ângulo 1 educativo" e "Ângulo 2 também educativo mas com outro exemplo")
- [ ] Cada ângulo tem hook completo (primeira linha do slide 1 escrita, não descrita)
- [ ] Output encerra com pergunta de escolha para o usuário

## Veto Conditions

Rejeita e refaz se QUALQUER uma for verdadeira:
1. Menos de 5 ângulos entregues
2. Dois ou mais ângulos com o mesmo tom E estrutura emocional (duplicatas)
