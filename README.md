# Rede de relações da constituição da Educação Estatística

Rede historiográfica usada no capítulo da tese *Redes que contam histórias da constituição da área de pesquisa em Educação Estatística* (Gerlan Silva da Silva, UFSCar). Ela reúne as relações entre pessoas, instituições, eventos, grupos, periódicos e programas que as fontes consultadas afirmam, para ajudar a escrever e conferir o capítulo.

**Corpus (13/11/2026):** 438 nós, 772 arestas (716 afirmadas, 56 incertas), 50 documentos, 120 pontes exterior–Brasil.

## Como a rede foi construída

1. **Fichas.** Cada documento (handbooks, a tese de Santos 2015, a dissertação de Araújo 2017, textos de Batanero, editoriais dos números temáticos, relato de Ody 2019, Conti s.d., o site da conferência de Florianópolis recuperado na Wayback Machine e o Acervo CIEEE 1999) foi lido e resumido em ficha estruturada, com páginas.
2. **Regra central** (`docs/regras_de_extracao.md`). Uma aresta só existe se a ficha afirma a relação ou o ano. Nada é inferido nem completado de memória. Cada aresta guarda a paráfrase do que a fonte diz, o documento e a página (61 estão sem página, marcadas `s/p`). Dúvida da fonte vira `confidence = incerta`; divergência entre fontes vira `conflict = true`, com as duas versões registradas.
3. **Extração em lotes** (`dados/lotes/`), com vocabulário fechado de relações (criou, fundou, presidiu, organizou, orientou, influenciou, colaborou com, participou de, entre outras).
4. **Consolidação** (`scripts/consolidar.py`). Tabela de nomes canônicos e variantes; 12 arestas cuja identidade foi unificada por sobrenome ou iniciais ficam marcadas `unif_provavel`; remoção de SPAINFL e BND-BRAX (bandeiras do site); correção de INE para o Departamento de Informática e Estatística da UFSC; remoção de duplicatas exatas.
5. **Classe da aresta.** Pelo contexto de cada ponta: *ponte* (exatamente um lado Brasil, 120), *exterior–exterior* (336), *Brasil–Brasil* (316).
6. **Nós-síntese.** 51 nós não são atores nem eventos reais: documentos (por exemplo, "Tese Santos 2015"), conceitos (por exemplo, "Brasil", "Educação Estatística") e agregados (por exemplo, "Pesquisadores brasileiros de EE"). Ficam fora das figuras e da vista padrão da página interativa; 101 arestas (25 pontes) os tocam.
7. **Layout.** As posições vêm do algoritmo de layout do programa [Redes](https://github.com/gerlansilva/redes) (`redes.viz.similitude`): agrupamento de Louvain em blocos, layout de molas dentro de cada bloco, separação das caixas de círculo e rótulo, e blocos afastados entre si. Por isso nada se sobrepõe. **A posição e as manchas de bloco não têm significado histórico.**

## Conteúdo

| Pasta | O quê |
|---|---|
| `dados/rede.json` | Nós e arestas consolidados (fonte única da verdade) |
| `dados/lotes/` | Saída bruta da extração, por lote |
| `dados/arestas_para_conferencia.csv` | Todas as arestas, para conferir contra os PDFs |
| `scripts/` | `consolidar.py`, `gerar_dados_pagina.py` e `build_layouts.py` (dados e posições da página), `figura_estatica.py` (figura do capítulo) |
| `index.html`, `rede_data.json`, `layouts.json` | Página interativa (na raiz, para o Cloudflare Pages servir `https://redeee.pages.dev/`) |
| `figuras/` | Figura estática para o capítulo |
| `docs/` | Regras de extração e números da rede |

## Reproduzir

```bash
pip install networkx numpy git+https://github.com/gerlansilva/redes
# 1) consolidar os lotes (lê edges_*/nodes_* do diretório atual e grava rede.json e arestas_para_conferencia.csv)
(cd dados/lotes && python3 ../../scripts/consolidar.py && mv rede.json arestas_para_conferencia.csv ..)
# 2) figura estática 
python3 scripts/figura_estatica.py 3 figuras/rede_figura.svg dados/rede.json
# 3) página interativa
python3 scripts/gerar_dados_pagina.py dados/rede.json rede_data.json
python3 scripts/build_layouts.py   # grava layouts.json (~40 s) na raiz
```

Para abrir a página localmente: `python3 -m http.server` na raiz do repositório e acessar `http://localhost:8000`.

## Limites (leia antes de citar)

- **A rede mede o corpus, não a área.** Cerca de 22% das arestas (47,6% das exterior–exterior) vêm de textos de Batanero; o acervo do CIEEE 1999 lista cada apoio e cada membro da comissão, o que infla Florianópolis.
- A direção da aresta segue o verbo, não indica influência; quantidade de arestas não mede importância.
- 204 arestas não têm ano; o internacional posterior a 2010 quase não está nas fichas.
- Nomes por sobrenome ou iniciais são identificações prováveis.
