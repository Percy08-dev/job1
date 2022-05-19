from tkinter import *
from tkinter.tix import IMAGE
import turtle
import glob
import os
import pathlib
import sys
from tkinter import Canvas

tmppath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../UserFile"))        # 下位ディレクトリのファイルの追加
sys.path.append(tmppath)


from lib.normalize_path import AbsPath


# 定数
STARTUP = 1
READY = 2
RUNNING = 3
DONE = 4
EVENTDRIVEN = 5

# 
menufont = ("Arial", 12, NORMAL)
btnfont = ("Arial", 12, 'bold')
txtfont = ['Lucida Console', 10, 'normal']


class MasterWindow(object):
    
    def __init__(self):
        self.main_window = main_window =  Tk()                      # 主windowの生成
        main_window.title = "Simulator"                             # タイトル  
        main_window.wm_protocol("WM_DELETE_WINDOW", self._destroy)  # 終了動作

        
        main_window.grid_rowconfigure(0, weight=1)
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_columnconfigure(1, minsize=90, weight=1)
        main_window.grid_columnconfigure(2, minsize=90, weight=1)
        main_window.grid_columnconfigure(3, minsize=90, weight=1)


        self.MenuBar = Menu(main_window, relief=RAISED, borderwidth=2)
        self.MenuBar.add_cascade(label="File", menu=self.__makeFileMenu(self.MenuBar), underline=0)                      # メニューバーの項目を作る
        # self.MenuBar.add_cascade(label="scale", menu=self.__makeScale(self.MenuBar), underline=0)                         # 内部未実装

        main_window["menu"] = self.MenuBar

        pane = PanedWindow(orient=HORIZONTAL, sashwidth=5, sashrelief=SOLID, bg = "#ddd")   # 画面作成
        pane.add(self.__makeGraphFrame(pane))
        pane.grid(row=0, columnspan=4, sticky="ns")

        self.output_lbl = Label(main_window, height= 1, text=" --- ", bg="#ddf",            # ??
                                font=("Arial", 16, 'normal'), borderwidth=2,
                                relief=RIDGE)

        
        self.start_btn = Button(main_window, text=" START ", font=btnfont,
                                fg="white", disabledforeground = "#fed",
                                background="black", command=self.startSM)
        self.stop_btn = Button(main_window, text=" STOP ", font=btnfont,
                                fg="white", disabledforeground = "#fed",
                                background="black", command=self.stopIt)
        self.clear_btn = Button(main_window, text=" CLEAR ", font=btnfont,
                                fg="white", disabledforeground="#fed",
                                background="black", command = self.clearCanvas)
        
        self.output_lbl.grid(row=1, column=0, sticky='news', padx=(0,5))
        self.start_btn.grid(row=1, column=1, sticky='ew')
        self.stop_btn.grid(row=1, column=2, sticky='ew')
        self.clear_btn.grid(row=1, column=3, sticky='ew')

        self.__configGUI(DISABLED, DISABLED, DISABLED, "Choose example from menu", "black")

        self.dirty = False          # clearが必要かのフラグ
        self.exitflag = False


    def __makeFileMenu(self, master):
        menu = Menu(master)

        # ファイルリスト

        file_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../UserFile/*.py"))
        for path in glob.glob(file_path):
            if os.path.basename(path) == os.path.basename(__file__):
                continue
            def load(path=path):
                self.loadfile(path)
            label = os.path.basename(path)
            menu.add_command(label=label, underline=0, font=menufont, command=load)

        # 他
        menu.add_separator()
        # menu.add_command(label="Save PNG", command=self.__png, font=menufont)
        # menu.add_separator()
        menu.add_command(label="Exit", command=self.main_window.quit, font=menufont)

        return menu


    def loadfile(self, path):
        self.clearCanvas()
        turtle.TurtleScreen._RUNNING = False
        mod_name = pathlib.Path(path).stem
        # mod_name = "UserFile." + mod_name
        __import__(mod_name)
        self.module = sys.modules[mod_name]
        self.state = READY

    
    def __png(self):        # タートルグラフィックスの画面をpng形式で保存
        """
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "./test.eps"))
        cv = turtle.getcanvas()                     # Canvasを受け取る
        ps = cv.postscript(colormode="color")       # Canvasからpostscriptを生成
        mem = StringIO(ps)                          # インメモリ(メモリ上にファイルを置く)
        img = Image.open(mem)                       # メモリ上のファイルを開く
        # goast script以外でpostscriptを描写する方法がなさそうで頓挫
        """
        pass


    def __makeScale(self, master):
        menu = Menu(master, tearoff=0)
        menu.add_command(label = "zoom in", command=self.__zoom_in, font=menufont)
        menu.add_command(label = "zoom out", command=self.__zoom_out, font=menufont)
        return menu

    def __zoom_in(self):
        pass

    def __zoom_out(self):
        pass

    
    def __makeGraphFrame(self, root):
        turtle._Screen._root = root
        self.canvwidth = 1000
        self.canvheight = 800
        turtle._Screen._canvas = self._canvas = canvas = turtle.ScrolledCanvas(
            root, 800, 600, self.canvwidth, self.canvheight
        )
        canvas.adjustScrolls()
        canvas._rootwindow.bind('<Configure>', self.__onResize)
        canvas._canvas['borderwidth'] = 0

        self.screen = _s_ = turtle.Screen()
        turtle.TurtleScreen.__init__(_s_, _s_._canvas)
        self.scanvas = _s_._canvas
        turtle.RawTurtle.screens = [_s_]
        return canvas

    def __onResize(self, event):
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        self._canvas.xview_moveto(1*(self.canvwidth-cwidth)/self.canvwidth)
        self._canvas.yview_moveto(1*(self.canvheight-cheight)/self.canvheight)


    def startSM(self):
        self.refreshCanvas()
        self.dirty = True
        turtle.TurtleScreen._RUNNING = True
        self.__configGUI(DISABLED, NORMAL, DISABLED, "running...", "black")
        self.screen.clear()
        self.state = RUNNING

        # ここで作成したコードを動かす
        try:
            result = self.module.main()
            if result == "EVENTLOOP":
                self.state = EVENTDRIVEN
            else:
                self.state = DONE
        except turtle.Terminator:
            if self.main_window is None:
                return
            self.state = DONE
            result = "stopped!"
        if self.state == DONE:
            self.__configGUI(NORMAL, DISABLED, NORMAL, result)
        elif self.state == EVENTDRIVEN:
            self.exitflag = True
            self.__configGUI(DISABLED, NORMAL, DISABLED, "use mouse/keys or STOP", "red")


    def stopIt(self):
        if self.exitflag:
            self.clearCanvas()
            self.exitflag = False
            self.__configGUI(NORMAL, DISABLED, DISABLED, "STOPPED!", "red")
        turtle.TurtleScreen._RUNNING = False


    def clearCanvas(self):
        self.refreshCanvas()
        self.screen._delete("all")
        self.scanvas.config(cursor="")
        self.__configGUI(NORMAL, DISABLED, DISABLED)

    def refreshCanvas(self):
        if self.dirty:
            self.screen.clear()
            self.dirty=False
    

    def __configGUI(self, start, stop, clear, txt="", color="blue"):
        self.start_btn.config(state=start, bg="#d00" if start == NORMAL else "#fca")
        self.stop_btn.config(state=stop, bg="#d00" if stop == NORMAL else "#fca")
        self.clear_btn.config(state=clear, bg="#d00" if clear == NORMAL else "#fca")
        self.output_lbl.config(text=txt, fg=color)



    def _destroy(self):
        turtle.TurtleScreen._RUNNING = False
        self.main_window.destroy()
        self.main_window = None




def test():
    demo = MasterWindow()
    demo.main_window.mainloop()

if __name__ == "__main__":
    test()
