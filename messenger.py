from datetime import datetime
import json


with open('server.json') as file:
    server = json.load(file)


class Users:
  def __init__(self, name: str, id: int):
    self.name = name
    self.id = id

class channels:
  def _init_(self, id: int, name: str, member_ids: int):
    self.id= id
    self.name= name
    self.member_ids= member_ids

class messages:
  def _init_(self, id: int, reception_date: int, sender_id: int, channel: int, content: str):
    self.id= id
    self.reception_date= reception_date
    self.sender_id= sender_id
    self.channel= channel
    self.content= content


def save_server():
   print("save_server:", server)
   with open('server.json','w') as file:
      json.dump(server, file, indent=4)


def get_next_message_id():
    if not server['messages']:
        return 1
    return max(m['id'] for m in server['messages']) + 1


def menuprincipal():
    print('=== Messenger ===')
    print('x. Leave')
    print('u.users')
    print('g.groupes')
    print('m.messages')
    print('a.ajout users')
    print('p.menu principal')
    print('r.add groupes')
    print('s.send')
    choice = input('Select an option: ')
    if choice == 'x':
     print('Bye!')
    if choice == 'u':
     afficher_users()
    if choice == 'g':
     afficher_groupes()
    if choice == 'm':
     afficher_messages()
    if choice == 'p':
     menuprincipal()
    if choice == 'a':
     add_users()
    if choice == 'r':
     add_groupes()
    if choice == 's':
     send_message()
    else:
     print('Unknown option:', choice)


def afficher_users():
   for i in range (len(server['users'])):
      print(server['users'][i]['id'],server['users'][i]['name'])
   
def afficher_groupes():
   for i in range (len(server['channels'])):
      print(server['channels'][i]['id'],server['channels'][i]['name'],server['channels'][i]['member_ids'])

   
def afficher_messages():
   for i in range (len(server['messages'])):
      print(server['messages'][i]['sender_id'], server['messages'][i]['content'])
   menuprincipal()
   
def add_users():
   newid= input('id nouvel utilisateur: ')
   newname= input('nom nouvel utilisateur: ')
   newuser= {'id': int(newid), 'name': newname}
   server['users'].append(newuser)
   afficher_users()
   save_server()
   menuprincipal()
   
   
def add_groupes():
   newidg= input('id nouveau groupe: ')
   newnameg= input('nom nouveau groupe: ')
   afficher_users()
   newmb= input('membres du groupe: ')
   newchannel= {'id': newidg, 'name': newnameg, 'member_ids': [newmb]}
   server['channels'].append(newchannel)
   afficher_groupes()
   save_server()
   menuprincipal()


def send_message():
   afficher_users()
   sender_id = input('ID de l\'expéditeur: ')
   afficher_groupes()
   channel_id = input('ID du canal: ')
   content = input('Contenu du message: ')
   new_message_id= get_next_message_id()
   reception_date = int(datetime.now().strftime('%Y%m%d'))
   new_message= {'id': new_message_id,'reception_date': reception_date,'sender_id': int(sender_id),'channel': int(channel_id),'content': content }
   server['messages'].append(new_message)
   save_server()
   afficher_messages()
   menuprincipal()



menuprincipal()








