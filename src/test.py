import sys
import os
tmppath = os.path.normpath(os.path.join(os.path.dirname(__file__), "./lib"))        # 下位ディレクトリのファイルの追加
sys.path.append(tmppath)
from lib import object
from lib.move import Move
import turtle

import time


def main():
    feed = [(50, 50)]
    kame = [(10, 10), (90, 90), (0, 10), (60 ,60)]

    options = {
        # 移動アルゴリズム
        "Feeds_algo" : Move.stay, 
        "Turtle_algo" : Move.HaveEye, 

        # 距離関係
        "DistanceFunction" : "Manhattan",          # Euclidean or Manhattan
        # "DistanceFunction" : "Euclidean",
        "sight" : 10, 
        
        # 亀の移動速度
        "Speed" : 0,        # 0 -> 10 -> 9 -> 8 -> ... -> 2 -> 1 の順に遅くなる. 正直余り変わらない. 移動距離を伸ばすと意味が出そう
        "Delay" : 0,        # 1ターンごとの遅延時間. (ms), 1 (s) = 1000 (ms)

        # グリッドの描写
        "Grid" : True, 

        # 行動回数
        "loop" : 1000, 
    }

    x = object.Feald(feeds=feed, turtles=kame, options=options)
    print([i.shape() for i in x.scr.turtles()])

    t1 = time.perf_counter()
    for i in range(options["loop"]):
        x.play()
    
    t2 = time.perf_counter()

    print(t2 - t1)
    # time.sleep(10)



if __name__ == "__main__":
    main()
