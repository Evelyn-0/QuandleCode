n=2

gen = 3
init = [[3,1,2,1,3,1,2,1,2,1],[1,2,1,2,1,2,1,3,1,2,1,2],[3,1,2,1,2,3,1,2]]

sec = []

for i in range(gen):
    sec.append([i+1, i+1])

for i in init:
    start = i[0]
    end = i[-1]
    exp = i[1:-1]
    build = []
    build.extend(exp[::-1])
    build.append(start)
    build.extend(exp)
    build.append(end)
    sec.append(build)

print(sec)
# print(sec)