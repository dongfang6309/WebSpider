# coding=UTF-8<code>
import json

j = '{"name": "张佳豪", "age": 25, "Univ.": "Zhejiang Univ."}'
d = json.loads(j)
print(d, '--', type(d))

j2 = json.dumps(d, ensure_ascii=False)
print(j2, '--', type(j2))

s = '哈哈哈哈'
s1 = s.encode('utf-8')
s2 = s1.decode('utf-8')
print(s1, '---', type(s1))
print(s2, '---', type(s2))
