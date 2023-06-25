import tkinter as tk
import pygame

def bofangqi(path):
    global v
    root = tk.Toplevel()
    root.title("音乐播放器")
    root['background']='white'
    root.iconbitmap(r'media\\Hitubiao.ico')
    root.title('Hi音乐播放器v0.5')
    root.resizable(width=False,height=False)
    image_=tk.PhotoImage(file=r'media\bofangqi.png')
    cavans=tk.Canvas(root,bg='white')
    cavans.place(x=0,y=0)
    cavans.create_image(100,50,image = image_)

    v=0.5
    def play():

        pygame.mixer.init()
        pygame.mixer.music.load(path)  # 加载本地文件
        pygame.mixer.music.set_volume(v)
        pygame.mixer.music.play()  # 播放音乐


    def stop():
        pygame.mixer.music.pause() # 停止音乐


    def bofang():

        play()  # 随机播放


    def next_song():  # 下一首
        pygame.mixer.music.unpause()

    def last_song():  # 上一首
        global v
        if v==1:
            return
        v +=0.1
        pygame.mixer.music.set_volume(v)

    def jian():
        global v
        if v == 0:
            return
        v -= 0.1
        pygame.mixer.music.set_volume(v)


    b1 =tk.Button(root, text="+音量", width=10, command=last_song,bg='pink',relief='solid')
    b1.grid(row=0, column=0, padx=10, pady=10)

    b2 = tk.Button(root, text="继续", width=10, command=next_song,bg='pink',relief='solid')
    b2.grid(row=0, column=1, padx=10, pady=10)

    b3 =tk.Button(root, text="-音量", width=10, command=jian,bg='pink',relief='solid')
    b3.grid(row=0, column=2, padx=10, pady=10)

    b4 = tk.Button(root, text="停止", width=20, command=stop,bg='pink',relief='solid')
    b4.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

    b5 = tk.Button(root, text="开始", width=20, command=bofang,bg='pink',relief='solid')
    b5.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
    root.mainloop()
    print('已经执行完毕')

path = 'E:\projects\comper_lungher\project\love music\Red(Rob Simonsen).mp3'
bofangqi(path)