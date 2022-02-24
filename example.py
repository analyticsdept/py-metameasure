from metameasure import MetaMeasure
import json

m = MetaMeasure(max_size_bytes=500)

x = {
    'my_key': 'a string',
    '1': 222
}

print(m.bytes(kb=1, mb=1, gb=1, tb=1))

_ = [print(m.sizeof(json.dumps(x))) for i in range(0, 10)]