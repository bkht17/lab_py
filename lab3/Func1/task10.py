def is_unique(lsst):
    ulist = []
    for i in range(len(lsst)):
        if lsst[i] not in ulist:
            ulist.append(lsst[i])
    
    for x in ulist:
        print(x, end=" ")

test = [x for x in input().split()]
print(is_unique(test))