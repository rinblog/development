# -*- coding: UTF-8 -*-

import wx
import cv2
import os

# D&Dウィンドウクラス
class FileDropTarget(wx.FileDropTarget):
    """ Drag & Drop Class """
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    # DDされた画像のパスをimgComp(self, path)に渡す
    def OnDropFiles(self, x, y, files):
        self.window.pathList(files)
        return 0


class App(wx.Frame):
    """ GUI """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 400), style=wx.DEFAULT_FRAME_STYLE)

        # ファイルドロップエリア
        p = wx.Panel(self, wx.ID_ANY)
        label = wx.StaticText(p, wx.ID_ANY, 'ここにファイルをドロップしてください', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        label.SetBackgroundColour("#e0ffff")

        # ドロップ対象の設定
        label.SetDropTarget(FileDropTarget(self))

        # ログ表示エリア
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        self.text_entry = wx.TextCtrl(p, wx.ID_ANY, style = style)
        
        # レイアウト
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(label, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        layout.Add(self.text_entry, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        p.SetSizer(layout)

        self.Show()

    # 画像を保存する
    def imgWrite(self, compArray, decimg, name, ext):
        # 保存先フォルダ指定。なければ作る
        dir = os.getcwd()
        dir1 = dir + "/imgComp_output/圧縮画像比較用"
        if not os.path.exists(dir1):
            os.makedirs(dir1)

        dir2 = dir + "/imgComp_output/" + str(compArray)
        if not os.path.exists(dir2):
            os.makedirs(dir2)

        # 圧縮画像を保存
        fileName = name + "_" + str(compArray) + "." + ext
        cv2.imwrite(os.path.join(dir1, fileName), decimg)
        # 圧縮品質ごとに分けて保存
        fileName = name + "." + ext
        cv2.imwrite(os.path.join(dir2, fileName), decimg)
    
    # パスの画像を圧縮する
    def imgComp(self, path):
        # 入力画像の読み込み
        img = cv2.imread(path, -1)

        # jpg圧縮品質。高いほど高品質
        jpgArray = [90, 80, 70, 60, 50, 40, 10]
        # png圧縮率。値が大きいほどサイズが小さい。
        pngArray = [1, 2, 3, 7, 8 ,9]

        # ファイル名と拡張子を取得
        imgName = self.fileName(path)
        name, ext = imgName.split(".")

        if ext == "jpg" or ext == "jpeg":
            for i in range(len(jpgArray)):
                # 画像をメモリ上で圧縮
                result, encimg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), jpgArray[i]])

                # 圧縮されたメモリ上の画像を復元
                decimg = cv2.imdecode(encimg, -1)

                # jpg保存
                self.imgWrite(jpgArray[i], decimg, name, ext)
        
        elif ext == "png":
            for i in range(len(pngArray)):
                # 画像をメモリ上で圧縮
                result, encimg = cv2.imencode(".png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), pngArray[i]])

                # 圧縮されたメモリ上の画像を復元
                decimg = cv2.imdecode(encimg, -1)

                # png保存
                self.imgWrite(pngArray[i], decimg, name, ext)

        else:
            exit()
    
    # ファイル名と拡張子を取得
    def fileName(self, path):
        imgNameArray = path.split("/")
        imgName = imgNameArray[-1]
        return imgName
        
    # 受け取ったパスリストをループ処理
    def pathList(self, path):
        for i in range(len(path)):
            # 拡張子がjpgかpngかそれ以外を判定
            imgName = self.fileName(path[i])
            if ".jpg" in imgName or ".jpeg" in imgName or ".png" in imgName:
                self.imgComp(path[i])

                # ファイル名と拡張子を取得する。ログ表示用
                name, ext = imgName.split(".")
                self.text_entry.AppendText(name + "." + ext + " の圧縮成功\n")
            else:
                self.text_entry.AppendText(imgName + " は圧縮できないよ。pngかjpgをD&Dしてね。\n")
                pass



app = wx.App()
App(None, -1, "imgCompression")
app.MainLoop()
