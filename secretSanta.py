#!/usr/bin/python3

import json
import random
import argparse
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class Participant(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return self.name


class Exclusion(object):
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2


class SecretSanta(object):
    def __init__(self, participants, exclusions=[]):
        self.participants = participants
        self.exclusions = exclusions

    def assign(self):
        if (len(self.participants) < 2):
            print("You must have at least two participants")
            exit(1)

        sanityCheckCounter = 0
        while True:
            random.shuffle(participants)
            assignments = {}
            for i, participant in enumerate(self.participants):
                source = participant
                target = participants[(i+1) % len(participants)]

                assignments[source.email] = target.email

            if(self.areAssignmentsAcceptable(assignments)):
                return assignments

            sanityCheckCounter += 1
            if sanityCheckCounter == 10_000:
                print('Impossible problem, check exclusions')
                exit(1)

    def areAssignmentsAcceptable(self, assignments):
        for exclusion in self.exclusions:
            if assignments[exclusion.user1.email] == exclusion.user2.email or assignments[exclusion.user2.email] == exclusion.user1.email:
                return False

        return True


def sendEmail(message, recipient):
    emailCredentials = None
    with open("secrets.json") as fin:
        emailCredentials = json.load(fin)

    subject = f'#SecretSanta{datetime.datetime.now().year} 🎄 ({recipient.name})'

    gmail_user = emailCredentials['email']
    gmail_pwd = emailCredentials['password']

    smtpMessage = MIMEMultipart('alternative')
    smtpMessage['Subject'] = subject
    smtpMessage['From'] = f'Santa Claus <{gmail_user}>'
    smtpMessage['To'] = f'{recipient.name} <{recipient.email}>'

    text = message
    html = f'''<html><head></head><body>{message}</body></html>'''

    part1 = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    part2 = MIMEText(html.encode('utf-8'), 'html', 'utf-8')

    smtpMessage.attach(part1)
    smtpMessage.attach(part2)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, [recipient.email], smtpMessage.as_string())
        server.close()
        print(f'Email sent')
    except:
        print(f'Failed to send mail to: {recipient}')
        raise


def notify(source, target, budget):
    if budget is None:
        budget = 20 #€

    message = f'''Ciao {source.name},<br />
    <br />
    Il Natale è alle porte, e Santa Claus ha bisogno del tuo aiuto per portare i regali! 🎁<br />
    <br />
    La persona a cui dovrai (segretamente! 🙊) fare il regalo è: <strong>{target.name}</strong> ({target.email})!<br />
    Ti ricordo che puoi scegliere un unico consigliere con cui confidarti, e che il budget massimo è di {budget}€.<br />
    <br />
    Buon lavoro, e che lo spirito dei maglioni brutti sia con te! 😜<br />
    <br />
    Babbo Natale 🎅<br />
    <img src="https://media.giphy.com/media/3o6ZtdulyqqoJjWB6U/giphy.gif" />'''

    # print(message)
    # print("<<<<<<<<<<<<<<<")
    sendEmail(message, source)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Secret Santa Fun!")
    parser.add_argument(
        'participants', help='File containing csv for participants')
    parser.add_argument("-n", "--exclusions",
                        help="File containing csv for exclusions")
    parser.add_argument("-b", "--budget",
                        help="Maximum budget (in €)")
    args = parser.parse_args()

    # Check secrets file
    if not os.path.exists("secrets.json"):
        print("You must have a secrets.json file with email credentials!")

    participants = []
    with open(args.participants) as fin:
        for line in fin:
            nameAndEmail = line.rstrip().split(',')
            participants.append(Participant(nameAndEmail[0], nameAndEmail[1]))

    exclusions = []
    if args.exclusions:
        with open(args.exclusions) as fin:
            for line in fin:
                namesPair = line.rstrip().split(',')
                participant1 = list(
                    p for p in participants if p.name == namesPair[0])[0]
                participant2 = list(
                    p for p in participants if p.name == namesPair[1])[0]

                exclusions.append(Exclusion(participant1, participant2))

    budget = None
    if args.budget:
        budget = args.budget

    ss = SecretSanta(participants, exclusions)
    assignments = ss.assign()

    # print(json.dumps(assignments))

    for participant in participants:
        target = [p for p in participants if p.email ==
                  assignments[participant.email]][0]
        
        notify(participant, target, budget)
