# pyWechatProxyClient

A dedicated API client for [wenoptk](https://github.com/wenoptics)'s WechatProxy.

## Install

Simply `python setup.py install`

## Usage Examples

```
url = 'ws://192.168.1.161:5000/wechat'
client = Client(url)
wen = Friend(friend_id='wenoptics')

@client.register(wen)
def on_message(msg: Message):
    print("on Wen's message '{}'".format(msg.text))

    if msg.text == '#stop':
        print("stop called")
        client.stop()
        return
    return 'cool!'

client.start()
client.join()
```

## Dependencies
 - python-dateutil
 - websocket-client
 