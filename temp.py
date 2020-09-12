N = 5
res = [[3,2],[3,0],[4,3],[1,4]]
visit = [0] *(N)
edgesize = [[0,i] for i in range(N)]
g = {}
print(edgesize)
for i in range(len(res)):
  edgesize[res[i][0]][0] += 1
  if res[i][0] in g:
    #update
    g[res[i][0]].append(res[i][1])
    pass
  else:
    g[res[i][0]] = [res[i][1]]

edgesize.sort()
print(g, edgesize)

answer = 0
idx = 0



while(N > 0):
  print(visit)
  for i in range(len(visit)):
    if(visit[edgesize[i][1]] == 0):
      visit[edgesize[i][1]] = 1
      idx = i
      N -= 1
      break;
  print(str(edgesize[i][1]) + "   seleted")
    for p,c in tree.items():
        for j in range(len(c)):
            if(c[j] == a):
                roada.append(a)
                a = p
                break
  
  answer += 1
  #선택된 
  if edgesize[idx][1] in g:
    for i in range(len(g[edgesize[idx][1]])):
      visit[g[edgesize[idx][1]][i]] = 1
      N -= 1

print(answer)