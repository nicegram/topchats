
import os
import urllib3
import json

stats = {}

def rm_stats(filter_type):
    if stats.get(filter_type):
        stats[filter_type] += 1
    else:
        stats[filter_type] = 1

url = os.environ.get('JSON_URL')

http = urllib3.PoolManager()
r = http.request('GET', url)
chats = json.loads(r.data.decode('utf-8'))
result = []


stop_words = ('porn', 'sex', '18+', '🔞', 'drug', 'nazi', 'binance', 'crypto')
ignore_usernames = ('vidnie_podrugi')
filter_usernames = ('newsob')

for chat in chats:
    if chat['u'] in filter_usernames:
        rm_stats('filter_username')
        continue
    if chat.get('a') and len(chat['a']) >= 2:
        age = 0
        try:
            age = int(chat['a'][:2])
        except ValueError:
            pass
        if age >= 16: # Some chats are really strange even for 16+
            rm_stats('age')
            continue
    if any(s in chat['t'] for s in stop_words) or (chat['u'] not in ignore_usernames and any(s in chat['u'] for s in stop_words)):
        rm_stats('stop_word')
        continue
    result.append(chat)

print(f'Total: {len(chats)}\nFiltered: {len(result)}\nDiff: {len(chats) - len(result)}')
for k, v in stats.items():
    print(k, v)

with open('topchats.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False)


    