from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage


# Aici gasim functiile pentru mail-uri
class mail:
          
        def open_deranjament(type_deranjament, contract):

            content= f'''Technical
        ######
        Name: NOC ROMANIA
        ######
        Phone: {contract}
        ######
        Email: monitor@jcs.jo
        ######
        Account number: {contract}
        ######
        Message:{type_deranjament}
        ######
        Call back: I want to be called on the number below
                        '''
            mail_deranjament = EmailMessage()
            mail_deranjament.add_header('Subject', "New Message From Jordan European Internet")
            mail_deranjament.set_content(content)
            #Ne conectam si trimitem mailul
            smtp_server = SMTP_SSL('mail.jcs.jo', port=SMTP_SSL_PORT)
            smtp_server.login('monitor@jcs.jo', 'tpS#Np^3n3vR6$v5')
            smtp_server.sendmail('monitor@jcs.jo', 'webmaster@jcs.jo', mail_deranjament.as_bytes())
            #Ne deconectam de pe server
            smtp_server.quit()
        
        def open_deranjament_attbuilding( location):
           
            content= (location)
            print(content)
            mail_deranjament = EmailMessage()
            mail_deranjament.add_header('Subject', "Atenuare pe cladire")
            mail_deranjament.set_content(content)
            #Ne conectam si trimitem mailul
            smtp_server = SMTP_SSL('mail.jcs.jo', port=SMTP_SSL_PORT)
            smtp_server.login('monitor@jcs.jo', 'tpS#Np^3n3vR6$v5')
            #smtp_server.sendmail('monitor@jcs.jo', 'dan@square-media.ro', mail_deranjament.as_bytes())
            #smtp_server.sendmail('monitor@jcs.jo', 'gb@jcs.jo', mail_deranjament.as_bytes())
            #Ne deconectam de pe server
            smtp_server.quit()