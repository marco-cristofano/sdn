class Data_Flow:
     ip_origen= None
     puerto_origen= None
     ip_destino= None
     puerto_destino= None
     protocolo= None
     accion= None


     def empty_data(self):
          self.ip_origen= None
          self.puerto_origen= None
          self.ip_destino= None
          self.puerto_destino= None
          self.protocolo= None
          self.accion= None


     def print_all(self):
          print self.ip_origen
          print self.puerto_origen
          print self.ip_destino
          print self.puerto_destino
          print self.protocolo
          print self.accion
     