###############################################################################
#
# Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################

from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import random
import json
import serial
import time
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
porta = '/dev/ttyUSB4'

for p in ports:
    if "Linux" in p[1]:
        porta = p[0]


baud_rate = 9600
counter = 0
global_val = 0
tempo_ligado = 0
energia_consumida = 0

class AppSession(ApplicationSession):
    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        # SUBSCRIBE to a topic and receive events
        #
        def onhello(msg):
            self.log.info("event for 'onhello' received: {msg}", msg=msg)

        yield self.subscribe(onhello, 'com.example.onhello')
        self.log.info("subscribed to topic 'onhello'")

        # REGISTER a procedure for remote calling
        #
        def add2(x, y):
            self.log.info("add2() called with {x} and {y}", x=x, y=y)
            return x + y

        yield self.register(add2, 'com.example.add2')
        self.log.info("procedure add2() registered")
        
        def randomvalue(x, y):
            self.log.info("RandomValue() called")

            ws = json.dumps({
                "chain": random.randint(x, y), 
                "rotation": random.randint(300, 500), 
                "energy": random.randint(x+10, y+10)
                })

            return ws

        yield self.register(randomvalue, 'com.mubo.randomvalue')
        self.log.info("procedure randomvalue() registered")

        def readSerial():
          last_received = 0
          global_val = 0
          try:
            ser = serial.Serial(porta, baud_rate)
            last_received = None
            buffer_string = ''
            reading = True
            while reading:
            # while x < 10:
              # time.sleep(0.2)
              buffer_string = buffer_string + ser.read(ser.inWaiting())
              if '\n' in buffer_string:
                lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
                last_received = lines[-2]
                #If the Arduino sends lots of empty lines, you'll lose the
                #last filled line, so you could make the above statement conditional
                #like so: if lines[-2]: last_received = lines[-2]
                buffer_string = lines[-1]
                # x += 1
                if last_received != None:
                  reading = False
                  ser.close()
                  global_val = last_received
                  try: 
                    return last_received.strip()
                  except:
                    return last_received
                else:
                  reading = True
          except:
            return global_val

        def serialvalue():
            val = counter
            global tempo_ligado
            ws = json.dumps({
                "message": val
                })
            return ws

        yield self.register(serialvalue, 'com.mubo.serialvalue')
        #yield self.publish('com.mubo.serialvalue', serialvalue)
        self.log.info("procedure serialvalue() registered")
        # PUBLISH and CALL every second .. forever
        #
        counter = 0
        global tempo_ligado
        global energia_consumida
        while True:
            
            # PUBLISH an event
            #
            yield self.publish('com.example.oncounter', counter)
            self.log.info("published to 'oncounter' with counter {counter}",
                          counter = str(counter))
            # counter = counter + 1
            counter = readSerial()
            tempo_ligado += 0.45
            try:
                energia_consumida += (abs((float(counter) - 2.49 )) / 0.185) / 3600
            except:
                energia_consumida = 0
            if (counter == '8') or (counter == 8):
                tempo_ligado = 0
                energia_consumida = 0
            # CALL a remote procedure
            #
            try:
                res = yield self.call('com.example.mul2', counter, 3)
                self.log.info("mul2() called with result: {result}",
                              result=res)
            except ApplicationError as e:
                # ignore errors due to the frontend not yet having
                # registered the procedure we would like to call
                if e.error != 'wamp.error.no_such_procedure':
                    raise e

            yield sleep(1)
