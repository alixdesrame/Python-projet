from datetime import datetime
import json


server = {
    'users': [
        {'id': 41, 'name': 'Alice'},
        {'id': 23, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 12, 'name': 'Town square', 'member_ids': [41, 23]}
    ],
    'messages': [
        {
            'id': 18,
            'reception_date': datetime.now(),
            'sender_id': 41,
            'channel': 12,
            'content': 'Hi 👋'
        }
    ]
}





def menuprincipal():
    print('=== Messenger ===')
    print('x. Leave')
    print('u.users')
    print('g.groupes')
    print('m.messages')
    print('a.ajout users')
    print('p.menu principal')
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
    if choice == 'g':
     add_groupes()
    else:
     print('Unknown option:', choice)

def afficher_users():
   for i in range (len(server['users'])):
      print(server['users'][i]['id'],server['users'][i]['name'])
   menuprincipal()
   
def afficher_groupes():
   for i in range (len(server['channels'])):
      print(server['channels'][i]['id'],server['channels'][i]['name'],server['channels'][i]['member_ids'])
   menuprincipal()
   
def afficher_messages():
   for i in range (len(server['messages'])):
      print(server['messages'][i]['sender_id'], server['messages'][i]['content'])
   menuprincipal()
   
def add_users():
   newid= input('id nouvel utilisateur: ')
   newname= input('nom nouvel utilisateur: ')
   newuser= {'id': newid, 'name': newname}
   server['users'].append(newuser)
   afficher_users()
   menuprincipal()
   
def add_groupes():
   newidg= input('id nouveau groupe: ')
   newnameg= input('nom nouveau groupe: ')
   afficher_users()
   newmb= input('membres du groupe: ')
   newchannel= {'id': newidg, 'name': newnameg, 'member_ids': [newmb]}
   server['channels'].append(newchannel)
   afficher_groupes()
   menuprincipal()


print('=== Messenger ===')
print('x. Leave')
print('u.users')
print('g.groupes')
print('m.messages')
print('a.ajout users')
print('p.menu principal')
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
if choice == 'g':
   add_groupes()
else:
    print('Unknown option:', choice)


