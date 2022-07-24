from database import init_tables, async_session
from parsing import parsing_first_info
from database.tables.user import User
from sqlalchemy.future import select
from asyncio import run


async def a():
    aboba = {}
    async with async_session() as Asession:
        q = select(User)
        result = await Asession.execute(q)

        for user in result.all():
            user = user["User"]
            aboba[user.level] = aboba.get(user.level, 0) + 1
    print(aboba)


if __name__ == "__main__":
    run(init_tables())
    commnad = input("Command:\n")

    if "parsing" == commnad or commnad == "0":
        cookie = input("cookie:\n")
        parsing_first_info(cookie)
    elif "calc" == commnad or commnad == "1":
        run(a())


