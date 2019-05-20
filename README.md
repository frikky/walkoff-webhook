# Webhook implementation between TheHive and WALKOFF
* https://github.com/nsacyber/WALKOFF
* https://github.com/TheHive-Project/TheHive

More selfmade at https://github.com/frikky/walkoff-apps

## Run - Standalone
```bash
git clone https://github.com/frikky/walkoff-webhook
cd walkoff-webhook
pip3 install -r requirements.txt
python3 walkoff-webhook.py
```

### Run - Docker - You will need to change the url in the python script to not be localhost
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

## ERRORS:
Traceback (most recent call last):
  File "app.py", line 89, in <module>
    asyncio.run(Helper.run(), debug=True)
  File "/usr/local/lib/python3.7/asyncio/runners.py", line 43, in run
    return loop.run_until_complete(main)
  File "/usr/local/lib/python3.7/asyncio/base_events.py", line 584, in run_until_complete
    return future.result()
  File "/app/walkoff_app_sdk/app_base.py", line 167, in run
    await app.get_actions()
  File "/app/walkoff_app_sdk/app_base.py", line 106, in get_actions
    await self.execute_action(action)
  File "/app/walkoff_app_sdk/app_base.py", line 142, in execute_action
    await self.redis.xadd(results_stream, {action.execution_id: message_dumps(action_result)})
  File "/app/common/message_types.py", line 7, in message_dumps
    return json.dumps(obj, cls=MessageJSONEncoder)
  File "/usr/local/lib/python3.7/json/__init__.py", line 238, in dumps
    **kw).encode(obj)
  File "/usr/local/lib/python3.7/json/encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/local/lib/python3.7/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
ValueError: Circular reference detected

