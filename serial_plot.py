import serial, argparse
from collections import deque
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen, countDownLen):
      # open serial port
      self.ser = serial.Serial(strPort, 115200)
      self.maxLen = maxLen
      self.countDownLen = countDownLen
      self.countDownX1 = 0
      self.countDownY1 = 0
      self.countDownX2 = 0
      self.countDownY2 = 0
      
      # original data
      self.ax1 = deque([0.0]*maxLen)
      self.ay1 = deque([0.0]*maxLen)
      self.az1 = deque([0.0]*maxLen)
      self.ax2 = deque([0.0]*maxLen)
      self.ay2 = deque([0.0]*maxLen)
      self.az2 = deque([0.0]*maxLen)
      
      # first derivative
      self.ax1d1 = deque([0.0]*maxLen)
      self.ay1d1 = deque([0.0]*maxLen)
      self.ax2d1 = deque([0.0]*maxLen)
      self.ay2d1 = deque([0.0]*maxLen)
      
      # second derivative
      self.ax1d2 = deque([0.0]*maxLen)
      self.ay1d2 = deque([0.0]*maxLen)
      self.ax2d2 = deque([0.0]*maxLen)
      self.ay2d2 = deque([0.0]*maxLen)

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.appendleft(val)
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
      # first derivative
      self.addToBuf(self.ax1d1, self.first_derivative(self.ax1)-500)
      self.addToBuf(self.ay1d1, self.first_derivative(self.ay1)-500)
      self.addToBuf(self.ax2d1, self.first_derivative(self.ax2)-500)
      self.addToBuf(self.ay2d1, self.first_derivative(self.ay2)-500)
      # second derivative
      self.addToBuf(self.ax1d2, self.second_derivative(self.ax1)-1000)
      self.addToBuf(self.ay1d2, self.second_derivative(self.ay1)-1000)
      self.addToBuf(self.ax2d2, self.second_derivative(self.ax2)-1000)
      self.addToBuf(self.ay2d2, self.second_derivative(self.ay2)-1000)
      
  # calculate the first derivative
  def first_derivative(self, buf):
      if len(buf) < 2:
          return 0.0
      else: 
          return buf[0]-buf[1]
          
  # calculate the second derivative
  def second_derivative(self, buf):
      if len(buf) < 3:
          return 0.0
      else:
          return (buf[0]-buf[1])-(buf[1]-buf[2])

  # update plot
  def update(self, frameNum, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, label1, label2, label3, label4):
      try:
          line = self.ser.readline()
          data = [float(val) for val in line.split()]
          # print data
          if(len(data) == 6):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax1)
              a1.set_data(range(self.maxLen), self.ay1)
              #a2.set_data(range(self.maxLen), self.az1)
              a3.set_data(range(self.maxLen), self.ax2)
              a4.set_data(range(self.maxLen), self.ay2)
              #a5.set_data(range(self.maxLen), self.az2)
              # note: data[0] is pin2, leftX
              #   data[1] is pin1, leftY
              #   data[2] is pin0, leftZ
              #   data[3] is pin11, rightX
              #   data[4] is pin10, rightY
              #   data[5] is pin9, rightZ
              
              # first derivative
              #a6.set_data(range(self.maxLen), self.ax1d1)
              #a3.set_data(range(self.maxLen), self.ay1d1)
              
              # second derivative
              a6.set_data(range(self.maxLen), self.ax1d2)
              a7.set_data(range(self.maxLen), self.ay1d2)
              a8.set_data(range(self.maxLen), self.ax2d2)
              a9.set_data(range(self.maxLen), self.ay2d2)

          # determine whether to fire a left arrow   
          if (self.ay1d2[0] > -500):
              label1.set_text('Left arrow')
              self.countDownY1 = self.countDownLen
          elif(self.countDownY1 > 0):
              self.countDownY1 = self.countDownY1-1
          else:
              label1.set_text('')
          
          # determine whether to fire a down arrow   
          if (self.ax1d2[0] > -500):
              label2.set_text('Down arrow')
              self.countDownX1 = self.countDownLen
          elif(self.countDownX1 > 0):
              self.countDownX1 = self.countDownX1-1
          else:
              label2.set_text('')

          # determine whether to fire an up arrow   
          if (self.ax2d2[0] > -500):
              label3.set_text('Up arrow')
              self.countDownX2 = self.countDownLen
          elif(self.countDownX2 > 0):
              self.countDownX2 = self.countDownX2-1
          else:
              label3.set_text('')

          # determine whether to fire a down arrow   
          if (self.ay2d2[0] > -500):
              label4.set_text('Right arrow')
              self.countDownY2 = self.countDownLen
          elif(self.countDownY2 > 0):
              self.countDownY2 = self.countDownY2-1
          else:
              label4.set_text('')

      except KeyboardInterrupt:
          print('exiting')
      return

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
  analogPlot = AnalogPlot(strPort, 100, 10)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(-1500, 1000))
  
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
  a6, = ax.plot([], [])
  a7, = ax.plot([], [])
  a8, = ax.plot([], [])
  a9, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, label1, label2, label3, label4), 
                                 interval=50)
  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
