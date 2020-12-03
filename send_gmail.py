import os
import sys
import smtplib, ssl, argparse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#import credentials

def mp3_to_gmail(file_vec, mailing_list, subj, body):
    mailing_list = open(mailing_list, 'r')
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    [sender_email, password] = open('credentials.txt', 'r').readlines()
    message = body
    recipients = mailing_list.readlines()
    
    COMMASPACE = ', '
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subj
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender_email
    
    for mp3file in file_vec.split(","):
        try:
            with open(mp3file, 'rb') as outfile:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(outfile.read())
            encoders.encode_base64(msg)
            print("Uploading {}...".format(os.path.basename(mp3file)))
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(mp3file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info())
    outer.attach(MIMEText(message, 'plain'))
    full_email = outer.as_string()
        
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        try:
            for recipient in recipients:
                print("Sending email to " + str(recipient))
                server.sendmail(sender_email, recipient, full_email)
            print('Email sent to {} users!'.format(str(len(recipients))))
        except: 
            print('Email attempt unsuccessful. Error msg: ', sys.exc_info()[0])
            
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filenames", help="Comma-delimited list of files to email")
    parser.add_argument("-m", "--mailing_list", help=".txt file of relevant emails")
    parser.add_argument("-s", "--subject", help="Subject line of email")
    parser.add_argument("-c", "--content", help="Written content of email")
    
    args = parser.parse_args()
    mp3_to_gmail(file_vec=args.filenames, mailing_list=args.mailing_list, subj=args.subject, body=args.content)

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\nSuccessfully sent beats to mailing list.')
