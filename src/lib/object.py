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
    def __init__(self, x, y) -> None:
        if x < 0 or y < 0:
            print("ERROR: invalid range", file=sys.stderr)
            sys.exit(1)
        # 空間の範囲
        self.x_lim = (0, x)          # 大きな値を設定した場合, gridで塗りつぶされる & 細かい動きが見えなくなる. 
        self.y_lim = (0, y)


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
        super().__init__(options["x_lim"], options["y_lim"])       # スーパークラス
        
        self.scr = turtle.Screen()
        x_mg = (self.x_lim[1] - self.x_lim[0]) // 10
        y_mg = (self.y_lim[1] - self.y_lim[0]) // 10
        turtle.setworldcoordinates(self.x_lim[0]-x_mg, self.y_lim[1]+y_mg, self.x_lim[1]+x_mg, self.y_lim[0]-y_mg)      # 画面のサイズを指定

        self.FeedsAlgo = options[FEEDS_ALGO]                 # 餌のアルゴリズム
        self.TurtlesAlgo = options[TURTLE_ALGO]              # 亀のアルゴリズム
        self.delay = options[DELAY] / 1000
        self.Options = options

        self.__wall()                               # 壁の描写
        if options[GRID]:                           # grid
            self.__grid()

        self.init_colors()
        
        self.Feeds = [Feed(x, y, options) for (x, y) in feeds]                   # 指定座標に餌を配置
        self.Turtles = [Turtle(x, y, options) for (x, y) in turtles]             # 指定座標に亀を配置

        
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
        if self.Options["x_lim"] % self.Options["sep"] != 0 or self.Options["y_lim"] %  self.Options["sep"] != 0:
            print("WARNING! : x or y can't div by sep.", file=sys.stderr)

        x_stride = self.Options["x_lim"] / self.Options["sep"]           # 描写幅 
        y_stride = self.Options["y_lim"] / self.Options["sep"]          

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

        while V.xcor() + x_stride < self.x_lim[1] or H.ycor() + y_stride < self.y_lim[1]:
            if V.xcor() + x_stride < self.x_lim[1]:         # 垂直方向の描写
                V.setx(V.xcor() + x_stride)           # 右へ1マス移動
                V.pendown()
                V.sety(self.y_lim[1])            # 下向きに線を引いて上へ戻す
                V.penup()
                V.sety(self.y_lim[0])

            if H.ycor() + y_stride < self.y_lim[1]:         # 水平方向の描写
                H.sety(H.ycor() + y_stride)
                H.pendown()
                H.setx(self.x_lim[1])
                H.penup()
                H.setx(self.x_lim[0])

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
        for i in self.Feeds:
            i.run(algo=self.FeedsAlgo, option=self.Options)
            i.draw_border()

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
        super().__init__(op["x_lim"], op["y_lim"])

        if self.x_lim[0] <= x <= self.x_lim[1] :       # 餌がFeald内に収まっているかの確認
            pass
        else:
            print("ERROR: invalid x position", file=sys.stderr)
            sys.exit(1)

        if self.y_lim[0] <= y <= self.y_lim[1]:
            pass
        else:
            print("ERROR: invalid y position", file=sys.stderr)
            sys.exit(1)

        self.Feed = turtle.Turtle()         # 餌の本体
        self.circler = turtle.Turtle()      # 円を描くオブジェクト
        self.Options = op

        # 餌の初期化
        self.Feed.shape("circle")
        self.Feed.color("Red")
        self.Feed.hideturtle()
        self.Feed.penup()
        self.Feed.setpos(x, y)
        self.Feed.pendown()
        self.Feed.showturtle()

        # 円を描くオブジェクトの初期化
        self.circler.color("Red")
        self.circler.hideturtle()

        # 初回の描写
        self.circler.penup()
        self.circler.setpos(x, y-op["sight"])
        self.circler.pendown()
        if op["DistanceFunction"] == "Euclidean":
            self.circler.circle(radius=op["sight"])
        elif op["DistanceFunction"] == "Manhattan":
            self.circler.circle(radius=op["sight"], steps=4)
        else:
            print("Undefined distance function", file=sys.stderr)
            sys.exit()



    def draw_border(self):
        op = self.Options
        x, y = self.Feed.pos()
        self.circler.clear()

        if self.Options["Turtle_algo"].__name__ == "HaveNose":
            self.circler.penup()
            self.circler.setpos(x, y-op["sight"])
            self.circler.pendown()
            if op["DistanceFunction"] == "Euclidean":
                self.circler.circle(radius=op["sight"])
            elif op["DistanceFunction"] == "Manhattan":
                self.circler.circle(radius=op["sight"], steps=4)
            else:
                print("Undefined distance function", file=sys.stderr)
                sys.exit()


    def run(self, algo:Move, option):
        if algo.__name__ == "stay":     # stayの対応
            return

        x = [(True, 1), (False, 1), (True, -1), (False, -1)]        # True->水平, False->垂直
        flag = False
        # 壁のチェック
        while not flag:                                             # 壁のない方向が出るまで繰り返す
            direction = algo(T=self.Feed, option=option)               
            if x[direction][0]:
                flag = self.x_lim[0] <= self.Feed.xcor() + x[direction][1] <= self.x_lim[1]
            else:
                flag = self.y_lim[0] <= self.Feed.ycor() + x[direction][1] <= self.y_lim[1]


        # self.T.setheading(direction * 90)   # 頭の方向を決めて前進 -> 誤差の原因
        # self.T.forward(1)                  
        # print("座標:{}, 角度:{}".format(self.T.pos(), self.T.heading()))
        next_pos = tuple(map(add, self.Feed.pos(), MOVE[direction]))       # 移動先の座標を計算
        self.Feed.setpos(next_pos)                                         # 指定座標へ移動





"""
亀クラス
"""
class Turtle(Law):
    def __init__(self, x:int, y:int, op) -> None:
        super().__init__(op["x_lim"], op["y_lim"])
        if self.x_lim[0] <= x <= self.x_lim[1]:       # 餌がFeald内に収まっているかの確認
            pass
        else:
            print("ERROR: invalid x position", file=sys.stderr)
            sys.exit(1)

        if self.y_lim[0] <= y <= self.y_lim[1]:
            pass
        else:
            print("ERROR: invalid y position", file=sys.stderr)
            sys.exit(1)

        # config
        self.T = turtle.Turtle()
        self.T.speed(speed=op[SPEED])
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
        if algo.__name__ == "stay":     # stayの対応
            return

        x = [(True, 1), (False, 1), (True, -1), (False, -1)]        # True->水平, False->垂直
        flag = False
        # 壁のチェック
        while not flag:                                             # 壁のない方向が出るまで繰り返す
            direction = algo(T=self.T, option=option)               
            if x[direction][0]:
                flag = self.x_lim[0] <= self.T.xcor() + x[direction][1] <= self.x_lim[1]
            else:
                flag = self.y_lim[0] <= self.T.ycor() + x[direction][1] <= self.y_lim[1]


        # self.T.setheading(direction * 90)   # 頭の方向を決めて前進 -> 誤差の原因
        # self.T.forward(1)                  
        # print("座標:{}, 角度:{}".format(self.T.pos(), self.T.heading()))
        next_pos = tuple(map(add, self.T.pos(), MOVE[direction]))       # 移動先の座標を計算
        self.T.setpos(next_pos)                                         # 指定座標へ移動




