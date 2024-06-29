from settings import *
from random import choice
bit = [4,2,1]                               #fired,hitted,destroyed
class FSMStat:
    may_2 = 0
    may_3 = 0
    may_5 = 0
    must = False
    prob = 0
    def __repr__(self):
        return f"<FSM 2:{self.may_2},3:{self.may_3},5:{self.may_5} must:{self.must} prob:{self.prob}>"
def may(stmap,x,y):
    return (not stmap[x][y][0]) or (stmap[x][y][1] and (not stmap[x][y][2]))
def available(x,y):
    return x >= 0 and x < MAPSIZE and y >= 0 and y < MAPSIZE
def analyze(map,cnt_2,cnt_3,cnt_5):
    scmap = [[0 for i in range(MAPSIZE)] for i in range(MAPSIZE)]
    stmap = [[[j & bit[0] == bit[0],j & bit[1] == bit[1],j & bit[2] == bit[2]] for j in i] for i in map]
    ls = [[FSMStat() for i in range(MAPSIZE)] for i in range(MAPSIZE)]
    for y in range(MAPSIZE):
        for scx_2 in range(-1,MAPSIZE):
            stat = True
            for i in range(scx_2,scx_2 + 2):
                if available(i,y):
                    if not may(stmap,i,y):
                        stat = False
                        break
            if stat:
                for i in range(scx_2,scx_2 + 2):
                    if available(i,y):
                        ls[i][y].may_2 += 1
    for x in range(MAPSIZE):
        for scy_2 in range(-1,MAPSIZE):
            stat = True
            for i in range(scy_2,scy_2 + 2):
                if available(x,i):
                    if not may(stmap,x,i):
                        stat = False
                        break
            if stat:
                for i in range(scy_2,scy_2 + 2):
                    if available(x,i):
                        ls[x][i].may_2 += 1
    for y in range(MAPSIZE):
        for scx_3 in range(-2,MAPSIZE):
            stat = True
            for i in range(scx_3,scx_3 + 3):
                if available(i,y):
                    if not may(stmap,i,y):
                        stat = False
                        break
            if stat:
                for i in range(scx_3,scx_3 + 3):
                    if available(i,y):
                        ls[i][y].may_3 += 1
    for x in range(MAPSIZE):
        for scy_3 in range(-2,MAPSIZE):
            stat = True
            for i in range(scy_3,scy_3 + 3):
                if available(x,i):
                    if not may(stmap,x,i):
                        stat = False
                        break
            if stat:
                for i in range(scy_3,scy_3 + 3):
                    if available(x,i):
                        ls[x][i].may_3 += 1
    for y in range(MAPSIZE):
        for scx_5 in range(-4,MAPSIZE):
            stat = True
            for i in range(scx_5,scx_5 + 5):
                if available(i,y):
                    if not may(stmap,i,y):
                        stat = False
                        break
            if stat:
                for i in range(scx_5,scx_5 + 5):
                    if available(i,y):
                        ls[i][y].may_5 += 1
    for x in range(MAPSIZE):
        for scy_5 in range(-4,MAPSIZE):
            stat = True
            for i in range(scy_5,scy_5 + 5):
                if available(x,i):
                    if not may(stmap,x,i):
                        stat = False
                        break
            if stat:
                for i in range(scy_5,scy_5 + 5):
                    if available(x,i):
                        ls[x][i].may_5 += 1
    for x in range(MAPSIZE):
        for y in range(MAPSIZE):
            if stmap[x][y][0] and stmap[x][y][1] and (not stmap[x][y][2]):
                for g in [[1,0],[-1,0],[0,1],[0,-1]]:
                    if available(x + g[0],y + g[1]) and not stmap[x + g[0]][y + g[1]][0]:
                        ls[x + g[0]][y + g[1]].prob += 0.5
                for g in [[1,0],[-1,0],[0,1],[0,-1]]:
                    if available(x + g[0],y + g[1]) and stmap[x + g[0]][y + g[1]][0] and stmap[x + g[0]][y + g[1]][1] and (not stmap[x + g[0]][y + g[1]][2]) and available(x - g[0],y - g[0]) and not stmap[x - g[0]][y - g[1]][0]:
                        ls[x - g[0]][y - g[1]].prob += 1
    for x in range(MAPSIZE):
        for y in range(MAPSIZE):
            scmap[x][y] = 0.0 if stmap[x][y][0] else (max(ls[x][y].may_2,cnt_2) + max(ls[x][y].may_3,cnt_3) + max(ls[x][y].may_5,cnt_5)) + (int(ls[x][y].must) * 1e16 + ls[x][y].prob * 1000)
    return scmap
def next_step(map_,cnt_2,cnt_3,cnt_5):
    scmap = analyze(map_,cnt_2,cnt_3,cnt_5)
    maxn = -1e9
    ls = []
    for i in scmap:
        maxn = max(maxn,max(i))
    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
            if scmap[i][j] == maxn:
                ls.append((i,j))
    return choice(ls)
# ori_map = [[0,0,0,0,0],[0,6,0,0,0],[0,6,6,6,0],[0,0,7,0,0],[0,0,7,0,0]]
# for _ in range(10):
#     ana_1 = analyze(ori_map)
#     for i in ori_map:
#         for j in i:
#             print(j,end="\t")
#         print()
#     ans_1 = next_step(ori_map)
#     print(ans_1)
#     ori_map[ans_1[0]][ans_1[1]] |= 4