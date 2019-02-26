import imaplib
import os

# ===================================================
# INPUT
# ===================================================
folder = input("Qual é a pasta à ser lida? Default: inbox")
if(len(folder) == 0): folder = "inbox"

sender = input("Algum remetente específico?: ")
query = ''
if(len(sender) > 0):
    query = 'FROM "{}"'.format(sender)
else: query = 'FROM "no-reply@tumblr.com"'

subject = input("Algum assunto específico: ")
if(len(subject) > 0):
    query += ' SUBJECT "{}"'.format(subject)
else: query += ' SUBJECT "Os 5 blogs do seu futuro"'

# ===================================================
# Connect
# ===================================================
mail = imaplib.IMAP4_SSL(os.environ['HOST'])
mail.login(os.environ['EMAIL'], os.environ['PASSWORD'])
mail.list()

# Out: list of "folders" aka labels in gmail.
mail.select(folder) # connect to inbox.

# result, data = mail.search(None, '(FROM "no-reply@tumblr.com" SUBJECT "Os 5 blogs do seu futuro")' )
result, data = mail.search(None, '({})'.format(query) )

ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest

result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822)             for the given ID

id_email = data[0][0] # Mail ID
raw_email = data[0][1] # here's the body, which is raw text of the whole email

# ===================================================
# Show
# ===================================================
print('#####################')
print( id_email.decode("utf-8") )
print( raw_email.decode("utf-8") )
print('#####################')
# including headers and alternate payloads