N = 5
res = [[3,2],[3,0],[4,3],[1,4]]
#res = [[0,1],[1,3],[3,0],[1,2]]
#res = [[0,5],[5,2],[2,8],[8,0],[2,3],[3,1],[1,2],[2,9],[7,9],[7,2],[4,2],[4,6],[2,6]]
#res = [[1,4],[4,7],[7,9],[9,8],[8,6],[6,5],[5,3],[3,0],[0,2],[2,1]]
visit = [0] *(N)
edgesize = [[0,i] for i in range(N)]

# print(edgesize)
for i in range(len(res)):
    edgesize[res[i][0]][0] += 1

edgesize.sort()
answer = 0
idx = 0

while(N > 0):
    for i in range(N):
        if(visit[edgesize[i][1]] == 0):
            if(edgesize[i][0] == 0):
                visit[edgesize[i][1]] = 1
                idx = edgesize[i][1]
                N -= 1
                answer += 1
                break;
            else:
                flag = edgesize[i][0]
                ch = []
                for j in range(i,N):
                    if edgesize[j][0] == flag:
                        ch.append(edgesize[j][1])
                    else:
                        break
                if len(ch) == N:
                    visit[edgesize[i][1]] = 1
                    idx = edgesize[i][1]
                    N -= 1
                    # print(str(edgesize[i][1]) + "   seleted")
                    answer += 1
                    break;
                # print("!!!!!!!!!!!!!!!!!!!!!")
                # print(ch)
                flag = 0
                for t in range(1,len(edgesize)):
                    if flag:
                        break
                    for j in range(len(ch)):
                        if flag:
                            break
                        if j in g:
                            for k in range(len(g[j])):
                                if flag:
                                    break
                                if(g[j][k] == edgesize[len(edgesize)-t][1]):
                                    visit[j] = 1
                                    idx = j
                                    N -= 1
                                    # print(str(j) + "   seleted")
                                    answer += 1
                                    flag = 1
                                    break
                break
                
    # 선택된 노드 엣지 삭제 처리
    # 선택된 노드 나가는 엣지 삭제, 엣지 사이즈 처리도 필요,visit도 처리
    
    print("=======================")
    print("edge : {}".format(res))
    print("edgesize : {}".format(edgesize))
    print(idx)
    
    for i in range(len(res)):
        # 나가는
        if(res[i][0] == idx):
            print("out")
            visit[res[i][1]] = 1
            N -= 1
            subidx = res[i][1]
            for j in range(len(res)):
                if(res[j][1] == subidx):
                    for k in range(N):
                        if(edgesize[k][1] == res[j][0]):
                            edgesize[k][0] -= 1
                            break
                    del res[j]
                    # i -= 1
            print("edge : {}".format(res))
            print("edgesize : {}".format(edgesize))

        # 들어오는
        if(res[i][1] == idx):
            print("in")
            for j in range(N):
                if(edgesize[j][1] == res[i][0]):
                    print(i)
                    print(j)
                    edgesize[j][0] -= 1
            del res[i]
            print("edge : {}".format(res))
            print("edgesize : {}".format(edgesize))
    edgesize.sort()
print(answer)
