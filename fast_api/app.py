from sqlite3 import Connection
from typing import List

from fastapi import FastAPI
from sqlalchemy import event, insert, desc, asc
from sqlalchemy.future import select
from sqlalchemy.orm import Mapper

import models
import schemas
from database import engine, session

app = FastAPI()


@event.listens_for(models.AllRecipes, 'after_insert')
def insert_all_recipes(mapper: Mapper, connection: Connection, target: models.AllRecipes) -> None:
    """
    Вставляет рецепт, добавленный в models.AllRecipes, в таблицу
    models.Recipes
    @param mapper: The mapper object
    @param connection: The connection to the database
    @param target: The instance of the object being inserted
    @return: None
    """
    connection.execute(
        insert(models.Recipe).values(
            title=target.title,
            time=target.time
        )
    )
    session.commit()


@app.on_event("startup")
async def startup() -> None:
    """
    Срабатывает при запуске, создаётся база данных, если ещё не существует
    @return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        await session.commit()


@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Срабатывает при остановке, закрывает сессию
    @return: None
    """
    async with session.begin():
        await session.commit()
    await session.close()
    await engine.dispose()


@app.post('/add_recipe/', response_model=schemas.AllRecipeOut)
async def add_recipe(recipe_with_desc: schemas.AllRecipeIn) -> models.AllRecipes:
    """
    Добавляет новый рецепт
    @param recipe_with_desc: schemas.AllRecipeIn
    @return: models.AllRecipes
    """
    new_recipe = models.AllRecipes(**recipe_with_desc.dict())
    session.add(new_recipe)  # использование существующей транзакции
    await session.commit()
    return new_recipe


@app.get('/recipes/', response_model=List[schemas.RecipeOut])
async def get_recipes() -> List[models.Recipe]:
    """
    Показывает все рецепты, сортирует по убыванию просмотров, если просмотры одинаковые -
    то по возрастанию времени приготовления.
    @return: List[models.Recipe]
    """
    res = await session.execute(select(models.Recipe).order_by(desc(models.Recipe.views), asc(models.Recipe.time)))
    return res.scalars().all()


@app.get('/recipes/{recipe_id}', response_model=List[schemas.AllRecipeOut])
async def get_recipes(recipe_id: int) -> List[models.AllRecipes]:
    """
    Показывает подробную информацию про рецепт по recipe_id, увеличивает views на 1.
    @param recipe_id: int
    @return: List[models.AllRecipes]
    """
    res = await session.execute(select(models.AllRecipes).filter_by(id=recipe_id))
    recipe = await session.get(models.Recipe, recipe_id)
    recipe.views += 1
    await session.commit()
    return res.scalars().all()
