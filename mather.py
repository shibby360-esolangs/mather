import sys, os
import tkinter as tk
import math
import time
graph = tk.Tk()
graph.title('mather')
def mather(code, canvases={}, vars={}):
  code = code.split('\n')
  loopcode = ''
  looping = False
  toexec = True
  loopcond = ''
  tracktransform = False
  def findfig(name):
    for i in canvases:
        if name in canvases[i]['figures']:
          fig = canvases[i]['figures'][name]
          cvs = canvases[i]['cnvs']
          dct = canvases[i]
    return fig, cvs, dct
  for i in range(len(code)):
    line = code[i]
    splt = line.split(' ')
    for j in range(len(splt)):
      if splt[j].startswith('vr-'):
        splt[j] = vars[splt[j][3:]]
      if splt[j].startswith('calc('):
        splt[j] = str(eval(splt[j][5:-1]))
    cmd = splt[0]
    if cmd.startswith('--'):
      continue
    elif cmd == 'addcanvas' and toexec:
      cnvs = tk.Canvas(graph, width=int(splt[2]), height=int(splt[3]))
      cnvs.pack()
      canvases[splt[1]] = {'cnvs':cnvs, 'figures':{}, 'width':int(splt[2]), 'height':int(splt[3])}
    elif cmd == 'figure' and toexec:
      args = splt[3:]
      coords = []
      for i in args:
        coords += [i.split(',')[0], i.split(',')[1]]
      fig = canvases[splt[1]]['cnvs'].create_polygon(*coords)
      canvases[splt[1]]['figures'][splt[2]] = fig
    elif cmd == 'rectangle' and toexec:
      x, y = splt[3].split(',')
      x, y = int(x), int(y)
      width, height = int(splt[4]), int(splt[5])
      fig = canvases[splt[1]]['cnvs'].create_rectangle(x, y, x+width, y+height, fill='black', outline='')
      canvases[splt[1]]['figures'][splt[2]] = fig
    elif cmd == 'ellipse' and toexec:
      x, y = splt[3].split(',')
      x, y = int(x), int(y)
      width, height = int(splt[4]), int(splt[5])
      fig = canvases[splt[1]]['cnvs'].create_oval(x, y, x+width, y+height, fill='black', outline='')
      canvases[splt[1]]['figures'][splt[2]] = fig
    elif cmd == 'arc' and toexec:
      x, y = splt[3].split(',')
      x, y = int(x), int(y)
      width, height = int(splt[4]), int(splt[5])
      start = int(splt[6])
      extent = int(splt[7])
      fig = canvases[splt[1]]['cnvs'].create_arc(x, y, x+width, y+height, fill='black', start=start, extent=extent, outline='')
      canvases[splt[1]]['figures'][splt[2]] = fig
    elif cmd == 'translate' and toexec:
      fig, cvs, dct = findfig(splt[1])
      coords = cvs.coords(fig)
      for i in range(0, len(coords), 2):
        coords[i], coords[i+1] = coords[i]+int(splt[2]), coords[i+1]+int(splt[3])
      cvs.coords(fig, *coords)
      if tracktransform:
        print('Translated', splt[1], abs(int(splt[2])), 'units', 'left' if x < 0 else 'right', 'and', abs(int(splt[3])), 'up' if y < 0 else 'down')
    elif cmd == 'rotate' and toexec:
      def rotate(points, angle):
        new_points = list(points)
        rad = angle * (math.pi/180)
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        for coords in new_points:
          x_val = coords[0] 
          y_val = coords[1]
          coords[0] = x_val * cos_val - y_val * sin_val
          coords[1] = x_val * sin_val + y_val * cos_val
        return new_points
      fig, cvs, dct = findfig(splt[1])
      coords = cvs.coords(fig)
      center = splt[2]
      if center == 'center':
        center = str(dct['width']/2) + ',' + str(dct['height']/2)
      center = [center.split(',')[0], center.split(',')[1]]
      for i in range(len(coords)):
        if i % 2 == 0: # y
          coords[i] += float(center[1])
        else:
          coords[i] -= float(center[0])
      ncoords = []
      for i in range(0, len(coords), 2):
        ncoords += [[coords[i], coords[i+1]]]
      splt[3] = int(splt[3])
      ncoords = rotate(ncoords, splt[3])
      coords = []
      for i in ncoords:
        coords.append(i[0])
        coords.append(i[1])
      cvs.coords(fig, *coords)
      if tracktransform:
        print('Rotated', splt[1], 'around', center, splt[3], 'degrees')
    elif cmd == 'dilate' and toexec:
      fig, cvs, dct = findfig(splt[1])
      coords = cvs.coords(fig)
      for i in range(0,len(coords),2):
        coords[i] *= float(splt[2])
        coords[i+1] *= float(splt[2])
        if len(splt) == 3:
          splt.append('0,0')
        coords[i], coords[i+1] = coords[i] + int(splt[3].split(',')[0]), coords[i+1] + int(splt[3].split(',')[1])
      cvs.coords(fig, *coords)
      if tracktransform:
        print('Dilated', splt[1], 'by', splt[2])
    elif cmd == 'clone' and toexec:
      fig, cvs, dct = findfig(splt[1])
      dct['figures'][splt[2]] = cvs.create_polygon(*cvs.coords(fig))
      config = cvs.itemconfig(fig)
      new_config = {key: config[key][-1] for key in config.keys()}
      cvs.itemconfig(dct['figures'][splt[2]], **new_config)
    elif cmd == 'color' and toexec:
      fig, cvs, dct = findfig(splt[1])
      cvs.itemconfig(fig, fill=splt[2])
    elif cmd == 'outline' and toexec:
      fig, cvs, dct = findfig(splt[1])
      cvs.itemconfig(fig, outline=splt[2])
    elif cmd == 'waitenter' and toexec:
      input()
    elif cmd == 'exit' and toexec:
      exit()
    elif cmd == 'infinite' and toexec:
      looping = True
      loopcond = 'True'
      line = ''
      toexec = False
    elif cmd == 'while' and toexec:
      loopcond = splt[2:]
      looping = True
      line = ''
      toexec = False
    elif cmd == 'closeloop':
      looping = False
      while eval(loopcond):
        mather(loopcode, canvases)
      loopcode = ''
      loopcond = ''
      toexec = True
    elif cmd == 'wait' and toexec:
      time.sleep(int(splt[1]))
    elif cmd == 'var' and toexec:
      vars[splt[1]] = splt[2]
    elif cmd == 'image' and toexec:
      x, y = splt[3].split(',')
      x, y = int(x), int(y)
      fig = canvases[splt[1]]['cnvs'].create_image(x, y, image=splt[4], anchor='nw')
      canvases[splt[1]]['figures'][splt[2]] = fig
    elif cmd == 'tracktransformations':
      tracktransform = True
    elif cmd == 'log':
      print(' '.join(splt[1:]))
    elif cmd == 'clear':
      os.system('clear')
    elif cmd == '':
      continue
    else:
      raise ValueError('Unknown command')
    if looping:
      loopcode += line + '\n'
  graph.mainloop()
mather(sys.argv[1])
