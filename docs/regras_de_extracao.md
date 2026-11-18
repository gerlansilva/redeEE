# Extração de arestas para a rede historiográfica da Educação Estatística (EE)
Entrada: fichas em /home/claude/work/fichas/<id>.md (resumos estruturados com páginas). Textos originais em /home/claude/work/txt/<id8>.txt só para conferir uma página duvidosa.
Saída (2 arquivos por lote, UTF-8, uma linha JSON por registro, sem comentários):
- /home/claude/work/rede/edges_<LOTE>.jsonl
- /home/claude/work/rede/nodes_<LOTE>.jsonl

## REGRA CENTRAL
Uma aresta existe SOMENTE se a ficha afirma a relação (ou o ano). NÃO infira, NÃO complete de memória, NÃO crie ligação por "provável". Se a ficha marca (incerto), registre confidence="incerta". Se duas fichas divergem, registre as duas e marque conflict=true.

## Aresta (campos)
{"source":"<nome canônico>","source_type":"pessoa|instituicao|periodico|evento|grupo|programa|marco|documento",
 "target":"<nome canônico>","target_type":"...",
 "relation":"um de: criou|fundou|presidiu|coordenou|orientou|formou_em|trabalhou_em|membro_de|organizou|realizou_em|publicou_em|editou|influenciou|trouxe_ao_brasil|originou|sucedeu|incorporou|financiou|ministrou_curso_em|colaborou_com|participou_de",
 "year":<int|null>,"year_end":<int|null>,
 "ctx_source":"<país/comunidade de source, ex.: Espanha, Brasil, Reino Unido/ISI, EUA, França, Austrália, Internacional>",
 "ctx_target":"<idem para target>",
 "evidence":"<paráfrase curta (<=25 palavras) do que a ficha afirma>",
 "doc":"<Autor ano do texto que afirma, ex.: Santos 2015>","ficha":"<id da ficha>","page":"<p. X como na ficha>",
 "confidence":"afirmada|incerta","conflict":false}

## Nó (campos)
{"id":"<nome canônico, igual ao usado nas arestas>","type":"pessoa|instituicao|periodico|evento|grupo|programa|marco|documento","ctx":"<país/comunidade>","city":"<cidade ou null>","year_start":<int|null>,"note":"<<=15 palavras, só o que as fichas dizem>"}

## Nomes canônicos (use exatamente; crie novos no mesmo padrão)
Pessoas: "Carmen Batanero", "Juan D. Godino", "Celi Espasandin Lopes", "Carlos Monteiro" (sem variações), etc. – nome completo mais usado, sem títulos.
Instituições: "Universidade de Granada", "UNICAMP", "PUC-SP", "UFPE", "UNESP Rio Claro", "ISI", "IASE", "SBEM", "GT-12/SBEM", "ABE", "IBGE"...
Eventos: "ICOTS-1 (Sheffield, 1982)", "CIEEE 1999 (Florianópolis)". Periódicos: "SERJ", "Journal of Statistics Education", "Teaching Statistics", "Bolema".
Evite duplicatas: reutilize o mesmo nome em todas as fichas do seu lote.

## O que extrair
Fundação/criação (instituição, evento, periódico, grupo, GT, programa), orientações e formação acadêmica (quem formou/orientou quem; onde fez doutorado/estágio), publicação/edição em periódicos, participação/organização de eventos, colaboração explícita, influência declarada ("X trouxe/introduziu/inspirou Y", "a abordagem de Granada chegou ao Brasil por..."), sucessão (um evento/órgão dá origem a outro). Cada aresta liga duas entidades; para "chegada ao Brasil" use relation="trouxe_ao_brasil" com ctx_source internacional e ctx_target "Brasil".
Marque ctx corretamente: é ele que permite desenhar o fluxo internacional→Brasil.

## Qualidade
- 1 afirmação = 1 aresta (sem duplicar a mesma afirmação; se vários textos afirmam o mesmo, uma linha por texto).
- Sempre doc+ficha+page. Sem página na ficha: page="s/p".
- Não copie citações literais >15 palavras; evidence é paráfrase.
- Ao terminar, valide: `python3 -I -c "import json;[json.loads(l) for l in open(ARQ)]"` nos dois arquivos, e responda só com: arquivos, nº de arestas, nº de nós, 3 observações sobre ambiguidades/conflitos.
