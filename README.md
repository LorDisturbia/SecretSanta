# 🎅 Secret Santa Generator

Ho, ho, ho! It's that time of the year already. Your friends have been possessed by the Christmas spirit and they tasked you, the guy who "is good with computers", to generate some Secret Santa pairings.

Look no further! This simple script will help you set everything up.

## 🎁 What does this script do?

Given a list of participants, it assigns to each participant another one to which they must give a Christmas gift.

Then, it sends an email to each participant, letting them know who they were assigned.

> 📧 The email message is hardcoded in `secretSanta.py`. You can personalize it by changing it directly there.

## 🧑‍💻 Usage

First, clone this repository with:

```sh
git clone https://github.com/LorDisturbia/SecretSanta
```

Then, you need to configure the following files:

- `participants.txt`, a CSV list of users with their email addresses
- `secrets.json`, a gmail username and password that will be used to send the email. We suggest creating a custom one [with no 2FA](https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python).
- `exclusions.txt` (optional), a list of assignments that you want to be excluded from the possible drafts. Note that it's not commutative!

Finally, you can run the script with:

```sh
./secretSanta.py --budget 10 --exclusions exclusions.txt participants.txt
```

The budget is in euros, and `--exclusions exclusions.txt` is optional.