from datetime import datetime

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
    for i in range (len(server['users'])):
      print(server['users'][i]['id'],server['users'][i]['name'])
if choice == 'g':
    for i in range (len(server['channels'])):
      print(server['channels'][i]['id'],server['channels'][i]['name'],server['channels'][i]['member_ids'])
if choice == 'm':
    for i in range (len(server['messages'])):
      print(server['messages'][i]['sender_id'], server['messages'][i]['content'])
if choice == 'p':
   menuprincipal()
if choice == 'a':
   newid= input('id nouvel utilisateur: ')
   newname= input('nom nouvel utilisateur: ')
   newuser= {'id': newid, 'name': newname}
   server['users'].append(newuser)
   for i in range (len(server['users'])):
      print(server['users'][i]['id'],server['users'][i]['name'])
else:
    print('Unknown option:', choice)




