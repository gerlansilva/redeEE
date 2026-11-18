"""Calcula as posições da rede com o algoritmo de layout do programa Redes (redes.viz.similitude):
Louvain por bloco, layout de molas dentro de cada bloco, separação de caixas (círculo + rótulo) e
disposição dos blocos sem que as manchas se toquem. Gera layouts.json para a página interativa."""
import os,sys
if os.environ.get('PYTHONHASHSEED')!='0':   # Louvain do networkx depende da ordem de hash dos conjuntos: fixa para reproduzir a mesma figura
    os.environ['PYTHONHASHSEED']='0'; os.execv(sys.executable,[sys.executable]+sys.argv)
import json,collections,sys
import networkx as nx
from redes.viz import similitude as sim
D=json.load(open('rede_data.json'))
nodes={n[0]:n for n in D['nodes']}
def layout_for(gmin,syn,cls=None,ego=None):
    claims=collections.defaultdict(set)
    EN=None
    if ego:
        EN={ego}|{e[1] for e in D['edges'] if e[0]==ego}|{e[0] for e in D['edges'] if e[1]==ego}
    for e in D['edges']:
        a,b=e[0],e[1]
        if a==b: continue
        if cls and e[7]!=cls: continue
        if EN is not None and (a not in EN or b not in EN): continue
        if not syn and (nodes[a][6] or nodes[b][6]): continue
        claims[frozenset((a,b))].add((e[0],e[2],e[1]))
    G=nx.Graph()
    for k,v in sorted(claims.items(),key=lambda kv:sorted(kv[0])):
        a,b=sorted(k); G.add_edge(a,b,weight=len(v))
    core=[n for n in G if G.degree(n)>=gmin]
    H=G.subgraph(core).copy(); H.remove_nodes_from([n for n in list(H) if H.degree(n)==0])
    comms=nx.community.louvain_communities(H,weight='weight',seed=3)
    comms=sorted(comms,key=lambda c:-sum(H.degree(n,weight='weight') for n in c))
    com={n:i for i,c in enumerate(comms) for n in c}
    ids={n:'n%d'%i for i,n in enumerate(H)}; inv={v:k for k,v in ids.items()}
    formas=[dict(id=ids[n],forma=n if len(n)<=34 else n[:32]+'…',frequencia=int(H.degree(n,weight='weight')),comunidade=com[n],resumos=H.degree(n),idioma='pt') for n in H]
    T=nx.maximum_spanning_tree(H,weight='weight'); tree={frozenset(e) for e in T.edges()}
    arestas=[dict(origem=ids[a],destino=ids[b],peso=float(w['weight']),tipo='arvore' if frozenset((a,b)) in tree else 'extra') for a,b,w in H.edges(data=True)]
    infos=[dict(id=i,n=len(c),nome=', '.join(t if len(t)<=26 else t[:24]+'…' for t in sorted(c,key=lambda n:-H.degree(n,weight='weight'))[:3])) for i,c in enumerate(comms)]
    res=dict(formas=formas,arestas=arestas,comunidades=infos,n_resumos=50,idiomas_nas_formas=['pt'],n_extras=0,parametros={})
    pos=sim.layout(res)
    out={inv[i]:[round(d['x'],1),round(d['y'],1),round(d['r'],2),round(d['fs'],2),round(d['tw'],1),d['com'],d['txt']] for i,d in pos.items()}
    return dict(pos=out,com=[c['nome'] for c in infos])
L={}
import time
for syn in (0,1):
    for cls in (None,'P','EE','BB'):
        for g in (1,2,3):
            k=f"{cls or 'all'}_{g}_{syn}"
            try: L[k]=layout_for(g,syn,cls)
            except Exception as ex: print('skip',k,ex); continue
            print(k,len(L[k]['pos']),flush=True)
# layouts de ego (nó e vizinhos), só nós reais
deg=collections.Counter()
for e in D['edges']:
    if nodes[e[0]][6] or nodes[e[1]][6]: continue
    deg[e[0]]+=0
nb=collections.defaultdict(set)
for e in D['edges']:
    if nodes[e[0]][6] or nodes[e[1]][6] or e[0]==e[1]: continue
    nb[e[0]].add(e[1]); nb[e[1]].add(e[0])
for n,v in nb.items():
    if len(v)>=2:
        try: L['ego_'+n]=layout_for(1,0,None,n)
        except Exception as ex: print('skip ego',n,ex)
print('egos',sum(1 for k in L if k.startswith('ego_')))
json.dump(L,open('layouts.json','w'),ensure_ascii=False,separators=(',',':'))
