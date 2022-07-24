from requests import post
from pprint import pprint

_url = "https://edu.21-school.ru/services/graphql"


json_data = {"operationName": "getGlobalSearchResults",
             "variables": {"searchString": "", "items": ["PROFILES"], "page": {"limit": 2, "offset": 0}},
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

json_data2 = {"operationName": "publicProfileGetPersonalInfo",
              "variables": {"userId": "da616513-f58c-4ae7-ac30-35092f2d5f39",
                            "studentId": "0470aff5-d828-42a7-8549-873e89be50c8",
                            "schoolId": "6bfe3c56-0211-4fe1-9e59-51616caac4dd",
                            "login": "nanadaug@student.21-school.ru"},
              "query": "query publicProfileGetPersonalInfo($userId: UUID!, $studentId: UUID!, $login: String!, "
                       "$schoolId: UUID!) {\n  student {\n    getAvatarByUserId(userId: $userId)\n    "
                       "getStageGroupS21PublicProfile(studentId: $studentId) {\n      waveId\n      waveName\n      "
                       "eduForm\n      __typename\n    }\n    getExperiencePublicProfile(userId: $userId) {\n      "
                       "value\n      level {\n        levelCode\n        range {\n          leftBorder\n          "
                       "rightBorder\n          __typename\n        }\n        __typename\n      }\n      "
                       "cookiesCount\n      coinsCount\n      codeReviewPoints\n      __typename\n    }\n    "
                       "getEmailbyUserId(userId: $userId)\n    getWorkstationByLogin(login: $login) {\n      "
                       "workstationId\n      hostName\n      row\n      number\n      __typename\n    }\n    "
                       "getClassRoomByLogin(login: $login) {\n      id\n      number\n      floor\n      __typename\n "
                       "   }\n    getFeedbackStatisticsAverageScore(studentId: $studentId) {\n      countFeedback\n   "
                       "   feedbackAverageScore {\n        categoryCode\n        categoryName\n        value\n        "
                       "__typename\n      }\n      __typename\n    }\n    __typename\n  }\n  user {\n    getSchool("
                       "schoolId: $schoolId) {\n      id\n      fullName\n      shortName\n      address\n      "
                       "__typename\n    }\n    __typename\n  }\n}\n"}

# cookie = "tmr_lvid=7c47045582124a26cedd818d77e9b63a; tmr_lvidTS=1648036055912; _ym_d=1648036056; _ym_uid=1648036056685165069; iap.uid=93e92f85f1c944b6815693726b1908cd; _tt_enable_cookie=1; _ttp=5ef58694-1c15-4a6d-91e3-ef30fee7d832; _gcl_au=1.1.817044179.1656764824; _gid=GA1.2.1360150302.1658155682; SI=c5ced420-633a-4d86-94b7-1e0c88ca8948; localeCode=en_EN; _ym_isad=1; _ga=GA1.1.1270576993.1648036056; tmr_reqNum=604; _ga_TR6E0P9RCL=GS1.1.1658673013.85.1.1658673797.0; tokenId=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJWd1EtbG12bldkbERPTVNxc0ZCX1otSVJVNWhHR19GUWpHbFk5Rng2dXBZIn0.eyJleHAiOjE2NTg2NzkxMDEsImlhdCI6MTY1ODY3ODUwMSwiYXV0aF90aW1lIjoxNjU4NjU0OTkwLCJqdGkiOiI5YTE3MzE0ZC0wMDA5LTQ4ZDMtOGQ3Zi05YzlmOGUzZjU4YTQiLCJpc3MiOiJodHRwczovL2F1dGguc2JlcmNsYXNzLnJ1L2F1dGgvcmVhbG1zL0VkdVBvd2VyS2V5Y2xvYWsiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiZGIxYjQwMWItZjAwNS00OTQ5LTgwNDItMzQyMzBjMDMxZGFjIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2Nob29sMjEiLCJub25jZSI6ImYwMjM0ZWQ5LTRkZjQtNGRkNi04YThjLTAzZWMyMmQzNWMzNyIsInNlc3Npb25fc3RhdGUiOiIzMWNlNjYxZi01NzRjLTRiYzQtOWIzYy0xMDliYzc5YzlhNDYiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydSIsImh0dHBzOi8vZWR1LWFkbWluLjIxLXNjaG9vbC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lZHVwb3dlcmtleWNsb2FrIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInVzZXJfaWQiOiJiYjhmNGVhNC1lYzU3LTRlZjQtYjA0MS1kZmY1NGE4MTI3ZjEiLCJuYW1lIjoiVGVzdF9Gcm9udGVudF9vc25vdmEgbmFuYWRhdWciLCJhdXRoX3R5cGVfY29kZSI6ImRlZmF1bHQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJuYW5hZGF1Z190ZXN0X2Zyb250ZW50X29zbm92YSIsImdpdmVuX25hbWUiOiJUZXN0X0Zyb250ZW50X29zbm92YSIsImZhbWlseV9uYW1lIjoibmFuYWRhdWciLCJlbWFpbCI6Im5hbmFkYXVnKyt0ZXN0X2Zyb250ZW50X29zbm92YUBzdHVkZW50LjIxLXNjaG9vbC5ydSJ9.Q6Xo60Lv601eh9Ppw2MbK3Gx-xWzk7WznNSABZOnQ1f6V6ONsFA-lwDQ0FTCPy2HCLNfpMUm3khTKbMF1XG7jzxGYeDrK8h4uKr_IO_ROeoLYlDSoqDBQ9BUCa05l_bQyv_juIHNOWwThRl45lustD2-umiLJGbJY7GL2bk8PoSlmy0Mof_ty-9bvVj58zE0H4Z3tBsihPqUszV1U2Auah63RhX4TqaBzKjL2gKOeltOx9KgBgq7JY9yC1QOxoWmct_sx1QwLp48RE2eEU09S7-_idlgu6Sm-fAss4yFpH49SbJztr3QsKTUH96luSOR6B7OukJL9rOfS-NpOx0U3g; _ga_94PX1KP3QL=GS1.1.1658673009.153.1.1658678502.0"
# cookie = "tmr_lvid=7c47045582124a26cedd818d77e9b63a; tmr_lvidTS=1648036055912; _ym_d=1648036056; _ym_uid=1648036056685165069; iap.uid=93e92f85f1c944b6815693726b1908cd; _tt_enable_cookie=1; _ttp=5ef58694-1c15-4a6d-91e3-ef30fee7d832; _gcl_au=1.1.817044179.1656764824; _gid=GA1.2.1360150302.1658155682; SI=c5ced420-633a-4d86-94b7-1e0c88ca8948; localeCode=en_EN; _ym_isad=1; _ga=GA1.1.1270576993.1648036056; tmr_reqNum=604; _ga_TR6E0P9RCL=GS1.1.1658673013.85.1.1658673797.0; tokenId=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJWd1EtbG12bldkbERPTVNxc0ZCX1otSVJVNWhHR19GUWpHbFk5Rng2dXBZIn0.eyJleHAiOjE2NTg2Nzk5NjMsImlhdCI6MTY1ODY3OTM2MywiYXV0aF90aW1lIjoxNjU4NjU0OTkwLCJqdGkiOiJmMjcwYzU4NS03Y2M5LTRjODYtYTU2MS1kOThlZjZmZTk0ODciLCJpc3MiOiJodHRwczovL2F1dGguc2JlcmNsYXNzLnJ1L2F1dGgvcmVhbG1zL0VkdVBvd2VyS2V5Y2xvYWsiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiZGIxYjQwMWItZjAwNS00OTQ5LTgwNDItMzQyMzBjMDMxZGFjIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2Nob29sMjEiLCJub25jZSI6ImI1NzgwOTM4LWNjYzAtNDNiMy04Njc0LTY5ZjY0YzIzOGE5YyIsInNlc3Npb25fc3RhdGUiOiIzMWNlNjYxZi01NzRjLTRiYzQtOWIzYy0xMDliYzc5YzlhNDYiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydSIsImh0dHBzOi8vZWR1LWFkbWluLjIxLXNjaG9vbC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lZHVwb3dlcmtleWNsb2FrIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInVzZXJfaWQiOiJiYjhmNGVhNC1lYzU3LTRlZjQtYjA0MS1kZmY1NGE4MTI3ZjEiLCJuYW1lIjoiVGVzdF9Gcm9udGVudF9vc25vdmEgbmFuYWRhdWciLCJhdXRoX3R5cGVfY29kZSI6ImRlZmF1bHQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJuYW5hZGF1Z190ZXN0X2Zyb250ZW50X29zbm92YSIsImdpdmVuX25hbWUiOiJUZXN0X0Zyb250ZW50X29zbm92YSIsImZhbWlseV9uYW1lIjoibmFuYWRhdWciLCJlbWFpbCI6Im5hbmFkYXVnKyt0ZXN0X2Zyb250ZW50X29zbm92YUBzdHVkZW50LjIxLXNjaG9vbC5ydSJ9.WVnl14qQTIvmTvXdPdttAhpQuOHmunUdJIZC-RdXr1E7iZVoIiA00N-NsmumJGHvFv7WAeDgmMHQEqxHXPZmUxWbHIbBgwFEMTEqmOdLRPDAed9MMSr1ocrv726EgOniHqUhz9L-l9CU3XgZQlQig4WLWoSS5drrT7BwCtZtam4MICRLUczkYMAAeN7F0XM-HE7FKCb4uVN73dxWY_2Wj4YOOyUpzG2iVqZVVaNY46nahGG0AXYkuxSDG-r0XNcLH4ELBfoYVxlIkw_B_CgQH0vo4PheQVIBEOtdkGJQ2qW7iwzVQ2ovVZa3KEjRf03-JY0gsCVsc_oCXtholdJ7LA; _ga_94PX1KP3QL=GS1.1.1658673009.153.1.1658679364.0"
cookie = "tmr_lvid=7c47045582124a26cedd818d77e9b63a; tmr_lvidTS=1648036055912; _ym_d=1648036056; _ym_uid=1648036056685165069; iap.uid=93e92f85f1c944b6815693726b1908cd; _tt_enable_cookie=1; _ttp=5ef58694-1c15-4a6d-91e3-ef30fee7d832; _gcl_au=1.1.817044179.1656764824; _gid=GA1.2.1360150302.1658155682; SI=c5ced420-633a-4d86-94b7-1e0c88ca8948; localeCode=en_EN; _ym_isad=1; _ga_TR6E0P9RCL=GS1.1.1658684820.86.1.1658684820.0; _ga=GA1.1.1270576993.1648036056; tmr_reqNum=614; _ga_94PX1KP3QL=GS1.1.1658687746.155.1.1658687747.0; tokenId=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJWd1EtbG12bldkbERPTVNxc0ZCX1otSVJVNWhHR19GUWpHbFk5Rng2dXBZIn0.eyJleHAiOjE2NTg2OTA3NDYsImlhdCI6MTY1ODY5MDE0NiwiYXV0aF90aW1lIjoxNjU4Njc5OTQ3LCJqdGkiOiIxMWIzMmY5Ni0yYzJkLTQ1MTMtOGExNi02ZjQ2YTcwMzI0ZGMiLCJpc3MiOiJodHRwczovL2F1dGguc2JlcmNsYXNzLnJ1L2F1dGgvcmVhbG1zL0VkdVBvd2VyS2V5Y2xvYWsiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYTY5ZWYwODktYzMyOC00N2I4LTllMjYtYWY1ZGMzMGU5NGIwIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2Nob29sMjEiLCJub25jZSI6IjFhNTgyMGNkLTgxOTItNDliNy1iYWVlLTIyNzA1MjFjMDExOSIsInNlc3Npb25fc3RhdGUiOiJlMDVkZjAxNy0yMmQ1LTRlMjgtYjljZi1hMjNjNTgzMTc2OGMiLCJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydSIsImh0dHBzOi8vZWR1LWFkbWluLjIxLXNjaG9vbC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwidXNlcl9pZCI6ImRhNjE2NTEzLWY1OGMtNGFlNy1hYzMwLTM1MDkyZjJkNWYzOSIsIm5hbWUiOiJOYW5hIERhdWdodGVybGVzcyIsImF1dGhfdHlwZV9jb2RlIjoiZGVmYXVsdCIsInByZWZlcnJlZF91c2VybmFtZSI6Im5hbmFkYXVnQHN0dWRlbnQuMjEtc2Nob29sLnJ1IiwiZ2l2ZW5fbmFtZSI6Ik5hbmEiLCJmYW1pbHlfbmFtZSI6IkRhdWdodGVybGVzcyIsImVtYWlsIjoibmFuYWRhdWdAc3R1ZGVudC4yMS1zY2hvb2wucnUifQ.iBRB6fM381Xt2hCB5DcLZMUqtuf8YX_t4BjXzt0KVozXNCMo_fVeSnmUg1iyZpGfxff9s5YIBV9YbTQ9ipz5-vVwHLnxAzYE-EJvW6Gjasxmk8B04d-mSi0Vhv_VEU1VGcNJUpMJDwc78p65qSOZNx8P8ChBzzBweO0cK0G3o7h1VsV0bm2aeCYVDgIObk5e6ZdM4abDDSR4hN-xaMLVlaRS73uvYoPf2AItxoRISNxPortSrA5zTEkSmlEbHrNDvm8C0imTqYX69NUsrElsxqsrjH2sIiSH80f4pTkpC4voTFK5Jh-QkUZf73XlkYJMulB8LjVBo4bqXEWzvawYjQ"
data_s = {
    "content-type": "application/json",
    "cookie": cookie,
    "schoolid": "6bfe3c56-0211-4fe1-9e59-51616caac4dd",
    "userrole": "ADMIN",
}
#
# data_s = {
#     "content-type": "application/json",
#     "cookie": cookie,
#     "schoolid": "8832e878-577e-4583-847a-d7e1db5d5507",
#     "userrole": "STUDENT",
# }

a = post(_url, json=json_data, headers=data_s)
print(a)
pprint(a.json())
# pprint(a.json().get("data").get("student").get("searchByText").get("profiles").get("profiles"))
