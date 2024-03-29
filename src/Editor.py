import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Entry, StringVar, messagebox, filedialog

import re
import os


FONT_SIZE = 20


class TG_Options:
    def __init__(self) -> None:
        self.reset()

    def insert(self, feeld, value):
        pre_order = "type(value) == str"
        flag = eval(pre_order)
        order = "self.{} < \"{}\"".format(feeld, value) if flag else "self.{} < {}".format(feeld, value)
        exec(order)

    def fill_check(self):
        tmp = [
            len(self.Feed_Points) == 0,
            len(self.Turtle_Points) == 0,
            self.xlim.is_none(), 
            self.ylim.is_none(),
            self.grid_sep.is_none(),
            self.Feeds_algo.is_none(), 
            self.Turtle_algo.is_none(), 
            self.DistanceFunction.is_none(), 
            self.sight.is_none(), 
            self.Speed.is_none(), 
            self.Delay.is_none(), 
            self.Grid.is_none(), 
            self.max_loop.is_none()
        ]

        return any(tmp)

    def reset(self):
        # 座標
        self.Feed_Points = []
        self.Turtle_Points =[]

        # 範囲
        self.xlim = Py_Option(int)
        self.ylim = Py_Option(int)
        self.grid_sep = Py_Option(int)

        # 移動
        self.Feeds_algo = Py_Option(str)
        self.Turtle_algo = Py_Option(str)

        # 距離
        self.DistanceFunction = Py_Option(str)
        self.sight = Py_Option(int)

        # 移動速度
        self.Speed = Py_Option(int)
        self.Delay = Py_Option(int)

        # グリッド
        self.Grid = Py_Option(bool)

        # 行動回数
        self.max_loop = Py_Option(int)
    
    def print(self):
        print("Feeds:{}".format(self.Feed_Points))
        print("Turtle:{}".format(self.Turtle_Points))
        print("xlim:{}".format(self.xlim.unwrap_or(None)))
        print("ylim:{}".format(self.ylim.unwrap_or(None)))
        print("grid_sep:{}".format(self.grid_sep.unwrap_or(None)))
        print("Feeds_algo:{}".format(self.Feeds_algo.unwrap_or(None)))
        print("Turtle_algo:{}".format(self.Turtle_algo.unwrap_or(None)))
        print("DistanceFunction:{}".format(self.DistanceFunction.unwrap_or(None)))
        print("sight:{}".format(self.sight.unwrap_or(None)))
        print("Speed:{}".format(self.Speed.unwrap_or(None)))
        print("Delay:{}".format(self.Delay.unwrap_or(None)))
        print("Grid:{}".format(self.Grid.unwrap_or(None)))
        print("max_loop:{}".format(self.max_loop.unwrap_or(None)))
        print()


class Py_Option:
    def __init__(self, value_type, value = None) -> None:
        if not(value == None or type(value) == value_type):
            raise TypeError("define type={}, Input Value Type={}".format(value_type, type(value)))
        self.__type = value_type
        self.__value = value
    
    def unwrap(self):
        if self.__value == None:
            raise ValueError("Value is None")
        return self.__value

    def unwrap_or(self, value):
        if self.__value == None:
            return value
        else:
            return self.__value
    
    def is_none(self):
        return self.__value == None

    def value_type(self):
        return self.__type

    def __lt__(self, new_value):    # 値の代入 -> x < 10
        if self.__type != type(new_value):
            raise ValueError("new value type is wrong type")

        self.__value = new_value



