#Author: Felipe Lira
#Description: Script que altera a senha WEBGui de ONUs Fiberhome, percorrendo uma lista em um arquivo .csv

import socket
import csv
import time


olt = input('Informe a qual OLT pertence o arquivo.csv: ')
user = 'GEPON'
password = input(f'Informe a qual senha da OLT {olt}: ')
senhaWEB = input('Informe a nova senha WEBGui da ONU: ')

st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(command):
    st.send(command.encode('utf-8'))
    rcv = str(st.recv(4096))
    return rcv

def connect(server):
    st.connect((olt, 23))
    send(f'GEPON\n')
    send(f'{password}\n')
    send(f'en\n')
    send(f'{password}\n')
    send(f'cd onu\n')
    
connect(olt)



#função para alterar a senha da ONU
def altera_senha(slot, pon, onu):

    st.send(f'set web_cfg_mng slot {slot} pon {pon} onu {onu} index 1 web_user admin web_password {senhaWEB} group admin\n'.encode())
    st.send(f'apply web_cfg_mng slot {slot} pon {pon} onu {onu}\n'.encode())
    time.sleep(0.5)
    rcv = st.recv(8192)

    if 'OK' in rcv.decode():
      print ("+ Sucesso ao adicionar a senha na ONU {} localizada no slot {} e PON {}".format(onu,slot,pon))
    
    else:
      print ("- Erro ao adicionar a senha na ONU {} localizada no slot {} e PON {}".format(onu,slot,pon))



#ler o arquivo .CSV
csv_onu = 'onu-senha.csv'

with open(csv_onu, 'r') as csv_f:
   csv_reader = csv.reader(csv_f)
   next(csv_reader)
   for line in csv_reader:
       slot, pon, onu = line[0:3]
       altera_senha(slot, pon, onu)




