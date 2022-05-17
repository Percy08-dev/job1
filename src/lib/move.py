import random
import turtle
import math
from operator import sub

class Move:
    def stay(T, option):
        return None

    def RandomWalk(T, option):
        return random.randint(0, 3) 

    def HaveNose(T:turtle, option):          # 一定距離内に来た際に目標に直進する.
        sight = option["sight"]
        r = -1
        if option["DistanceFunction"] == "Euclidean":
            df = Move._euclidean
        elif option["DistanceFunction"] == "Manhattan":
            df = Move._manhattan

        for F in [i for i in turtle.turtles() if i.shape() == "circle"]:            # 見えたものを距離に関係なく食べに行く（若干バカ）
            # print("p1:({:.60f}, {:.60f})".format(T.pos()[0], T.pos()[1]))         # タートルグラフィックスの内部は単精度とか？
            p1 = [round(i, 0) for i in T.pos()]     # 偶数丸めだけど、浮動小数点数誤差の修正なら問題ない
            p2 = [round(i, 0) for i in F.pos()]
            # print("({:.20f}, {:.20f})".format(T.pos()[0], T.pos()[1]), "->", p1)
            d = df(p1=p1, p2=p2)
            if d <= sight:
                tmp = tuple(map(sub, p2, p1))            # (50.00,49.00) (50.00,50.00) -> ( -7.105427357601002e-15 0.999999999999936 ) ベクトル演算の誤差 -> 移動方法の変更で対応
                if tmp[0] < 0:
                    r = 2
                    break
                elif tmp[0] > 0:
                    r = 0
                    break
                elif tmp[1] < 0:
                    r = 3
                    break
                elif tmp[1] > 0:
                    r = 1
                    break
        else:
            r = Move.RandomWalk(T, option)

        return r


    
    # 距離計算
    def _euclidean(p1, p2):
        d2 = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
        return math.sqrt(d2)

    def _manhattan(p1, p2):
        tmp = [abs(i-j) for i, j in zip(p1, p2)]
        return sum(tmp)
