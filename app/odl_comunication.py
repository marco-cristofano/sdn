import requests
import xml.etree.ElementTree as ET
import json 
  
class OpenDayLight:
     cant_switch = 5
     switchs = [5,5,5,5,5]

     def url_addFlow(self,switch, table, flow):
          return "http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+str(switch)+"/table/"+str(table)+"/flow/"+ str(flow)
     
     def assemble_payload(self,priority,ip_origen,puerto_origen,ip_destino,puerto_destino,protocolo,accion,flow,table_id):
          payload="""<?xml version="1.0" encoding="UTF-8" standalone="no"?><flow xmlns="urn:opendaylight:flow:inventory"><priority>"""+str(priority)+"""</priority><flow-name>Foo</flow-name>""" 
          payload=str(payload)+"""<instructions><instruction><order>0</order><apply-actions><action><order>0</order>""" 
          if str(accion) == '0':
                payload=str(payload)+"""<drop-action/>"""
              

          if str(accion) == '1':
                payload=str(payload)+"""<output-action><output-node-connector>ALL</output-node-connector><max-length>60</max-length></output-action>"""                     
          
          payload=str(payload)+"""</action></apply-actions></instruction></instructions>"""
          
          payload=str(payload)+"""<match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match>"""
          if ip_origen != None:
               payload=str(payload)+""" <ipv4-source>"""+str(ip_origen)+"""</ipv4-source>"""

          if ip_destino != None:
               payload=str(payload)+"""<ipv4-destination>"""+str(ip_destino)+"""</ipv4-destination>"""

          if puerto_origen != None or puerto_destino != None:
               if protocolo == 0:     
                    payload=str(payload)+"""<ip-match><ip-protocol>6</ip-protocol></ip-match>"""
               elif protocolo ==1:
                    payload=str(payload)+"""<ip-match><ip-protocol>17</ip-protocol></ip-match>"""

               if puerto_origen != None:                    
                    if protocolo == 0:
                          payload=str(payload)+"""<tcp-source-port>"""+str(puerto_origen)+"""</tcp-source-port>"""
                    if protocolo == 1:
                          payload=str(payload)+"""<udp-source-port>"""+str(puerto_origen)+"""</udp-source-port>"""

               if puerto_destino != None:
                    if protocolo == 0:
                          payload=str(payload)+"""<tcp-destination-port>"""+str(puerto_destino)+"""</tcp-destination-port>"""
                    if protocolo == 1:
                          payload=str(payload)+"""<udp-destination-port>"""+str(puerto_destino)+"""</udp-destination-port>"""

          payload=str(payload)+"""</match><id>"""+str(flow)+"""</id><table_id>"""+str(table_id)+"""</table_id> </flow>"""
          return payload


     def addFlow(self,ip_origen,puerto_origen,ip_destino,puerto_destino,protocolo,accion,switch,flow):
          table_id=0
          URL=self.url_addFlow(switch,table_id,flow)
          HEADERS = {'Content-Type': 'application/xml','Accept':'application/xml'}
          PAYLOAD= self.assemble_payload(flow,ip_origen,puerto_origen,ip_destino,puerto_destino,protocolo,accion,flow,table_id)
          r = requests.put(url=URL, auth=('admin', 'admin') ,headers=HEADERS,data=PAYLOAD).text
          print (r.status_code)  
     
     def addFlows(self,ip_origen,puerto_origen,ip_destino,puerto_destino,protocolo,action):
          for switch in range(0,self.cant_switch):
               self.addFlow(ip_origen,puerto_origen,ip_destino,puerto_destino,protocolo,action,switch,self.switchs[switch]) 
               self.switchs[switch]=self.switchs[switch]+1
          
            

     def testConection(self):
          URL="http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/"
          HEADERS = {'Content-Type': 'application/xml','Accept':'application/xml'}
          try:
               r=requests.get(url=URL, auth=('admin', 'admin') ,headers=HEADERS)
               return (r.status_code == requests.codes.ok)
          except:     
               return False

     def get_nodes(self):
          URL="http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/"
          HEADERS = {'Content-Type': 'application/xml','Accept':'application/xml'}
          r=requests.get(url=URL, auth=('admin', 'admin') ,headers=HEADERS)
          b=r.content
          print r.headers
          #print r.raw
          #print r.text
          root=ET.fromstring(b)
        

