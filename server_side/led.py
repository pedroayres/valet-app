#!/usr/bin/python
import serial
import time
porta = '/dev/ttyUSB0'
baud_rate = 9600

#######################################################################
def escrever_porta():
  try:
    valor = (raw_input("Digite 1 para ligar o led.\nDigite 2 para desligar o led.\n"))
    Obj_porta = serial.Serial(porta, baud_rate)
    Obj_porta.write(valor)
    ler_porta()
    Obj_porta.close()

  except serial.SerialException:
    print"ERRO: Verifique se ha algum dispositivo conectado na porta!"

#########################################################################
def ler_porta():
    try:
        ser = serial.Serial(porta, baud_rate)
        global last_received

        buffer_string = ''
        while True:
            buffer_string = buffer_string + ser.read(ser.inWaiting())
            if buffer_string == None:
                print "null"
            if '\n' in buffer_string:
                lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
                last_received = lines[-2]
                #If the Arduino sends lots of empty lines, you'll lose the
                #last filled line, so you could make the above statement conditional
                #like so: if lines[-2]: last_received = lines[-2]
                buffer_string = lines[-1]
                return last_received
    except serial.serialutil.SerialException:
        print "deu ruim mas continuou"
        ler_porta()

def read_serial():
  buffer_string = "vazio"
  try:
    ser = serial.Serial(porta, baud_rate, timeout=1)
    last_received = None
    reading = True
    while reading:
      buffer_string = buffer_string + ser.read(ser.inWaiting())
      # print "ser.read: " + ser.read(ser.inWaiting())
      # if buffer_string == "vazio":
      #   last_received = "";
      #   print "buffer vazio"
      #   # return ""
      # if ser.read(ser.inWaiting()) != "":
      if '\n' in buffer_string:
        lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
        last_received = lines[-2]
        #If the Arduino sends lots of empty lines, you'll lose the
        #last filled line, so you could make the above statement conditional
        #like so: if lines[-2]: last_received = lines[-2]
        buffer_string = lines[-1]
        # if buffer_string == "":
        #     print "end buffer nada"
        # else:
        #     print "end buffer: " + buffer_string
        if last_received != "":
          # reading = False
          print "last:" + last_received    
          time.sleep(0.2)
          # return last_received  
        else:
          print "null"  
          reading = False
  except serial.serialutil.SerialException:
    print "deu ruim mas continuou"
    read_serial()

  ################################ MAIN ####################################
if __name__=='__main__':
    read_serial()
    print "read:" + read_serial()

