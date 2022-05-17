import turtle
import sys
import random
import time
from typing import List
import tkinter as tk
from operator import add

from move import Move

# 定数
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

MOVE = {
    RIGHT : (1, 0), 
    UP : (0, 1), 
    LEFT : (-1, 0), 
    DOWN : (0, -1),
}

INF = float("inf")

# Optionsの引数用
FEEDS_ALGO = "Feeds_algo"
TURTLE_ALGO = "Turtle_algo"
DISTANCE_FUNCTION = "DistanceFunction"
SIGHT = "sight"
SPEED = "Speed"
DELAY = "Delay"
GRID = "Grid"




# 色
colors = [
    "cadetblue", 
    "cyan",                 # 水色
    "chartreuse",           # 緑
    "purple",               # 紫
    "gold",                 # 黄色
    "magenta",              # ピンク
    "blue",                 # 青
    "green",                # 緑
]



"""
法則
"""
class Law:
    # 空間の範囲
    x_lim = (0, 1_00)          # 大きな値を設定した場合, gridで塗りつぶされる & 細かい動きが見えなくなる. 
    y_lim = (0, 1_00)

    # マージン, 餌と亀を設置できる範囲を壁からの距離で設定, 行動回数 < マージンとすることで実質無限の空間. 
    # とりあえず未使用
    margin = 0



"""
空間
"""
class Feald(Law):
    mode = {
        "Fastest":(0, 0), 
        "Fast": (0, 10), 
        "Normal": (0, 40), 
        "Slow": (1, 200)
        }
    
    Feeds = []
    Turtles = []
    
    FeedsAlgo = None
    TurtlesAlgo = None

    turn = 0
    delay = 0

    Options = {}



    def __init__(self, feeds:List[tuple], turtles:List[tuple], options) -> None:
        self.scr = turtle.Screen()
        x_mg = (Law.x_lim[1] - Law.x_lim[0]) // 10
        y_mg = (Law.y_lim[1] - Law.y_lim[0]) // 10
        turtle.setworldcoordinates(Law.x_lim[0]-x_mg, Law.y_lim[1]+y_mg, Law.x_lim[1]+x_mg, Law.y_lim[0]-y_mg)      # 画面のサイズを指定

        self.__wall()                               # 壁の描写
        if options[GRID]:                           # grid
            self.__grid()

        self.init_colors()
        
        self.Feeds = [Feed(x, y, options) for (x, y) in feeds]                   # 指定座標に餌を配置
        self.Turtles = [Turtle(x, y, options[SPEED]) for (x, y) in turtles]             # 指定座標に亀を配置
        self.FeedsAlgo = options[FEEDS_ALGO]                 # 餌のアルゴリズム
        self.TurtlesAlgo = options[TURTLE_ALGO]              # 亀のアルゴリズム
        self.delay = options[DELAY] / 1000
        self.Options = options

        
        # turtle.delay(delay)                         # 遅延をms単位で指定 -> tracerをオフにすることで無効
        turtle.tracer(0)                            # トレーサーをオフにする. (画面内の亀を全て同時に描写する事で早くする)


    def __wall(self):                                # 壁
        tmp = turtle.Turtle()
        tmp.hideturtle()
        tmp.speed(4)
        tmp.penup()
        tmp.setpos(self.x_lim[0], self.y_lim[0])
        tmp.pendown()
        tmp.setpos(self.x_lim[1], self.y_lim[0])
        tmp.setpos(self.x_lim[1], self.y_lim[1])
        tmp.setpos(self.x_lim[0], self.y_lim[1])
        tmp.setpos(self.x_lim[0], self.y_lim[0])
        
        tmp.penup()
        tmp.setpos(-1, -1)                          # 消せないから範囲外に置く. clearは書いた線も消える. -> turtlesで取得されるオブジェクトは描写されている物のみ -> penupすると映らない. 


    def __grid(self):
        color = (0.8, 0.8, 0.8)     # RGB
        V = turtle.Turtle()         # 垂直方向
        H = turtle.Turtle()         # 水平方向

        V.hideturtle()              # コンフィグ. 亀を非表示. 
        H.hideturtle()
        V.speed(0)
        H.speed(0)
        turtle.delay(0)

        V.pencolor(color)           # 色を指定
        H.pencolor(color)

        V.penup()
        H.penup()
        V.setpos(self.x_lim[0], self.y_lim[0])      # 左上へ移動
        H.setpos(self.x_lim[0], self.y_lim[0])

        while V.xcor() + 1 < Law.x_lim[1] or H.ycor() + 1 < Law.y_lim[1]:
            if V.xcor() + 1 < Law.x_lim[1]:         # 垂直方向の描写
                V.setx(V.xcor() + 1)           # 右へ1マス移動
                V.pendown()
                V.sety(Law.y_lim[1])            # 下向きに線を引いて上へ戻す
                V.penup()
                V.sety(Law.y_lim[0])

            if H.ycor() + 1 < Law.y_lim[1]:         # 水平方向の描写
                H.sety(H.ycor() + 1)
                H.pendown()
                H.setx(Law.x_lim[1])
                H.penup()
                H.setx(Law.x_lim[0])

        V.penup()
        H.penup()
        V.setpos(-1, -1)
        H.setpos(-1, -1)


    def init_colors(self):          # turtleで使用する色のリストを作成
        global colors
        colors = [
            "cadetblue", 
            "cyan",                 # 水色
            "chartreuse",           # 緑
            "purple",               # 紫
            "gold",                 # 黄色
            "magenta",              # ピンク
            "blue",                 # 青
            "green",                # 緑
        ]


    def start(self):
        op = self.Options
        while op["max-loop"] > 0 and self.end_check():
            self.play()
            op["max-loop"] -= 1



    def play(self):             # 1ターン進める
        for i in self.Turtles:
            i.run(algo=self.TurtlesAlgo, option=self.Options)

        self.eat_check()                # 餌を食べたか確認
        
        turtle.update()                 # 画面の更新
        time.sleep(self.delay)
        
        self.turn += 1


    def eat_check(self):        # 餌と亀が重なっているかを確認
        t = [i for i in turtle.turtles() if i.shape() == "turtle"]                  # 亀のリスト
        f = [i for i in turtle.turtles() if i.shape() == "circle"]                  # 餌のリスト

        for kame in t:
            for esa in f:
                if kame.pos() == esa.pos():             # 亀と重複した座標を持つ餌を確認
                    esa.hideturtle()                    # 餌を非表示にする



    def end_check(self)->bool:        # 餌が残っているか確認
        f = [i for i in turtle.turtles() if i.shape() == "circle" and i.isvisible()]
        return bool(f)




