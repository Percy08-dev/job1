# 説明書
## 実行方法
- exeファイルの場合
    
    ダブルクリックで実行できます. 
    ただし, srcディレクトリに属するファイルに対する変更は適用されません. 
    
    -> ファイルを動的に追加できる性質上exe化できない. 
    -> execを使えば行けるか？

- Pythonインタープリタから実行する場合
    
    付属の.batファイルを実行することで実行できます. 
    自身の環境に, Pythonをインストールする必要があります. 
    Python 3.8.10 で作成した為, 同様のPython を使用する事を推奨します. 
    下記のサイトにPythonの環境構築方法が記されています.  
    https://www.python.jp/install/windows/install.html  
    
    コマンドプロンプトやPowerShellの様なコマンドラインから実行する場合は, 
    cdを用いてsrcディレクトリを移動した後, 下記のコマンドを実行する事で実行可能です. "ファイル名"の部分を実際のファイル名 
    ```
    Python MasterWindow.py
    ```

## ディレクトリ構成
```
.
├── UserFile        -> 自身で作成したファイルを置くディレクトリ
│   └── test.py  
├── readme.md  
└── src                     -> 今回作成したソースコードが置かれたディレクトリ
    ├── MasterWindow.py     -> メインプログラム  
    ├── __pycache__         -> ※1 
    │   ├── T.cpython-38.pyc
    │   ├── move.cpython-38.pyc
    │   ├── object.cpython-38.pyc
    │   └── test.cpython-38.pyc
    ├── lib                 -> サブプログラムの置かれたディレクトリ
    │   ├── __pycache__     -> ※1
    │   │   ├── move.cpython-38.pyc
    │   │   ├── normalize_path.cpython-38.pyc
    │   │   └── object.cpython-38.pyc
    │   ├── move.py             -> 亀や餌の動き方について記述されたファイル
    │   ├── normalize_path.py   
    │   └── object.py           -> 画面, 亀, 餌に関するファイル
    └── test.py
```
※1 Pythonが実行時に作成したファイル群. 各種ファイルのコンパイルされたものが格納されている. 

## 記述方法
作成したファイルはmain関数が実行される. 


## ソースコードの解説

