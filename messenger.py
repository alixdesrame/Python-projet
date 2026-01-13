from datetime import datetime
import json
import requests


with open('server.json') as file:
    server = json.load(file)


class Users:
  def __init__(self, id: int, name: str):
    self.name = name
    self.id = id

class channels:
  def __init__(self, id: int, name: str, member_ids: int):
    self.id= id
    self.name= name
    self.member_ids= member_ids

class messages:
  def __init__(self, id: int, reception_date: int, sender_id: int, channel: int, content: str):
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
        return [messages(id=m.get('id'), reception_date=m.get('reception_date'), sender_id=m.get('sender_id'), channel=m.get('channel'), content=m.get('content')) for m in r.json()]
        
        
    def create_user(self, name):
        response = requests.post(f"{self.base_url}/users/create", json={"name": name})
        if response.status_code == 201 or response.status_code == 200:
            print(f"Succès : Utilisateur '{name}' créé.")
        else:
            print(f"Erreur serveur ({response.status_code}): {response.text}")

        """requests.post(f"{self.base_url}/users", json={"name": name})"""

    def create_channel(self, name, member_ids):
        requests.post(f"{self.base_url}/channels/create", json={"name": name, "member_ids": member_ids})

    def create_message(self, sender_id, channel_id, content):
        payload = {"sender_id": int(sender_id), "channel": int(channel_id), "content": content}
        requests.post(f"{self.base_url}/messages/create", json=payload)


storage = RemoteStorage()


with open('server.json') as file:
  server= json.load(file)
  userslist=[]
  for user_dict in server['users']:
    user_object = Users(name=user_dict['name'], id=int(user_dict['id']))
    userslist.append(user_object)
  server['users']= userslist
  

def sauvegarderjson():
  server2= {}
  dico_user_list:list[dict]=[]
  for user in server['users']:
    dico_user_list.append({'name':user.name, 'id': user.id})
  server2['users']= dico_user_list
  dico_channel_list = []
  for channel in server.get('channels', []):
    if hasattr(channel, 'name'):
        dico_channel_list.append({'name': channel.name, 'id': channel.id, 'member_ids': channel.member_ids})
    else:
        dico_channel_list.append(channel)
  server2['channels'] = dico_channel_list
  dico_mess_list = []
  for mess in server.get('messages', []):
    if hasattr(mess, 'content'):
        dico_mess_list.append({'id': mess.id, 'reception_date': mess.reception_date, 'sender_id': mess.sender_id, 'channel': mess.channel, 'content': mess.content})
    else:
        dico_mess_list.append(mess)
  server2['messages'] = dico_mess_list
  
  with open('server.json', 'w') as fichier:
    json.dump(server2, fichier, indent=4)

  """dico_channel_list:list[dict]=[]
  for channel in server['channels']:
    dico_channel_list.append({'name': channel.name, 'id': channel.id, 'member_ids': channel.member_ids})
  server2['channels']= dico_channel_list
  dico_mess_list:list[dict]=[]
  for mess in server['messages']:
    dico_mess_list.append({'id': mess.id, 'reception_date': mess.reception_date, 'sender_id': mess.sender_id, 'channel': mess.channel, 'content': mess.content})
  server2['messages']=dico_mess_list
  with open('server.json', 'w') as fichier:
    json.dump(server2, fichier, indent=4)"""




def save_server():
   sauvegarderjson()

   """print("save_server:", server)
   with open('server.json','w') as file:
      json.dump(server, file, indent=4)"""


def get_next_message_id():
    if not server['messages']:
        return 1
    ids = [m.id if hasattr(m, 'id') else m['id'] for m in server['messages']]
    return max(ids) + 1


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
    elif choice == 'u':
     afficher_users()
    elif choice == 'g':
     afficher_groupes()
    elif choice == 'm':
     afficher_messages()
    elif choice == 'p':
     menuprincipal()
    elif choice == 'a':
     add_users()
    elif choice == 'r':
     add_groupes()
    elif choice == 's':
     send_message()
    else:
     print('Unknown option:', choice)
     menuprincipal()



def afficher_users():
    print("--- Utilisateurs sur le serveur ---")
    for user in storage.get_users():
        print(f"ID: {user.id} | Nom: {user.name}")
    menuprincipal()

def afficher_groupes():
    print("--- Groupes sur le serveur ---")
    for groupe in storage.get_channels():
        print(groupe.id, groupe.name, groupe.member_ids)
    menuprincipal()

def afficher_messages():
    print("--- Messages sur le serveur ---")
    for msg in storage.get_messages():
        print(msg.sender_id, msg.content)
    menuprincipal()



def add_users():
    newname = input('nom nouvel utilisateur : ')
    storage.create_user(newname) 
    print(f"Utilisateur {newname} envoyé au serveur.")
    afficher_users()
    menuprincipal()

def add_groupes():
    newnameg = input('nom nouveau groupe : ')
    newmb = input('ID du premier membre : ')
    storage.create_channel(newnameg, [int(newmb)])
    afficher_groupes()
    menuprincipal()

    """newmb = input('membres du groupe : ')
    storage.create_channel(newnameg, [int(newmb)])
    afficher_groupes()
    menuprincipal()"""

def send_message():
    sender_id = input('ID de l\'expéditeur : ')
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









