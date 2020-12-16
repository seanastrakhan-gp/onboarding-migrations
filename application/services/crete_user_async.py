import asyncio
import aiohttp
from application.settings import ENV_HOST

def test_async(org_id, token, users, index):
    auth_header = {'Authorization': f"Bearer {token}"}
    url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
    print('Index {index}')
    connector = aiohttp.TCPConnector(verify_ssl=False)
    for user in users:
        try:
            r = yield from aiohttp.request('post', url, json=user, headers=auth_header, connector=connector)
        except Exception as e:
            print(f'bad eternal link {url}: {e}')
        else:
            print(f"Result: {r.content}")

async def make_request(session, payload, org_id, token):
    auth_header = {'Authorization': f"Bearer {token}"}
    url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
    async with session.post(url, json=payload, headers = auth_header) as response:
                data = await response.json()
                print(f"Student Response: {data}")

async def process_users(users, org_id, token, index=0):
    n_requests = 100
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[make_request(session, users[i], org_id, token) for i in range(len(users))]
        )

async def post_async_student(org_id, token, payload, index):
    auth_header = {'Authorization': f"Bearer {token}"}
    url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
    print('Index {index}', str(payload))
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers = auth_header) as response:
            data = await response.json()
            print(f"Student Response: {data}")

async def make_range(end):
    for i in range(0, end):
        yield i

async def do_post(session, url, token, payload):
    auth_header = {'Authorization': f"Bearer {token}"}
    print('About to do_post', str(payload))
    async with  session.post(url, json=payload, headers = auth_header) as response:
        data = await response.json()
        print(f"Student Response: {data}")

async def create_async_student(payload, org_id, token, user_count, index=0):
   print(f'INDEX NUMBER: {index}')
   url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
   async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for x in make_range(user_count):
            post_tasks.append(do_post(session, url, token, payload[x]))
        # now execute them all at once
        await asyncio.gather(*post_tasks)

def create_student(payload, org_id, index=0):
    print(f'INDEX NUMBER: {index}')
    url = f"{ENV_HOST}/classes/organization/{org_id}/student_user/"
    #auth_header = {'Authorization': f"Bearer {token}"}
    #response = requests.post(url, json=payload)
    response = authorized_request('post', url, json=payload)
    return response.content