def make_label(frame):
    ### 1列目
    # 餌 座標       (基準)
    lbl_Feed_points = ttk.Label(frame, text='餌の座標', font=("Helvetica", FONT_SIZE))
    lbl_Feed_points.grid(row=1, column=0)
    ref_lbl_Feed_points = lbl_Feed_points.grid_info()       # 相対位置指定用
    # 亀 座標
    lbl_turtle_points = ttk.Label(frame, text='亀の座標', font=("Helvetica", FONT_SIZE))
    lbl_turtle_points.grid(row=ref_lbl_Feed_points["row"] + 1, column=ref_lbl_Feed_points["column"])
    ref_lbl_turtle_points = lbl_turtle_points.grid_info()

    ## 領域
    # x
    lbl_xlim = ttk.Label(frame, text='横幅', font=("Helvetica", FONT_SIZE))
    lbl_xlim.grid(row=ref_lbl_turtle_points["row"] + 1, column=ref_lbl_turtle_points["column"])
    ref_lbl_xlim = lbl_xlim.grid_info()
    # y
    lbl_ylim = ttk.Label(frame, text='縦幅', font=("Helvetica", FONT_SIZE))
    lbl_ylim.grid(row=ref_lbl_xlim["row"] + 1, column=ref_lbl_xlim["column"])
    ref_lbl_ylim = lbl_ylim.grid_info()

    # 分割数
    lbl_grid_sep = ttk.Label(frame, text='分割間隔', font=("Helvetica", FONT_SIZE))
    lbl_grid_sep.grid(row=ref_lbl_ylim["row"] + 1, column=ref_lbl_ylim["column"])
    ref_lbl_grid_sep = lbl_grid_sep.grid_info()

    ##移動アルゴ
    # 餌移動
    lbl_feed = ttk.Label(frame, text='餌移動アルゴリズム', font=("Helvetica", FONT_SIZE))
    lbl_feed.grid(row=ref_lbl_grid_sep["row"] + 1, column=ref_lbl_grid_sep["column"])
    ref_lbl_feed = lbl_feed.grid_info()

    # 亀移動
    lbl_turtle = ttk.Label(frame, text='亀移動アルゴリズム', font=("Helvetica", FONT_SIZE))
    lbl_turtle.grid(row=ref_lbl_feed["row"] + 1, column=ref_lbl_feed["column"])
    ref_lbl_turtle = lbl_turtle.grid_info()

    ## 距離関係
    # 距離関数
    lbl_dist = ttk.Label(frame, text='距離計算方法', font=("Helvetica", FONT_SIZE))
    lbl_dist.grid(row=ref_lbl_turtle["row"] + 1, column=ref_lbl_turtle["column"])
    ref_lbl_dist = lbl_dist.grid_info()

    # 視界
    lbl_sight = ttk.Label(frame, text='匂いのする距離', font=("Helvetica", FONT_SIZE))
    lbl_sight.grid(row=ref_lbl_dist["row"] + 1, column=ref_lbl_dist["column"])
    ref_lbl_sight = lbl_sight.grid_info()

    ## 移動速度
    # 速度
    lbl_speed = ttk.Label(frame, text='速度', font=("Helvetica", FONT_SIZE))
    lbl_speed.grid(row=ref_lbl_sight["row"] + 1, column=ref_lbl_sight["column"])
    ref_lbl_speed = lbl_speed.grid_info()

    # 遅延
    lbl_delay = ttk.Label(frame, text='遅延', font=("Helvetica", FONT_SIZE))
    lbl_delay.grid(row=ref_lbl_speed["row"] + 1, column=ref_lbl_speed["column"])
    ref_lbl_delay = lbl_delay.grid_info()

    ## グリッド
    # 亀移動
    lbl_grid = ttk.Label(frame, text='グリッドの有無', font=("Helvetica", FONT_SIZE))
    lbl_grid.grid(row=ref_lbl_delay["row"] + 1, column=ref_lbl_delay["column"])
    ref_lbl_grid = lbl_grid.grid_info()

    ## 行動回数
    # 行動回数
    lbl_looplim = ttk.Label(frame, text='行動回数上限(-1=無制限)', font=("Helvetica", FONT_SIZE))
    lbl_looplim.grid(row=ref_lbl_grid["row"] + 1, column=ref_lbl_grid["column"])
    ref_lbl_looplim = lbl_looplim.grid_info()

    ## 保存先
    lbl_save = ttk.Label(frame, text='保存ファイル名', font=("Helvetica", FONT_SIZE))
    lbl_save.grid(row=ref_lbl_looplim["row"] + 1, column=ref_lbl_looplim["column"])


    ### 3列目(単位等)
    # 餌 座標
    lbl_f_c3 = ttk.Label(frame, text='x=', font=("Helvetica", FONT_SIZE))
    lbl_f_c3.grid(row=ref_lbl_Feed_points["row"], column=ref_lbl_Feed_points["column"] + 2, sticky=tk.E)
    lbl_f_c5 = ttk.Label(frame, text='y=', font=("Helvetica", FONT_SIZE))
    lbl_f_c5.grid(row=ref_lbl_Feed_points["row"], column=ref_lbl_Feed_points["column"] + 4, sticky=tk.E)
    # 亀 座標
    lbl_t_c3 = ttk.Label(frame, text='x=', font=("Helvetica", FONT_SIZE))
    lbl_t_c3.grid(row=ref_lbl_turtle_points["row"], column=ref_lbl_turtle_points["column"] + 2, sticky=tk.E)
    lbl_t_c5 = ttk.Label(frame, text='y=', font=("Helvetica", FONT_SIZE))
    lbl_t_c5.grid(row=ref_lbl_turtle_points["row"], column=ref_lbl_turtle_points["column"] + 4, sticky=tk.E)

    ## 領域
    # x
    lbl_x_description = ttk.Label(frame, text='マス', font=("Helvetica", FONT_SIZE))
    lbl_x_description.grid(row=ref_lbl_xlim["row"], column=ref_lbl_xlim["column"] + 2, sticky=tk.W)
    # y
    lbl_y_description = ttk.Label(frame, text='マス', font=("Helvetica", FONT_SIZE))
    lbl_y_description.grid(row=ref_lbl_ylim["row"], column=ref_lbl_xlim["column"] + 2, sticky=tk.W)
    # 分割
    lbl_grid_sep_description =  ttk.Label(frame, text='マス', font=("Helvetica", FONT_SIZE))
    lbl_grid_sep_description.grid(row=ref_lbl_grid_sep["row"], column=ref_lbl_grid_sep["column"] + 2, sticky=tk.W)

    # 視界
    lbl_sight_description = ttk.Label(frame, text='マス', font=("Helvetica", FONT_SIZE))
    lbl_sight_description.grid(row=ref_lbl_sight["row"], column=ref_lbl_sight["column"] + 2, sticky=tk.W)

    # 速度
    # lbl_speed_description = ttk.Label(frame, text='(速い) 0 -> 10 -> 9 -> ... -> 2 -> 1 (遅い)', font=("Helvetica", FONT_SIZE))
    # lbl_speed_description.grid(row=9, column=2, sticky=tk.W)

    # 視界
    lbl_delay_description = ttk.Label(frame, text='ms', font=("Helvetica", FONT_SIZE))
    lbl_delay_description.grid(row=ref_lbl_delay["row"], column=ref_lbl_delay["column"] + 2, sticky=tk.W)

    # 最大回数
    lbl_maxmove_description = ttk.Label(frame, text='回', font=("Helvetica", FONT_SIZE))
    lbl_maxmove_description.grid(row=ref_lbl_looplim["row"], column=ref_lbl_looplim["column"] + 2, sticky=tk.W)

