import json,glob,collections,csv,sys,os
ALIAS={
"GrEF":"GREF","Maria-Gabriella Ottaviani":"Maria Gabriella Ottaviani","Grupo de estocástica do PME":"Grupo de Estocástica do PME",
"Irene Cazorla":"Irene Maurício Cazorla","Irene Mauricio Cazorla":"Irene Maurício Cazorla",
"Ailton Paulo de Oliveira Junior":"Ailton Paulo de Oliveira Júnior",
"Enfoque Ontosemiótico":"Enfoque Ontosemiótico (EOS)",
"Conferência IASE/PRESTA (Florianópolis, 1999)":"CIEEE 1999 (Florianópolis)",
"IASE Satellite Conference (Rio de Janeiro, 2015)":"9ª Conferência Satélite da IASE (Rio de Janeiro, 2015)",
"1º SIPEM (2000)":"I SIPEM (Serra Negra, 2000)",
"Round Tables do Comitê de Educação do ISI":"Round Tables do Comitê de Educação do ISI (1968-1988)","Round Tables do ISI":"Round Tables do Comitê de Educação do ISI (1968-1988)",
"Educação Estatística no Brasil":"Pesquisa em Educação Estatística no Brasil","Pesquisa em EE no Brasil":"Pesquisa em Educação Estatística no Brasil",
"Universidade de Grenoble I":"Universidade de Grenoble",
"Pedro Barbetta":"Pedro A. Barbetta","Maria Wodewotzki":"Maria Lúcia Wodewotzki","Lisbeth Cordani":"Lisbeth Kaiserlian Cordani",
"Cileda Coutinho":"Cileda de Queiroz e Silva Coutinho","Gilda Guimarães":"Gilda Lisbôa Guimarães","Verônica Kataoka":"Verônica Yumi Kataoka",
"D. Vere-Jones":"David Vere-Jones","J. Gani":"Joe Gani",
# por sobrenome / iniciais (sinalizado como unificação provável); C. A. Peres e P. A. Morettin = Clóvis Peres e Pedro Morettin, confirmado pelo autor (13/11/2026), fora de PROVAVEL
"Carlos Monteiro":"Carlos Eduardo Ferreira Monteiro","Cileda Q. S. Coutinho":"Cileda de Queiroz e Silva Coutinho","Suzi Samá":"Suzi Samá Pinto","José Ivanildo Felizberto de Carvalho":"José Ivanildo Felisberto de Carvalho","Rute Elizabete Souza de Rosa Borba":"Rute Borba","Gref":"GREF","Geração":"Grupo de Estudos em Raciocínio Combinatório (UFPE)",
"Instituto Interamericano de Estatística":"IASI","Grupo FQM126 (Granada)":"Grupo FQM-126 (Granada)","Grupo PAI FQM-126 (Universidade de Granada)":"Grupo FQM-126 (Granada)","C. Coutinho":"Cileda de Queiroz e Silva Coutinho","Garfield":"Joan Garfield","Ottaviani":"Maria Gabriella Ottaviani","Shaughnessy":"Michael Shaughnessy","Wild":"Chris Wild",
"Jolliffe":"Flavia Jolliffe","Ben-Zvi":"Dani Ben-Zvi","Fischbein":"Efraim Fischbein","Cordani":"Lisbeth Kaiserlian Cordani","S. A. Rice":"Stuart A. Rice",
"C. A. Peres":"Clóvis Peres","P. A. Morettin":"Pedro Morettin","Dione Carvalho":"Dione Lucchesi de Carvalho","Pedro Luis do Nascimento Silva":"Pedro L. N. Silva","Round Table IASE Tóquio 2000":"Round Table Formação de Pesquisadores no Uso da Estatística",
}
# correções de 13/11/2026 (site da conferência recuperado, imagens e índice): SPAINFL e BND-BRAX são bandeiras da Espanha e do Brasil (botões de idioma), não apoios; INE é o Departamento de Informática e Estatística da UFSC
DROP={"SPAINFL","BND-BRAX"}
ALIAS["INE [apoio CIEEE]"]="INE/UFSC"
PROVAVEL={"C. Coutinho","Garfield","Ottaviani","Shaughnessy","Wild","Jolliffe","Ben-Zvi","Fischbein","Cordani","S. A. Rice"}
a=lambda x:ALIAS.get(x,x)
E=[];N=[]
for f in sorted(glob.glob('edges_*.jsonl')):
    for l in open(f):
        if l.strip(): d=json.loads(l); d['lote']=f[6:-6]; E.append(d)
