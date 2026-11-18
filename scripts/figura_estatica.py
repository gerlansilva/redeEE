"""Figura estática da rede para o capítulo, com o motor de figuras do Redes (redes.viz.similitude).
Só entram entidades reais (pessoas, instituições, eventos, grupos, periódicos, programas); os 51
nós-síntese (documentos, conceitos e agregados) ficam de fora. Uso: python3 figura_estatica.py [grau_min] [saida.svg] [rede.json]"""
import os,sys
if os.environ.get('PYTHONHASHSEED')!='0':   # Louvain do networkx depende da ordem de hash dos conjuntos: fixa para reproduzir a mesma figura
    os.environ['PYTHONHASHSEED']='0'; os.execv(sys.executable,[sys.executable]+sys.argv)
import json,sys,collections
import networkx as nx
from redes.viz import similitude
gmin=int(sys.argv[1]) if len(sys.argv)>1 else 3
out=sys.argv[2] if len(sys.argv)>2 else 'rede_figura.svg'
d=json.load(open(sys.argv[3] if len(sys.argv)>3 else 'rede.json'))
AGG={'Pesquisadores anglo-americanos de EE','Pesquisadores brasileiros de EE','Pesquisadores latino-americanos em EE','Pesquisadores brasileiros formados no exterior','Pesquisa em EE de língua espanhola e portuguesa','Escola espanhola de Educação Estatística'}
syn={n['id'] for n in d['nodes'] if n['type'] in('documento','marco') or n['id'] in AGG}
G=nx.Graph(); claims=collections.defaultdict(set)
for e in d['edges']:
    a,b=e['source'],e['target']
    if a==b or a in syn or b in syn: continue
    claims[frozenset((a,b))].add((e['source'],e['relation'],e['target']))
for k,v in sorted(claims.items(),key=lambda kv:sorted(kv[0])):
    a,b=sorted(k); G.add_edge(a,b,weight=len(v))
core=[n for n in G if G.degree(n)>=gmin]
H=G.subgraph(core).copy(); H.remove_nodes_from([n for n in list(H) if H.degree(n)==0])
H=H.subgraph(max(nx.connected_components(H),key=len)).copy()
comms=nx.community.louvain_communities(H,weight='weight',seed=3)
comms=sorted(comms,key=lambda c:-sum(H.degree(n,weight='weight') for n in c))
com={n:i for i,c in enumerate(comms) for n in c}
ids={n:'n%d'%i for i,n in enumerate(H)}
formas=[dict(id=ids[n],forma=n if len(n)<=34 else n[:32]+'…',frequencia=int(H.degree(n,weight='weight')),comunidade=com[n],resumos=H.degree(n),idioma='pt') for n in H]
T=nx.maximum_spanning_tree(H,weight='weight'); tree={frozenset(e) for e in T.edges()}
arestas=[dict(origem=ids[a],destino=ids[b],peso=float(w['weight']),tipo='arvore' if frozenset((a,b)) in tree else 'extra') for a,b,w in H.edges(data=True)]
infos=[dict(id=i,n=len(c),nome=', '.join(t if len(t)<=26 else t[:24]+'…' for t in sorted(c,key=lambda n:-H.degree(n,weight='weight'))[:3])) for i,c in enumerate(comms)]
ndoc=len({e['doc'] for e in d['edges']})
res=dict(formas=formas,arestas=arestas,comunidades=infos,n_resumos=ndoc,idiomas_nas_formas=['pt'],n_extras=sum(a['tipo']=='extra' for a in arestas),parametros={})
rod=(f"Como foi construída: {len(d['edges'])} arestas ({sum(1 for e in d['edges'] if e['confidence']=='afirmada')} afirmadas, o restante incerto) extraídas de {ndoc} documentos lidos em fichas com página; "
     f"cada ligação existe porque ao menos uma fonte a afirma, sem inferência. Nós: {len(d['nodes'])-len(syn)} entidades reais (pessoas, instituições, eventos, grupos, periódicos, programas); "
     f"os {len(syn)} nós-síntese (documentos, conceitos e agregados) foram omitidos. A figura mostra os {H.number_of_nodes()} nós com {gmin} ou mais vizinhos distintos e {H.number_of_edges()} ligações "
     f"(cheias: árvore de maior peso; tracejadas: demais). Tamanho do nó = número de afirmações distintas em que aparece. Blocos: agrupamento automático de Louvain; "
     f"posição: layout do programa Redes, sem significado histórico. A rede mede o corpus, não a área.")
open(out,'w').write(similitude.svg(res,titulo='',rodape=rod)); print(len(H),H.number_of_edges(),len(comms))