# 座標選択時に入力欄を連動
def select_point(points:list, var:StringVar, input_area_x:Entry, input_area_y:Entry):
    now = var.get()
    now = now[1:-1].split(", ")     # parse
    input_area_x.delete(0, tk.END)  # 初期化
    input_area_x.insert(0, now[0])
    input_area_y.delete(0, tk.END)  # 初期化
    input_area_y.insert(0, now[1])

# 追加
def add_new_point(frame, point_list:list, input_area_x:Entry, input_area_y:Entry, cb:ttk.Combobox, row, col):
    fmt = "({}, {})"
    x = input_area_x.get()
    y = input_area_y.get()

    if x.replace("-", "") == "" or y.replace("-", "") == "":
        return

    point = fmt.format(x, y)
    point_list.append(point)

    cb.destroy()            # 元々の入力欄を削除
    cb = ttk.Combobox(frame, textvariable=tk.StringVar(), values=point_list, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    cb.grid(row=row, column=col)
    cb.current(len(point_list) - 1)     # 新しい要素の位置

# 削除
def rm_point(frame, point_list:list, input_area_x:Entry, input_area_y:Entry, cb:ttk.Combobox, row, col):
    fmt = "({}, {})"
    x = input_area_x.get()
    y = input_area_y.get()

    if x == "" or y == "":
        return
    
    point = fmt.format(x, y)
    if point in point_list:
        point_list.remove(point)
    else:
        messagebox.showerror("不正な値です。")
        return
    
    cb.destroy()            # 元々の入力欄を削除
    cb = ttk.Combobox(frame, textvariable=tk.StringVar(), values=point_list, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    cb.grid(row=row, column=col)
    cb.current(len(point_list) - 1)     # 新しい要素の位置



def make_input_area(frame, data:TG_Options):
    # ファイルオープン
    # open_btn = ttk.Button(frame, text="開く", command= lambda :read_file_open(frame))
    # open_btn.grid(row=0, column=1)

    ### 動くやつ
    ## 餌 座標
    point1_v = tk.StringVar()
    Feed_points = []    # "(x, y)"
    point1_cb = ttk.Combobox(frame, textvariable=point1_v, values=Feed_points, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    point1_cb.bind('<<ComboboxSelected>>', lambda e:select_point(Feed_points, point1_v, point1_x_input_area, point1_y_input_area, ref_point1_cb["row"], ref_point1_cb["column"]))
    point1_cb.grid(row=1, column=1)
    ref_point1_cb = point1_cb.grid_info()
    # 座標入力欄
    point1_x_input_area = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=6, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    point1_x_input_area.grid(row=ref_point1_cb["row"], column=ref_point1_cb["column"] + 2)
    point1_y_input_area = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=6, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    point1_y_input_area.grid(row=ref_point1_cb["row"], column=ref_point1_cb["column"] + 4)
    # 追加ボタン
    point1_add = ttk.Button(frame, text="追加", command=lambda: add_new_point(frame, Feed_points, point1_x_input_area, point1_y_input_area, point1_cb, ref_point1_cb["row"], ref_point1_cb["column"]))
    point1_add.grid(row=ref_point1_cb["row"], column=ref_point1_cb["column"] + 5)
    # 削除ボタン
    point1_rm = ttk.Button(frame, text="削除", command=lambda: rm_point(frame, Feed_points, point1_x_input_area, point1_y_input_area, point1_cb, row=ref_point1_cb["row"], col=ref_point1_cb["column"]))
    point1_rm.grid(row=ref_point1_cb["row"], column=ref_point1_cb["column"] + 6)

    ## 亀 座標
    point2_v = tk.StringVar()
    Turtle_points = []
    point2_cb = ttk.Combobox(frame, textvariable=point2_v, values=Turtle_points, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    point2_cb.bind('<<ComboboxSelected>>', lambda e:select_point(Turtle_points, point2_v, point2_x_input_area, point2_y_input_area))
    point2_cb.grid(row=ref_point1_cb["row"] + 1, column=ref_point1_cb["column"])
    ref_point2_cb = point2_cb.grid_info()
    # 座標入力欄
    point2_x_input_area = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=6, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    point2_x_input_area.grid(row=ref_point2_cb["row"], column=ref_point2_cb["column"] + 2)
    point2_y_input_area = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=6, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    point2_y_input_area.grid(row=ref_point2_cb["row"], column=ref_point2_cb["column"] + 4)
    # 追加ボタン
    point2_add = ttk.Button(frame, text="追加", command=lambda: add_new_point(frame, Turtle_points, point2_x_input_area, point2_y_input_area, point2_cb, ref_point2_cb["row"], ref_point2_cb["column"]))
    point2_add.grid(row=ref_point2_cb["row"], column=ref_point2_cb["column"] + 5)
    # 削除ボタン
    point2_rm = ttk.Button(frame, text="削除", command=lambda: rm_point(frame, Turtle_points, point2_x_input_area, point2_y_input_area, point2_cb, ref_point2_cb["row"], ref_point2_cb["column"]))
    point2_rm.grid(row=ref_point2_cb["row"], column=ref_point2_cb["column"] + 6)




    ## 範囲
    # x
    x_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    x_et.insert(0, 100)
    x_et.grid(row=ref_point2_cb["row"] + 1, column=ref_point2_cb["column"])
    ref_x_et = x_et.grid_info()
    # y
    y_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    y_et.insert(0, 100)
    y_et.grid(row=ref_x_et["row"] + 1, column=ref_x_et["column"])
    ref_y_et = y_et.grid_info()
    # grid sep
    grid_sep_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    grid_sep_et.insert(0, 10)
    grid_sep_et.grid(row=ref_y_et["row"] + 1, column=ref_y_et["column"])
    ref_grid_sep_et = grid_sep_et.grid_info()


    ##移動アルゴ
    move_choice = ("静止", "ランダムウォーク", "匂いを追う")
    # 餌移動
    move_v1 = tk.StringVar()
    move_cb1 = ttk.Combobox(frame, textvariable=move_v1, values=move_choice, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    move_cb1.bind('<<ComboboxSelected>>', lambda e:data.insert("Feeds_algo", move_v1.get()))
    move_cb1.grid(row=ref_grid_sep_et["row"] + 1, column=ref_grid_sep_et["column"])
    ref_move_cb1 = move_cb1.grid_info()
    # 亀移動
    move_v2 = tk.StringVar()
    move_cb2 = ttk.Combobox(frame, textvariable=move_v2, values=move_choice, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    move_cb2.bind('<<ComboboxSelected>>', lambda e:data.insert("Turtle_algo", move_v2.get()))
    move_cb2.grid(row=ref_move_cb1["row"] + 1, column=ref_move_cb1["column"])
    ref_move_cb2 = move_cb2.grid_info()

    ## 距離
    distance_choice = ("ユークリッド距離", "マンハッタン距離")
    # 距離関数
    dist_v1 = tk.StringVar()
    dist_cb1 = ttk.Combobox(frame, textvariable=dist_v1, values=distance_choice, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    dist_cb1.bind('<<ComboboxSelected>>', lambda e:data.insert("DistanceFunction", dist_v1.get()))
    dist_cb1.grid(row=ref_move_cb2["row"] + 1, column=ref_move_cb2["column"])
    ref_dist_cb1 = dist_cb1.grid_info()
    # 視界 数値入力制限付き 入力値を変数に入れる処理は最後に保存のボタンを押したときにする
    sight_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    sight_et.insert(0, 0)
    sight_et.grid(row=ref_dist_cb1["row"] + 1, column=ref_dist_cb1["column"])
    ref_sight_et = sight_et.grid_info()

    ## 移動速度
    # スピード
    speed_choice = ["0 (速い)"] + [str(i) for i in reversed(range(2, 11))] + ["1 (遅い)"]
    speed_table = {i:j for (i, j) in zip(speed_choice, [0] + [i for i in reversed(range(2, 11))] + [1])}        # 入力の変換用
    speed_v = tk.StringVar()
    speed_cb = ttk.Combobox(frame, textvariable=speed_v, values=speed_choice, width=16, height=12, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    speed_cb.bind('<<ComboboxSelected>>', lambda e:data.insert("Speed", int(speed_table[speed_v.get()])))
    speed_cb.grid(row=ref_sight_et["row"] + 1, column=ref_sight_et["column"])
    ref_speed_cb = speed_cb.grid_info()
    # 遅延
    delay_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    delay_et.insert(0, 0)
    delay_et.grid(row=ref_speed_cb["row"] + 1, column=ref_speed_cb["column"])
    ref_delay_et = delay_et.grid_info()

    ## グリッド
    grid_choice = (True, False)
    grid_v = tk.StringVar()
    grid_cb = ttk.Combobox(frame, textvariable=grid_v, values=grid_choice, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    grid_cb.bind('<<ComboboxSelected>>', lambda e:data.insert("Grid", bool(grid_v.get())))
    grid_cb.grid(row=ref_delay_et["row"] + 1, column=ref_delay_et["column"])
    ref_grid_cb = grid_cb.grid_info()

    ## 行動回数
    move_limit_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, validation_num), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    move_limit_et.insert(0, 0)
    move_limit_et.grid(row=ref_grid_cb["row"] + 1, column=ref_grid_cb["column"])
    ref_move_limit_et = move_limit_et.grid_info()

    ## file_name
    file_name_et = tk.Entry(frame, validate="key", validatecommand=(tk.Frame.register(frame, allowed_chars), "%P"), invalidcommand=None, width=16, font=("Helvetica", FONT_SIZE), justify=tk.RIGHT)
    file_name_et.grid(row=ref_move_limit_et["row"] + 1, column=ref_move_limit_et["column"])
    ref_file_name_et = file_name_et.grid_info()

    ## ファイル作成ボタン
    make_bt = ttk.Button(frame, text="保存", 
        command=lambda :file_make(
            file_name = file_name_et.get(), 
            Options = data, 
            Feed_points = Feed_points, 
            Turtle_points = Turtle_points, 
            xlim = int(x_et.get()), 
            ylim = int(y_et.get()),
            sep = int(grid_sep_et.get()), 
            sight = int(sight_et.get()), 
            delay = int(delay_et.get()), 
            move_limit = int(move_limit_et.get())
        )
    )
    make_bt.grid(row=ref_file_name_et["row"] + 1, column=ref_file_name_et["column"])
    ref_make_bt = make_bt.grid_info()

    # 実行ボタン
    run_btn = ttk.Button(frame, text="実行", command= lambda :run())
    run_btn.grid(row=ref_make_bt["row"] + 1, column=ref_make_bt["column"])


def run():
    os.system("Run")


def validation_num(s):
    # 数値以外の文字の検知
    return bool(re.fullmatch(re.compile('-?[0-9]*'), s))

def allowed_chars(s):
    return not bool(re.match(r'[\\|/|:|?|.|"|<|>|\|]', s))


def test_print_button(frame, data):
    bt = ttk.Button(frame, text="print", command=lambda :data.print())
    bt.grid(row=11, column=0)

def file_make(file_name, Options:TG_Options, Feed_points, Turtle_points, xlim, ylim, sep, sight, delay, move_limit):
    # 固定値
    output_file_path = "./UserFile/{}.py".format(file_name)
    file_overwrap_flag = True                  # 初回の実行をクリアと上書き警戒
    model_sorce_code_path = "./src/model.py"
    table = {       # 入力と出力の対応表
        "静止":"Move.stay", 
        "ランダムウォーク":"Move.RandomWalk", 
        "匂いを追う": "Move.HaveNose", 
        "ユークリッド距離":"Euclidean", 
        "マンハッタン距離":"Manhattan", 
        -1:"INF"
    }
    
    # 代入
    Options.Feed_Points = [(int(i[1:-1].split(",")[0]), int(i[1:-1].split(",")[1])) for i in Feed_points]
    Options.Turtle_Points = [(int(i[1:-1].split(",")[0]), int(i[1:-1].split(",")[1])) for i in Turtle_points]
    Options.insert("xlim", xlim)
    Options.insert("ylim", ylim)
    Options.insert("grid_sep", sep)
    Options.insert("sight", sight)
    Options.insert("Delay", delay)
    Options.insert("max_loop", move_limit)

    # 不正な座標の確認
    fp = [i for i in Options.Feed_Points if not(0 <= i[0] <= xlim) and not(0 <= i[1] <= ylim)]
    tp = [i for i in Options.Turtle_Points if not(0 <= i[0] <= xlim) and not(0 <= i[1] <= ylim)]
    if tp or fp:
        if messagebox.askyesno("範囲外に配置されたものがあります。", message="削除しますか？"):
            Options.Feed_Points = [i for i in Options.Feed_Points if 0 <= i[0] <= xlim and 0 <= i[1] <= ylim]
            Options.Turtle_Points = [i for i in Options.Turtle_Points if 0 <= i[0] <= xlim and 0 <= i[1] <= ylim]


    # ファイルの存在確認
    if os.path.exists(output_file_path):
        file_overwrap_flag = messagebox.askyesno("確認", "ファイルを上書きしますか？")
    
    # 上書きの許可が出たか
    if not file_overwrap_flag:
        return

    # 全ての項目が埋まっているか
    Options.print()
    if Options.fill_check():
        messagebox.showerror(title="Error", message="全ての項目を選択してください。")
        return

    with open(model_sorce_code_path, "r", encoding="utf-8") as f:
        model_sorce_code = f.read()

    # ソースコードの穴埋め
    model_sorce_code = model_sorce_code.format(
            Options.Feed_Points, 
            Options.Turtle_Points,
            Options.xlim.unwrap(), 
            Options.ylim.unwrap(), 
            Options.grid_sep.unwrap(), 
            table[Options.Feeds_algo.unwrap()], 
            table[Options.Turtle_algo.unwrap()], 
            table[Options.DistanceFunction.unwrap()], 
            Options.sight.unwrap(), 
            Options.Speed.unwrap(), 
            Options.Delay.unwrap(), 
            Options.Grid.unwrap(), 
            Options.max_loop.unwrap() if Options.max_loop.unwrap() != -1 else table[-1]
        )

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(model_sorce_code)

    messagebox.showinfo("完了", "保存が完了しました。")


def read_file_open(frame):
    path = "./UserFile/"
    typ = [("Python", "*.py")]
    file_path = filedialog.askopenfilename(filetypes=typ, initialdir=path)
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()
    # クリーニング部分
    txt = re.search("options = {.*}", src, re.DOTALL).group()
    txt = re.sub("#.*?\n", "\n", txt)
    txt = re.sub("Move(.*?),", "\"" + r"Move\1" + "\",", txt)
    txt = re.sub('"max-loop" : (.*?),', r'"max-loop" : "\1"', txt)
    txt = txt.replace("True", "true")
    txt = txt.replace("False", "false")
    txt = txt.replace("options = ", "")
    # 解析
    obj = json.loads(txt)
    
    tk_obj = frame.winfo_children()
    tk_obj = [i for i in tk_obj if i.grid_info()["column"] == 1][1:-1]
    tk_obj.sort(key=lambda x:x.grid_info()["row"])
    
    tk_obj[0].insert(0, obj["x_lim"])



def main():
    # 入力データ管理
    Options = TG_Options()

    # main window
    root = tk.Tk()  
    root.title("Edit")
    root.option_add("*TCombobox*Listbox.Font", FONT_SIZE)

    # main frame 
    frame = ttk.Frame(root)
    frame.pack(padx = 20, pady=20)

    ### 
    make_label(frame)                       # ラベル作成
    make_input_area(frame, Options)         # 入力欄作成 
    # test_print_button(frame, Options)       # デバッグ用

    root.state("zoomed")        # 全画面表示
    root.mainloop()

if __name__ == "__main__":
    main()