for f in sorted(glob.glob('nodes_*.jsonl')):
    for l in open(f):
        if l.strip(): d=json.loads(l); d['lote']=f[6:-6]; N.append(d)
n0=len(E)
seen=set();out=[]
for e in E:
    s0,t0=e['source'],e['target']
    e['source'],e['target']=a(s0),a(t0)
    e['unif_provavel']=bool({s0,t0}&PROVAVEL)
    if e['source']=='Enfoque Ontosemiótico (EOS)' and e['target']=='Universidade de Granada' and e['relation']=='originou':
        e['source'],e['target']=e['target'],e['source']; e['source_type'],e['target_type']=e['target_type'],e['source_type']; e['ctx_source'],e['ctx_target']=e['ctx_target'],e['ctx_source']; e['corrigida']='direção invertida (parecer 4)'
    if e['source'] in DROP or e['target'] in DROP: continue
    if e['source']=='INE/UFSC':
        e['ctx_source']='Brasil'; e['corrigida']='INE = Departamento de Informática e Estatística da UFSC (logotipo ine.jpg do site), não apoio externo'
    if e['source']==e['target']: continue
    if e['source']=='Carmen Batanero' and e['target']=='UNICAMP' and e['doc']=='Araújo 2017' and e['relation']=='ministrou_curso_em' and not e['conflict']:
        e['conflict']=True; e['corrigida']='conflict=true: relatos divergem sobre convidante, local e ano da visita (Ody 2019; Conti s.d.)'
    k=(e['source'],e['target'],e['relation'],e.get('year'),e['doc'],e['page'])
    if k in seen: continue
    seen.add(k); out.append(e)
nodes={}
for n in N:
    i=a(n['id']); n['id']=i
    if i in DROP: continue
    if i=='INE/UFSC': n['ctx']='Brasil'
    if i in nodes:
        m=nodes[i]
        for fld in ('ctx','city','year_start'):
            if not m.get(fld) and n.get(fld): m[fld]=n[fld]
        if n.get('note') and n['note'] not in (m.get('note') or ''): m['note']=((m.get('note') or '')+' | '+n['note']).strip(' |')
    else: nodes[i]=dict(n)
for e in out:
    for side,tp,cx in (('source','source_type','ctx_source'),('target','target_type','ctx_target')):
        i=e[side]
        if i not in nodes: nodes[i]=dict(id=i,type=e[tp],ctx=e[cx],city=None,year_start=None,note='')
        elif not nodes[i].get('type'): nodes[i]['type']=e[tp]
deg=collections.Counter()
for e in out: deg[e['source']]+=1; deg[e['target']]+=1
for i,n in nodes.items(): n['degree']=deg.get(i,0)
json.dump(dict(nodes=list(nodes.values()),edges=out),open('rede.json','w'),ensure_ascii=False)
with open('arestas_para_conferencia.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['source','relation','target','year','ctx_source','ctx_target','confidence','conflict','unif_provavel','doc','page','evidence','lote'])
    for e in out: w.writerow([e['source'],e['relation'],e['target'],e.get('year'),e['ctx_source'],e['ctx_target'],e['confidence'],e['conflict'],e['unif_provavel'],e['doc'],e['page'],e['evidence'],e['lote']])
print('arestas',n0,'->',len(out),'| nós',len(nodes),'| conflito',sum(e['conflict'] for e in out),'| incerta',sum(e['confidence']=='incerta' for e in out),'| unif provável',sum(e['unif_provavel'] for e in out))
print('nós isolados:',[i for i,n in nodes.items() if n['degree']==0])
print('top grau:',deg.most_common(15))
