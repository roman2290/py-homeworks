#! C:\Users\User\Desktop\py-homeworks\2.3-aiohttp\venv\Scripts\python.exe
import json
import pydantic
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from models import Session, Advertisement, User, engine, init_db
from schema import CreateAdv, CreateUser
from sqlalchemy.ext.asyncio import AsyncSession
from aiohttp.web import HTTPConflict, HTTPNotFound





app = web.Application()


async def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True) 
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop('ctx', None)
        raise get_http_error(web.HTTPBadRequest, error)

def generate_error(error_cls, message):
    error = error_cls(
        text=json.dumps({"error": message}), content_type="application/json"
    )
    return error

async def get_user_by_id(session: AsyncSession, user_id) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise generate_error(HTTPNotFound, "user not found")
    return user

async def add_advert(session: AsyncSession, advert: Advertisement): 
    user = await session.get(User, advert.owner_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, 'Пользователь не существует')
    try:
        session.add(advert)
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, 'Advert already exists')
    return advert


async def add_user(session: AsyncSession, user: User): 
    try:
        session.add(user)
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, 'пользователь уже существует')
    return user


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def init_orm(app: web.Application):
    print("START")
    await init_db()
    yield
    await engine.dispose()
    print("FINISH")


app.cleanup_ctx.append(init_orm)
app.middlewares.append(session_middleware)


def get_http_error(error_class, message):
    error = error_class(
        body=json.dumps({"error": message}), content_type="application/json"
    )
    return error


async def get_advert_by_id(session: AsyncSession, advert_id: int) -> Advertisement: 
    advert = await session.get(Advertisement, advert_id)
    if advert is None:
        raise get_http_error(web.HTTPNotFound, 'Advert not found')
    return advert


class AdvertView(web.View):
    @property
    def advert_id(self):
        return int(self.request.match_info["advert_id"])
    
    @property
    def session(self):
        return self.request.session
    
    async def get(self):
        advert = await get_advert_by_id(self.session, self.advert_id)
        advert_json = await advert.dict
        return web.json_response(advert_json)

    async def post(self):
        json_data = await self.request.json()
        json_data = await validate(CreateAdv, json_data)
        advert = Advertisement(**json_data)
        await add_advert(self.session, advert)
        advert_json = await advert.dict
        response = web.json_response(advert_json)
        response.status_code = 201
        return response  

    async def delete(self):
        advert = await get_advert_by_id(self.session, self.advert_id)
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({'status': 'success'})

class UserView(web.View):
    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])
    
    async def get(self):
        user = await get_user_by_id(self.request.session, self.user_id)
        return web.json_response(user.dict)
    
    async def post(self):
        json_data = await self.request.json()
        json_data = await validate(CreateUser, json_data)
        user = User(**json_data)
        await add_user(self.session, user)
        response = web.json_response(user.dict)
        response.status_code = 201
        return response


app.add_routes(
    [
        web.post('/user', UserView),
        web.get('/user/{user_id}', UserView),
        web.post('/advert', AdvertView),
        web.get('/advert/{advert_id}', AdvertView),
        web.delete('/advert/{advert_id}', AdvertView),
    ]
)



# if __name__ == "__main__":
#     web.run_app(app())

web.run_app(app)