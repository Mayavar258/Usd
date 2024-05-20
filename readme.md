# AntiSpam Telegram Userbot

##Features:-
- gban
- gmute
- ungmute
- ungban
- whois
- check help for more....

## How to host ?

```python
#Install python3 and pip3
sudo apt install python3 python3-pip python3-dev

#Install required python packages
pip3 install -U -r requirements.txt

#rename local.env.sample to local.env
mv local.env.sample local.env

#Generate user string, skip if have already
python3 genStr.py

#Fill the config values
nano local.env

#Start bot
python3 -m bot
```

## How to use in heroku?
#### fork the repo then goto heroku create app and select the forked repo then deploy, after deploying goto app settings and set enc configs.