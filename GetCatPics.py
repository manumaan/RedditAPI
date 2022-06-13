import requests
from json2table import convert

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('CLIENT ID', 'SECRET_TOKEN')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'user_name',
        'password': 'user_password'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'catpostv1/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
res = requests.get("https://oauth.reddit.com/r/cats/hot",
                   headers=headers)

#print(res.json())  # let's see what we get
json_object = res.json()

build_direction = "LEFT_TO_RIGHT"
table_attributes = {"style" : "width:100%"}
html = convert(json_object, build_direction=build_direction, table_attributes=table_attributes)

for post in res.json()['data']['children']:
    print(post['data']['title'])
    if post['data']['post_hint'] == 'image':
        print(post['data']['url_overridden_by_dest'])

#print(html)
