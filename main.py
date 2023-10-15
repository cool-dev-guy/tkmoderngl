"""
code from moderngl/examples

modified by : cool-dev-guy
"""
import tkinter as tk

import moderngl
import numpy as np

from tkmoderngl.framebuffer import FramebufferImage
from tkmoderngl.renderer import Canvas, PanTool


# the moderngl widget
class GlWidget(tk.Label):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.parent = args[0]
        self._ctx = moderngl.create_standalone_context()
        self._tkfbo = FramebufferImage(args[0],self._ctx,(500,500))
        self._canvas = Canvas(self._ctx)
        self._pan_tool = PanTool()
        self.config(image=self._tkfbo)
    def context(self):
        return self._ctx
    def fbo(self):
        return self._tkfbo
    def canvas(self):
        return self._canvas
    def pan_tool(self):
        return self._pan_tool

# the vertives of the graph to be drawn
def vertices():
    x = np.linspace(-1.0, 1.0, 50)
    y = np.random.rand(50) - 0.5
    r = np.ones(50)
    g = np.zeros(50)
    b = np.zeros(50)
    a = np.ones(50)
    return np.dstack([x, y, r, g, b, a])
verts = vertices()
# --------------------------------------

# The render event calling ctx.clear() and canvas.plot() to draw(aka update event).
def update(evt):
    if evt.type == tk.EventType.ButtonPress:
        pan_tool.start_drag(evt.x / size[0], evt.y / size[1])
    if evt.type == tk.EventType.Motion:
        pan_tool.dragging(evt.x / size[0], evt.y / size[1])
    if evt.type == tk.EventType.ButtonRelease:
        pan_tool.stop_drag(evt.x / size[0], evt.y / size[1])
    canvas.pan(pan_tool.value)
    with tkfbo:
        ctx.clear()
        canvas.plot(verts)
# --------------------------------------
# base tk code's
root = tk.Tk()
# import GL widget
lbl = GlWidget(root)
# get the context greated by the widget `lbl`
ctx = lbl.context()
# get the renderer.canvas where everything is drawn
canvas = lbl.canvas()
# add pan support(aka PanTool)
pan_tool = lbl.pan_tool()
# size of the context(currenctly its fixed in the class)
# the fbo
tkfbo = lbl.fbo()

# update events connect
lbl.bind("<ButtonPress-1>", update)
lbl.bind("<ButtonRelease-1>", update)
lbl.bind('<Motion>', update)

# basic tk codes.
lbl.pack()
root.mainloop()
