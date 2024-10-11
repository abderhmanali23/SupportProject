l = []
r = 1
u = v = 0
for i in range(50):
    c = input().split('//')

    
    if c[0].startswith('/*'):
        r = 0
        continue
    elif c[0].endswith('*/'):
        r = 1
        continue
    if r and c[0]:
        l.append(c[0])
    if '{' in c[0]:
        u += 1
    if '}' in c[0]:
        v += 1
        if u == v:
            break

print(*l, sep="\n")
