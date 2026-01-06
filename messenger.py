from datetime import datetime
import json
import requests


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



class RemoteStorage:
    def __init__(self):
        self.base_url = "https://groupe5-python-mines.fr"

    def get_users(self):
        r = requests.get(f"{self.base_url}/users")
        return [Users(id=u['id'], name=u['name']) for u in r.json()]

    def get_channels(self):
        r = requests.get(f"{self.base_url}/channels")
        return [channels(id=c['id'], name=c['name'], member_ids=c.get('member_ids', [])) for c in r.json()]

    def get_messages(self):
        r = requests.get(f"{self.base_url}/messages")
        return [messages(id=m['id'], reception_date=m['reception_date'], sender_id=m['sender_id'], channel=m['channel'], content=m['content']) for m in r.json()]

    def create_user(self, name):
        requests.post(f"{self.base_url}/users", json={"name": name})

    def create_channel(self, name, member_ids):
        requests.post(f"{self.base_url}/channels", json={"name": name, "member_ids": member_ids})

    def create_message(self, sender_id, channel_id, content):
        payload = {"sender_id": int(sender_id), "channel": int(channel_id), "content": content}
        requests.post(f"{self.base_url}/messages", json=payload)


storage = RemoteStorage()


with open('server.json') as file:
  server= json.load(file)
  userslist=[]
  for user_dict in server['users']:
    user_object= Users(user_dict['id'], user_dict['name'])
    userslist.append(user_object)
  server['users']= userslist
  

def sauvegarderjson():
  server2= {}
  dico_user_list:list[dict]=[]
  for user in server['users']:
    dico_user_list.append({'name':user.name, 'id': user.id})
  server2['users']= dico_user_list
  dico_channel_list:list[dict]=[]
  for channel in server['channels']:
    dico_channel_list.append({'name': channel.name, 'id': channel.id, 'member_ids': channel.member_ids})
  server2['channels']= dico_channel_list
  dico_mess_list:list[dict]=[]
  for mess in server['messages']:
    dico_mess_list.append({'id': mess.id, 'reception_date': mess.reception_date, 'sender_id': mess.sender_id, 'channel': mess.channel, 'content': mess.content})
  server2['messages']=dico_mess_list
  with open('server.json', 'w') as fichier:
    json.dump(server2, fichier, indent=4)




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
    for user in storage.get_users():
        print(user.id, user.name)

def afficher_groupes():
    for groupe in storage.get_channels():
        print(groupe.id, groupe.name, groupe.member_ids)

def afficher_messages():
    for msg in storage.get_messages():
        print(msg.sender_id, msg.content)
    menuprincipal()



def add_users():
    newname = input('nom nouvel utilisateur : ')
    storage.create_user(newname) 
    afficher_users()
    menuprincipal()

def add_groupes():
    newnameg = input('nom nouveau groupe : ')
    afficher_users()
    newmb = input('membres du groupe : ')
    storage.create_channel(newnameg, [int(newmb)])
    afficher_groupes()
    menuprincipal()

def send_message():
    afficher_users()
    sender_id = input('ID de l\'expéditeur : ')
    afficher_groupes()
    channel_id = input('ID du canal : ')
    content = input('Contenu du message : ')
    storage.create_message(sender_id, channel_id, content)
    afficher_messages()
    menuprincipal()

menuprincipal()


'''
def afficher_users():
   for i in range (len(server['users'])):
     print(server['users'][i].id,server['users'][i].name)
   


def afficher_groupes():
   for i in range (len(server['channels'])):
      print(server['channels'][i].id,server['channels'][i].name,server['channels'][i].member_ids)

   
def afficher_messages():
   for i in range (len(server['messages'])):
      print(server['messages'][i].sender_id, server['messages'][i].content)
   menuprincipal()
  ''' 

'''
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
'''









