import sys
import os
tmppath = os.path.normpath(os.path.join(os.path.dirname(__file__), "../src/lib"))        # 下位ディレクトリのファイルの追加
sys.path.append(tmppath)
from lib.object import Feald, INF
from lib.move import Move



def main():
    feed = [(50, 50)]
    kame = [(10, 10), (90, 90)]

    options = {
        # 範囲設定
        "x_lim" : 100, 
        "y_lim" : 100, 

        # grid分割数
        "sep" : 10, 
        
        # 移動アルゴリズム
        "Feeds_algo" : Move.RandomWalk, 
        "Turtle_algo" : Move.HaveNose, 

        # 距離関係
        "DistanceFunction" : "Euclidean",
        "sight" : 30, 
        
        # 亀の移動速度
        "Speed" : 0,        # 0 -> 10 -> 9 -> 8 -> ... -> 2 -> 1 の順に遅くなる. 正直余り変わらない. 移動距離を伸ばすと意味が出そう
        "Delay" : 0,        # 1ターンごとの遅延時間. (ms), 1 (s) = 1000 (ms)

        # グリッドの描写
        "Grid" : True, 

        # 行動回数
        "max-loop" : INF,      # 整数 or INF
    }
    
    x = Feald(feeds=feed, turtles=kame, options=options)
    x.start()


if __name__ == "__main__":
    main()
