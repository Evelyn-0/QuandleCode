# 1,1,1
gen = 3
k = 2

init = [[1,2,1,2,1,3,1,2,1,3]]

threek4 = int(3*k+4)
threek4list = [1,2]
if threek4 < 0:
    threek4list = [2,1]
    threek4 = abs(threek4)

init.append([2,1,3,*[v for _ in range(threek4) for v in threek4list],3])

if k % 2 == 0:
    threek2 = int((3*k+2)/2)
    threek2list = [1,2]
    threek = int(3*k/2)
    threeklist = [2,1]

    if threek2 < 0:
        threek2list = [2,1]
        threek2 = abs(threek2)
    
    if threek < 0:
        threeklist = [1,2]
        threek = abs(threek)

    init.append([2,*[v for _ in range(threek2) for v in threek2list],3,*[v for _ in range(threek) for v in threeklist],1])
else:
    threek1 = int((3*k-1)/2)
    threek1list = [1,2]
    threek3 = int((3*k+3)/2)
    threek3list = [2,1]

    if threek1 < 0:
        threek1list = [2,1]
        threek1 = abs(threek1)

    if threek3 < 0:
        threek3list = [1,2]
        threek3 = abs(threek3)

    init.append([2,*[v for _ in range(threek1) for v in threek1list],3,*[v for _ in range(threek3) for v in threek3list],1])
print(init)