"""
餌クラス
今のところ、目標物
"""
class Feed(Law):             
    def __init__(self, x:int, y:int, op:dict) -> None:
        if Law.x_lim[0] + Law.margin <= x <= Law.x_lim[1] - Law.margin:       # 餌がFeald内に収まっているかの確認
            pass
        else:
            print("ERROR: invalid x position", file=sys.stderr)
            sys.exit(1)

        if Law.y_lim[0] + Law.margin <= y <= Law.y_lim[1] - Law.margin:
            pass
        else:
            print("ERROR: invalid y position", file=sys.stderr)
            sys.exit(1)

        # 餌の描写
        self.Feed = turtle.Turtle()
        self.Feed.shape("circle")
        self.Feed.color("Red")
        self.Feed.hideturtle()
        self.Feed.penup()
        self.Feed.setpos(x, y)
        self.Feed.pendown()
        self.Feed.showturtle()


        if op["Turtle_algo"].__name__ == "HaveNose":
            tmp = turtle.Turtle()
            tmp.color("Red")
            tmp.hideturtle()
            tmp.penup()
            tmp.setpos(x, y-op["sight"])
            tmp.pendown()
            if op["DistanceFunction"] == "Euclidean":
                tmp.circle(radius=op["sight"])
            elif op["DistanceFunction"] == "Manhattan":
                tmp.circle(radius=op["sight"], steps=4)
            else:
                print("Undefined distance function", file=sys.stderr)
                sys.exit()
            
            tmp.penup()





"""
亀クラス
"""
class Turtle(Law):
    def __init__(self, x:int, y:int, speed:int) -> None:
        if Law.x_lim[0] + Law.margin <= x <= Law.x_lim[1] - Law.margin:       # 餌がFeald内に収まっているかの確認
            pass
        else:
            print("ERROR: invalid x position", file=sys.stderr)
            sys.exit(1)

        if Law.y_lim[0] + Law.margin <= y <= Law.y_lim[1] - Law.margin:
            pass
        else:
            print("ERROR: invalid y position", file=sys.stderr)
            sys.exit(1)

        # config
        self.T = turtle.Turtle()
        self.T.speed(speed=speed)
        self.T.color(self._individual_colors())
        self.T.shape("turtle")
        self.T.width(2)

        # set
        self.T.penup()
        self.T.setpos(x, y)
        self.T.pendown()


    def _individual_colors(self):
        if len(colors) > 0:
            return colors.pop()
        else:
            return (random.random(), random.random(), random.random())      # RGB [0~1)




    def run(self, algo:Move, option):
        x = [(True, 1), (False, 1), (True, -1), (False, -1)]        # True->水平, False->垂直
        flag = False
        # 壁のチェック
        while not flag:                                             # 壁のない方向が出るまで繰り返す
            direction = algo(T=self.T, option=option)               
            if x[direction][0]:
                flag = Law.x_lim[0] <= self.T.xcor() + x[direction][1] <= Law.x_lim[1]
            else:
                flag = Law.y_lim[0] <= self.T.ycor() + x[direction][1] <= Law.y_lim[1]


        # self.T.setheading(direction * 90)   # 頭の方向を決めて前進 -> 誤差の原因
        # self.T.forward(1)                  
        # print("座標:{}, 角度:{}".format(self.T.pos(), self.T.heading()))
        next_pos = tuple(map(add, self.T.pos(), MOVE[direction]))       # 移動先の座標を計算
        self.T.setpos(next_pos)                                         # 指定座標へ移動




