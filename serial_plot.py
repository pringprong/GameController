"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 115200)

      self.ax1 = deque([0.0]*maxLen)
      self.ay1 = deque([0.0]*maxLen)
      self.az1 = deque([0.0]*maxLen)
      self.ax2 = deque([0.0]*maxLen)
      self.ay2 = deque([0.0]*maxLen)
      self.az2 = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      assert(len(data) == 6)
      self.addToBuf(self.ax1, data[0])
      self.addToBuf(self.ay1, data[1])
      self.addToBuf(self.az1, data[2])
      self.addToBuf(self.ax2, data[3])
      self.addToBuf(self.ay2, data[4])
      self.addToBuf(self.az2, data[5])

  # update plot
  def update(self, frameNum, a0, a1, a2, a3, a4, a5, label1, label2, label3, label4):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 6):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax1)
              a1.set_data(range(self.maxLen), self.ay1)
              a2.set_data(range(self.maxLen), self.az1)
              a3.set_data(range(self.maxLen), self.ax2)
              a4.set_data(range(self.maxLen), self.ay2)
              a5.set_data(range(self.maxLen), self.az2)
          # note: data[0] is pin4, leftX
              #   data[1] is pin5, leftY
              #   data[2] is pin6, leftZ
              #   data[3] is pin9, rightX
              #   data[4] is pin10, rightY
              #   data[5] is pin11, rightZ
          # determine whether to fire a left arrow   
          if (data[0] > 500):
              curr_label = 'Left arrow'
          else:
              curr_label = ''
          label1.set_text(curr_label)
          
          # determine whether to fire a down arrow   
          if (data[1] > 500):
              curr_label = 'Down arrow'
          else:
              curr_label = ''
          label2.set_text(curr_label)

          # determine whether to fire an up arrow   
          if (data[3] > 500):
              curr_label = 'Up arrow'
          else:
              curr_label = ''
          label3.set_text(curr_label)

          # determine whether to fire a down arrow   
          if (data[4] > 500):
              curr_label = 'Right arrow'
          else:
              curr_label = ''
          label4.set_text(curr_label)

      except KeyboardInterrupt:
          print('exiting')
      
#      return a0, a1, a2, a3, a4, a5, label
      return a0

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, 100)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
  
  label1 = ax.text(5, 1000, 'Left Arrow', ha='left', va='center', fontsize=12)
  label2 = ax.text(20, 1000, 'Down Arrow', ha='left', va='center', fontsize=12)
  label3 = ax.text(45, 1000, 'Up Arrow', ha='left', va='center', fontsize=12)
  label4 = ax.text(75, 1000, 'Right Arrow', ha='left', va='center', fontsize=12)
          
  a0, = ax.plot([], [])
  a1, = ax.plot([], [])
  a2, = ax.plot([], [])
  a3, = ax.plot([], [])
  a4, = ax.plot([], [])
  a5, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1, a2, a3, a4, a5, label1, label2, label3, label4), 
                                 interval=50)
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
