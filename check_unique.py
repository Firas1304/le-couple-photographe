import re,glob,itertools,sys
def text(f):
    s=open(f,encoding='utf-8').read()
    m=re.search(r'<main.*?(?=<footer)',s,re.S)
    t=m.group(0) if m else s
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    t=re.sub(r'<[^>]+>',' ',t); w=re.sub(r'\s+',' ',t).lower().split()
    return w
def sh(w,n=5): return {' '.join(w[i:i+n]) for i in range(len(w)-n+1)}
groups={'combos':sorted(glob.glob('services/*/*/index.html')),'zones':sorted(glob.glob('zones/*/index.html')),'services':[f for f in sorted(glob.glob('services/*/index.html')) if f.count('/')==2],'palaces':sorted(glob.glob('palaces/*/index.html')),'villes':sorted(glob.glob('villes/*/index.html'))}
for g,fs in groups.items():
    fs=[f for f in fs if not f.endswith('services/index.html')]
    S={f:sh(text(f)) for f in fs}; worst=(0,None,None); tot=0;n=0
    for a,b in itertools.combinations(fs,2):
        j=len(S[a]&S[b])/max(1,len(S[a]|S[b])); tot+=j;n+=1
        if j>worst[0]: worst=(j,a,b)
    print(g,len(fs),'pages; moyenne %.2f; pire %.2f'%(tot/max(n,1),worst[0]),worst[1],worst[2])
