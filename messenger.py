from datetime import datetime
import json
import requests
import argparse


with open('server.json') as file:
    server = json.load(file)


class Users:
  def __init__(self, id: int, name: str):
    self.name = name
    self.id = id

# Par convention les noms de classes commencent pas une majuscule
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
        # Vous pouvez rendre cette URL configurable
        # par l'utilisateur en ajoutant un paramètre
        # "base_url" à cette fonction, puis en remplaçant cette ligne
        # par self.base_url = base_url
        self.base_url = "https://groupe5-python-mines.fr"

    # N'oubliez pas de typer vos fonctions afin d'indiquer
    # votre intention aux personnes qui reprendront votre code
    def get_users(self) -> list[Users]:
        r = requests.get(f"{self.base_url}/users")
        # Il vaut vérifier le code de retour HTTP
        r.raise_for_status()
        return [Users(id=u['id'], name=u['name']) for u in r.json()]

    def get_channels(self) -> list[channels]:
        r = requests.get(f"{self.base_url}/channels")
        r.raise_for_status()
        return [channels(id=c['id'], name=c['name'], member_ids=c.get('member_ids', [])) for c in r.json()]
        

    def get_messages(self) -> list[messages]:
        r = requests.get(f"{self.base_url}/messages")
        r.raise_for_status()
        return [messages(id=m.get('id'), reception_date=m.get('reception_date'), sender_id=m.get('sender_id'), channel=m.get('channel'), content=m.get('content')) for m in r.json()]
        
        
    def create_user(self, name: str) -> None:
        response = requests.post(f"{self.base_url}/users/create", json={"name": name})
        if response.status_code == 201 or response.status_code == 200:
            print(f"Succès : Utilisateur '{name}' créé.")
        else:
            print(f"Erreur serveur ({response.status_code}): {response.text}")

    

    def create_channel(self, name: str, member_ids: list[int]) -> None:
        response = requests.post(f"{self.base_url}/channels/create", json={"name": name, "member_ids": member_ids})
        response.raise_for_status()

    def create_message(self, sender_id: int, channel_id: int, content: str) -> None:
        payload = {"sender_id": int(sender_id), "channel": int(channel_id), "content": content}
        responses= requests.post(f"{self.base_url}/channels/{channel_id}/messages/post", json=payload)
        if responses.status_code == 201 or responses.status_code == 200:
            print(f"Succès : messages envoyé")
        else:
            print(f"Erreur serveur ({responses.status_code}): {responses.text}")






class LocalStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Il vaut mieux créer 3 attributs self.users, self.channels,
        # et self.messages, et les typer explicitement.
        self.data = {"users": [], "channels": [], "messages": []}
        self.load()

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save()

    def save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_users(self) -> list[Users]:
        return [Users(id=u['id'], name=u['name']) for u in self.data.get('users', [])]

    def get_channels(self) -> list[channels]:
        return [channels(id=c['id'], name=c['name'], member_ids=c.get('member_ids', [])) 
                for c in self.data.get('channels', [])]

    def get_messages(self) -> list[messages]:
        return [messages(id=m.get('id'), reception_date=m.get('reception_date'), 
                         sender_id=m.get('sender_id'), channel=m.get('channel'), 
                         content=m.get('content')) 
                for m in self.data.get('messages', [])]

    def create_user(self, name: str) -> None:
        users = self.data.get('users', [])
        # TB d'avoir pensé au default
        new_id = max([int(u['id']) for u in users], default=0) + 1
        
        users.append({"id": new_id, "name": name})
        self.save()
        print(f"Succès : Utilisateur '{name}' enregistré dans {self.file_path}.")

    def create_channel(self, name: str, member_ids: list[int]) -> None:
        channels_list = self.data.get('channels', [])
        new_id = max([c['id'] for c in channels_list], default=0) + 1
        
        channels_list.append({"id": new_id, "name": name, "member_ids": member_ids})
        self.save()

    def create_message(self, sender_id: int, channel_id: int, content: str) -> None:
        messages_list = self.data.get('messages', [])
        new_id = max([m['id'] for m in messages_list], default=0) + 1
        reception_date = int(datetime.now().strftime('%Y%m%d'))
        
        messages_list.append({
            "id": new_id,
            "reception_date": reception_date,
            "sender_id": int(sender_id),
            "channel": int(channel_id),
            "content": content
        })
        self.save() 


# Il faut utiliser le module argparse afin de pouvoir
# donner le choix à l'utilisateur dès le lancement du programme
def choix():
   print('LocalStorage')
   print('RemoteStorage')
   choice= input('choisir:')
   if choice=='LocalStorage':
      return LocalStorage('server.json')
   if choice=='RemoteStorage':
      return RemoteStorage()
   
storage= choix()

# Ce code n'est plus utile car repris dans LocalStorage.load
with open('server.json') as file:
  server= json.load(file)
  userslist=[]
  for user_dict in server['users']:
    user_object = Users(name=user_dict['name'], id=int(user_dict['id']))
    userslist.append(user_object)
  server['users']= userslist
  

# Idem avec LocalStorage.save
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

 



# Idem LocalStorage.save
def save_server():
   sauvegarderjson()

 

# Inutilisé
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
     # Utilisez 4 espaces pour l'indentation
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


def send_message():
    sender_id = input('ID de l\'expéditeur : ')
    channel_id = input('ID du canal : ')
    content = input('Contenu du message : ')
    storage.create_message(sender_id, channel_id, content)
    afficher_messages()
    menuprincipal()

menuprincipal()












