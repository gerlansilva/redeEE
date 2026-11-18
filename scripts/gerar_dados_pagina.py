"""Gera rede_data.json (compacto) para a página interativa a partir de rede.json.
Nós-síntese: documentos, marcos (conceitos) e agregados de pesquisadores. Uso: python3 gerar_dados_pagina.py rede.json rede_data.json"""
import json,sys,collections as C
src=sys.argv[1] if len(sys.argv)>1 else 'rede.json'; dst=sys.argv[2] if len(sys.argv)>2 else 'rede_data.json'
d=json.load(open(src))
AGG={'Pesquisadores anglo-americanos de EE','Pesquisadores brasileiros de EE','Pesquisadores latino-americanos em EE','Pesquisadores brasileiros formados no exterior','Pesquisa em EE de língua espanhola e portuguesa','Escola espanhola de Educação Estatística'}
syn=lambda n:1 if n['type'] in('documento','marco') or n['id'] in AGG else 0
nodes=[[n['id'],n['type'],n['ctx'] or '',n.get('city') or '',n['note'] or '',n['degree'],syn(n)] for n in d['nodes']]
def cls(e):
    a=e['ctx_source']=='Brasil'; b=e['ctx_target']=='Brasil'
    return 'BB' if a and b else ('EE' if not a and not b else 'P')
edges=[[e['source'],e['target'],e['relation'],e['year'],e['year_end'],1 if e['confidence']=='incerta' else 0,1 if e['conflict'] else 0,cls(e),e['evidence'] or '',e['doc'] or '',e['page'] or '',e['ctx_source'] or '',e['ctx_target'] or '',1 if e['unif_provavel'] else 0,e.get('corrigida') or ''] for e in d['edges']]
docs=C.Counter(e['doc'] for e in d['edges']).most_common()
json.dump({'nodes':nodes,'edges':edges,'docs':docs},open(dst,'w'),ensure_ascii=False,separators=(',',':'))
print(len(nodes),len(edges),len(docs))
