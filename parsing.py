from asyncio import wait, new_event_loop, set_event_loop
from database.tables.user import User
from aiohttp import ClientSession
from config import PersonConfig
from database import session
from copy import deepcopy

_url = "https://edu.21-school.ru/services/graphql"


async def pasra(data):
    async with ClientSession() as Csession:
        async with Csession.post(_url, **data) as resp:
            if resp.status == 200:
                res_json = await resp.json()

                for person in res_json["data"]["student"]["searchByText"]["profiles"]["profiles"]:
                    del person["avatarUrl"]
                    del person["__typename"]
                    print(f"\tlogin: {person['login']}")
                    session.add(User(**person))
                await session.commit()
            else:
                raise Exception(f"ERROR {resp}")


def parsing_first_info(cookie):
    data = PersonConfig({
        "content-type": "application/json",
        "cookie": cookie,
    'User-Agent': 'Mozilla/5.0'})

    limits = 200
    offset = 0
    json_data = {"operationName": "getGlobalSearchResults",
                 "variables": {"searchString": "", "items": ["PROFILES"], "page": {"limit": limits, "offset": 0}},
                 "query": "query getGlobalSearchResults($searchString: String!, $items: [SearchItem]!, "
                          "$page: PagingInput!) {\n  student {\n    searchByText(searchString: $searchString, "
                          "items: $items, page: $page) {\n      profiles {\n        ...GlobalSearchProfilesSearchResult\n "
                          "       __typename\n      }\n      projects {\n        ...GlobalSearchProjectsSearchResult\n    "
                          "    __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment "
                          "GlobalSearchProfilesSearchResult on ProfilesSearchResult {\n  count\n  profiles {\n    login\n "
                          "   firstName\n    lastName\n    level\n    avatarUrl\n    __typename\n  }\n  "
                          "__typename\n}\n\nfragment GlobalSearchProjectsSearchResult on ProjectsSearchResult {\n  "
                          "count\n  projects {\n    studentTaskId\n    status\n    finalPercentage\n    finalPoint\n    "
                          "project {\n      goalId\n      goalName\n      __typename\n    }\n    executionType\n    "
                          "__typename\n  }\n  __typename\n}\n"}
    loop = new_event_loop()
    set_event_loop(loop)
    try:
        background_tasks = list()
        while offset < 1400:
            print("DATA", json_data)
            print(f"Parsing person: {offset}")
            background_tasks.append(loop.create_task(pasra(deepcopy({"json": json_data, "headers": data}))))
            offset += limits
            json_data["variables"]["page"]["offset"] = offset
        loop.run_until_complete(wait(background_tasks))
    finally:
        loop.close()
