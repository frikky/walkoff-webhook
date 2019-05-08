# Webhook implementation between TheHive and WALKOFF
* https://github.com/nsacyber/WALKOFF
* https://github.com/TheHive-Project/TheHive

## Run - Standalone 
```bash
git clone https://github.com/frikky/walkoff-webhook
cd walkoff-webhook
pip3 install -r requirements.txt
python3 walkoff-webhook.py
```

## Run - Docker
```bash
git clone https://github.com/frikky/walkoff-webhook
cd walkoff-webhook
docker build . -t walkoff-webhook
docker run \
    -p 9091:9091 \
	walkoff-webhook
```

## What
Tries to start a workflow based on the name given from TheHive Webhook

## Why
Automation and orchestration :)
# walkoff-webhook
