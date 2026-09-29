
import tkinter as tk
import json
import math
import time
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PLAN CREATOR FULL")

        self.canvas = tk.Canvas(root, bg="#0f0f0f", width=1200, height=800)
        self.canvas.pack(fill="both", expand=True)

        self.shapes = []
        self.selected = []

        self.scale = 1.0

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        f = tk.Frame(self.root)
        f.pack()

        tk.Button(f, text="Circle", command=lambda: self.add("circle")).pack(side="left")
        tk.Button(f, text="Rect", command=lambda: self.add("rect")).pack(side="left")
        tk.Button(f, text="Triangle", command=lambda: self.add("tri")).pack(side="left")
        tk.Button(f, text="Bezier Connect", command=self.connect_bezier).pack(side="left")

    def bind_events(self):
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-3>", self.select)

    def add(self, t):
        x,y=200,200
        s=60
        if t=="circle":
            obj=self.canvas.create_oval(x,y,x+s,y+s,fill="cyan")
        elif t=="rect":
            obj=self.canvas.create_rectangle(x,y,x+s,y+s,fill="green")
        else:
            obj=self.canvas.create_polygon(x+30,y,x,y+60,x+60,y+60,fill="orange")
        self.shapes.append(obj)

    def center(self,o):
        c=self.canvas.coords(o)
        return ( (c[0]+c[2])/2,(c[1]+c[3])/2 )

    def connect_bezier(self):
        if len(self.selected)==2:
            x1,y1=self.center(self.selected[0])
            x2,y2=self.center(self.selected[1])
            mx=(x1+x2)/2
            line=self.canvas.create_line(x1,y1,mx,y1-100,mx,y2+100,x2,y2,smooth=True,fill="yellow",width=2)
            self.animate(line)
            self.text_path(x1,y1,x2,y2,"FLOW")
            self.selected=[]

    def text_path(self,x1,y1,x2,y2,t):
        dx=(x2-x1)/len(t)
        dy=(y2-y1)/len(t)
        for i,ch in enumerate(t):
            self.canvas.create_text(x1+dx*i,y1+dy*i,text=ch,fill="white")

    def animate(self,line):
        def run():
            for i in range(30):
                self.canvas.itemconfig(line,dash=(i,5))
                time.sleep(0.05)
        threading.Thread(target=run).start()

    def zoom(self,e):
        f=1.1 if e.delta>0 else 0.9
        self.scale*=f
        self.canvas.scale("all",e.x,e.y,f,f)

    def select(self,e):
        obj=self.canvas.find_closest(e.x,e.y)[0]
        self.selected.append(obj)
        if len(self.selected)>2:
            self.selected.pop(0)

root=tk.Tk()
App(root)
root.mainloop()
