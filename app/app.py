#!/usr/bin/env python
from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
import odl_comunication
import dataflow 

app = Flask(__name__)
Flow = dataflow.Data_Flow()
ODL = odl_comunication.OpenDayLight();

@app.route("/")
def index():
     return render_template('index.html')


@app.route("/services")
def services():
     return render_template('services.html', form='')
   

@app.route('/action', methods=['POST'])
def action():
     if request.method == 'POST' :
          Flow.empty_data()
          if validateFlow(request.form):
               mensaje=0
               Flow.print_all()
               ODL.addFlows(Flow.ip_origen,Flow.puerto_origen,Flow.ip_destino,Flow.puerto_destino,Flow.protocolo,Flow.accion)
          else:
               mensaje=1
     return render_template('services.html', form=request.form, mensaje=mensaje)


def validateFlow(form):
     form.errors = {}      
     if ODL.testConection():   
         if validateFields(form):
              Flow.accion=form['accion']
              if  len((form['ip_origen']))>0 :
                   if validateIP(form['ip_origen']):
                        if len((form['mascara_origen']))>0 :
                             if validateMascara(form['mascara_origen']):
                                  Flow.ip_origen=str(form['ip_origen'])+'/'+str(form['mascara_origen'])
                             else:
                                  form.errors['mascara_origen'] = 'Mascara origen incorrecta.'
                        else:
                             form.errors['mascara_origen'] = 'Ingresar mascara para la IP origen' 
                   else:
                       form.errors['ip_origen'] = 'IP origen incorreta'         
                             
              if len((form['ip_destino']))>0 : 
                   if validateIP(form['ip_destino']):
                        if len((form['mascara_destino']))>0 and validateMascara(form['mascara_destino']):
                            Flow.ip_destino=str(form['ip_destino'])+'/'+str(form['mascara_destino'])
                        else: 
                             form.errors['mascara_destino'] = 'Mascara destino incorrecta.'  
                   else:
                        form.errors['ip_origen'] = 'IP destino incorreta'

              if len(form['puerto_origen']) > 0 :
                   if validatePuerto(form['puerto_origen']):
                        Flow.puerto_origen=form['puerto_origen']
                        validateProtocolo(form['protocolo'])
                   else: 
                        form.errors['puerto_origen'] = 'Puerto origen incorrecto.'     

              if len(form['puerto_destino']) > 0 :
                   if validatePuerto(form['puerto_destino']):
                        Flow.puerto_destino=form['puerto_destino']
                        validateProtocolo(form['protocolo'])
                   else: 
                        form.errors['puerto_destino'] = 'Puerto origen destino.'

         else:
              form.errors['puerto_destino'] = 'Es necesario completar algun campo (IP y Mascara o puerto)'
     else:
        form.errors['puerto_destino'] = 'Error al conectarse al controlador.'
     
     if len(form.errors) == 0 :
          return True
     else: 
          return False

def validateFields(form): 
     if len((form['puerto_origen']))>0 or (len((form['ip_origen']))>0 and len((form['mascara_origen']))>0) or len(form['puerto_destino'])>0 or (len((form['ip_destino']))>0 and len((form['mascara_destino']))>0) : 
          try:
               if int(form['accion']) >=0 and int(form['accion']) <= 1 :
                     return True
               else:
                    return False
          except:
               return False
     else:
          return False

def validateIP(ip):
   if len(ip.split()) == 1:
        ipList = ip.split('.')
        if len(ipList) == 4:
            for i, item in enumerate(ipList):
                try:
                    ipList[i] = int(item)
                except:
                    return False
                if not isinstance(ipList[i], int):
                    return False
            if max(ipList) < 256 and min(ipList) > -1:
                return True
            else:
                return False
        else:
            return False
   else:
        return False

def validatePuerto(puerto):
     try:
          if int(puerto) < 0 or int(puerto) > 65535:
               return False
          else:
               return True
     except:
          return False

def validateProtocolo(protocolo):
      try:
          if int(protocolo) >= 0 and int(protocolo) <=1:
              Flow.protocolo=int(protocolo)
          else:
              Flow.protocolo=0
      except:
           Flow.protocolo=0

def validateMascara(mascara):
     try:
          if (int(mascara) < 1 or int(mascara) > 32):
               return False
          else:
               return True
     except:
          return False


@app.errorhandler(404)
def page_not_found(e):
     return redirect(url_for('index'))


if __name__ == '__main__':
     app.run(debug=True, port=8000)

