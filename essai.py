g=dict()

g["a"] == set(("d","b"))
g["b"] == set(("a","d","c"))
g["c"] == set(("d","b"))
g["d"] == set(("a","b","c"))


def creer_cycle(a):
    chemin=[a]
    while True:
        x=chemin[-1]
        for y in g[x]:
            if y != x:
                chemin.append(y)
                if y in chemin[:-1]:
                    return chemin
                else:
                    break
            break

creer_cycle("a")

