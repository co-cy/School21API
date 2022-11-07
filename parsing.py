from asyncio import wait, new_event_loop, set_event_loop, get_event_loop, gather
from database.tables.user import User
from aiohttp import ClientSession
from config import PersonConfig
from database import async_session
from copy import deepcopy

_url = "https://edu.21-school.ru/services/graphql"


async def pasra(data):
    async with ClientSession() as Csession:
        async with Csession.post(_url, **data) as resp:
            if resp.status == 200:
                res_json = await resp.json()
                print(res_json)
                # Get all size
                # print(res_json["data"]["school21"]["searchByText"]["profiles"]["count"])
                async with async_session() as db_session:
                    for person in res_json["data"]["school21"]["searchByText"]["profiles"]["profiles"]:
                        del person["avatarUrl"]
                        del person["__typename"]
                        print(f"\tlogin: {person['login']}")
                        db_session.add(User(**person))
                    await db_session.commit()
            else:
                raise Exception(f"ERROR {resp}")


async def parsing_first_info(cookie):
    data = PersonConfig({
        "content-type": "application/json",
        "cookie": cookie,
    'User-Agent': 'Mozilla/5.0'})

    limits = 50
    offset = 0
    max_offset = 5000
    json_data = {"operationName": "getGlobalSearchResults",
                 "variables": {"searchString": "", "items": ["PROFILES"], "page": {"limit": limits, "offset": 0}},
                 "query": "query getGlobalSearchResults($searchString: String!, $items: [SearchItem]!, "
                          "$page: PagingInput!) {\n  school21 {\n    searchByText(searchString: $searchString, "
                          "items: $items, page: $page) {\n      profiles {\n        "
                          "...GlobalSearchProfilesSearchResult\n        __typename\n      }\n      projects {\n       "
                          " ...GlobalSearchProjectsSearchResult\n        __typename\n      }\n      __typename\n    "
                          "}\n    __typename\n  }\n}\n\nfragment GlobalSearchProfilesSearchResult on "
                          "ProfilesSearchResult {\n  count\n  profiles {\n    login\n    firstName\n    lastName\n    "
                          "level\n    avatarUrl\n    __typename\n  }\n  __typename\n}\n\nfragment "
                          "GlobalSearchProjectsSearchResult on ProjectsSearchResult {\n  count\n  projects {\n    "
                          "studentTaskId\n    status\n    finalPercentage\n    finalPoint\n    project {\n      "
                          "goalId\n      goalName\n      __typename\n    }\n    executionType\n    __typename\n  }\n  "
                          "__typename\n}\n"}
    background_tasks = list()
    while offset < max_offset:
        print("DATA", json_data)
        print(f"Parsing person: {offset}")
        background_tasks.append(pasra(deepcopy({"json": json_data, "headers": data})))
        offset += limits
        json_data["variables"]["page"]["offset"] = offset
    await gather(*background_tasks)
