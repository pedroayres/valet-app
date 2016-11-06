#!/usr/bin/python
import falcon 
import json
import serial

from autobahn.twisted.websocket import WebSocketClientProtocol, \
        WebSocketClientFactory
import serial.tools.list_ports
#ports = list(serial.tools.list_ports.comports())
porta = '/dev/ttyUSB1'

#for p in ports:
#    if "Linux" in p[1]:
#        porta = p[0]

baud_rate = 9600
class Main:
	def on_get(self, req, resp):
		#allow CORS
		resp.set_header('Access-Control-Allow-Origin', '*')
		resp.status = falcon.HTTP_200
		resp.body = json.dumps({"mubo":"mubo"})
		valor = req.params['valor']
		ser = serial.Serial(porta, baud_rate)
		ser.write(valor)
		ser.close()

class Mubo:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ("Falcon Mubo Online!")
        print req.params['valor']


app = falcon.API()

main = Main()
mubo = Mubo()


app.add_route('/', main)
app.add_route('/mubo', mubo)

