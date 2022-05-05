import turtle
import sys
from typing import List

from move import Move

# 定数
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3




"""
法則
"""
class Law:
    # 空間の範囲
    x_lim = (0, 1_000)          # 大きな値を設定した場合, gridで塗りつぶされる & 細かい動きが見えなくなる. 
    y_lim = (0, 1_000)

    # マージン, 餌と亀を設置できる範囲を壁からの距離で設定, 行動回数 < マージンとすることで実質無限の空間. 
    # とりあえず未使用
    margin = 0



"""
空間
"""
class Feald(Law):
    scr = turtle.Screen()
    turtle.setworldcoordinates(Law.x_lim[0], Law.y_lim[1], Law.x_lim[1], Law.y_lim[0])
    
    Feeds = []
    Turtles = []
    
    FeedsAlgo = None
    TurtlesAlgo = None


    def __init__(self, feeds:List[tuple], turtles:List[tuple], feeds_algo = Move.stay, turtle_algo = Move.RandomWalk, speed = 3, delay=1, grid=True) -> None:
        self.Feeds = [Feed(x, y) for (x, y) in feeds]                   # 指定座標に餌を配置
        self.Turtles = [Turtle(x, y, speed) for (x, y) in turtles]             # 指定座標に亀を配置
        self.FeedsAlgo = feeds_algo                 # 餌のアルゴリズム
        self.TurtlesAlgo = turtle_algo              # 亀のアルゴリズム

        self._wall()                                # 壁の描写
        if grid:
            self._grid()
        
        turtle.delay(delay)                         # 遅延をms単位で指定


    def _wall(self):                                # 壁
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
        del tmp


    def _grid(self):
        color = (0.8, 0.8, 0.8)     # RGB
        V = turtle.Turtle()         # 垂直方向
        H = turtle.Turtle()         # 水平方向

        V.hideturtle()              # コンフィグ
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

        while V.xcor() +10 < Law.x_lim[1] or H.ycor() + 10 < Law.y_lim[1]:
            if V.xcor() + 10 < Law.x_lim[1]:         # 垂直方向の描写
                V.setx(V.xcor() + 10)           # 右へ1マス移動
                V.pendown()
                V.sety(Law.y_lim[1])            # 下向きに線を引いて上へ戻す
                V.penup()
                V.sety(Law.y_lim[0])

            if H.ycor() + 10 < Law.y_lim[1]:         # 水平方向の描写
                H.sety(H.ycor() + 10)
                H.pendown()
                H.setx(Law.x_lim[1])
                H.penup()
                H.setx(Law.x_lim[0])


        del V
        del H


    def play(self):             # 1ターン進める
        for i in self.Turtles:
            i.run(algo=self.TurtlesAlgo)


    def eat_check(self):        # 餌と亀が重なっているかを確認
        pass


    def end_check(self):        # 餌が残っているか確認
        pass


"""
餌クラス
今のところ、目標物
"""
class Feed(Law):             
    def __init__(self, x:int, y:int) -> None:
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

        self.Feed = turtle.Turtle()
        self.Feed.penup()
        self.Feed.setpos(x, y)
        self.Feed.pendown()



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

        self.T = turtle.Turtle()
        self.T.speed(speed=speed)
        self.T.width(2)

        self.T.penup()
        self.T.setpos(x, y)
        self.T.pendown()


    def run(self, algo:Move):
        direction = algo()
        self.T.setheading(direction * 90)
        self.T.forward(10)                  # 1では動きがよくわからない, 1pxの移動？










feed = []
t = [(100, 100), (900, 900)]

turtle.delay(1)

x = Feald(feeds=feed, turtles=t, speed=0)

for i in range(1000):
    x.play()



input()