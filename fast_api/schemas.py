from pydantic import BaseModel


class BaseRecipe(BaseModel):
    """
    Базовый класс для модели рецепта
    """
    title: str
    time: int
    views: int


class RecipeIn(BaseRecipe):
    ...


class RecipeOut(BaseRecipe):
    id: int

    class Config:
        orm_mode = True


class BaseAllRecipe(BaseModel):
    """
    Базовый класс для всех рецептов
    """
    title: str
    time: int
    ingredients: str
    description: str


class AllRecipeIn(BaseAllRecipe):
    ...


class AllRecipeOut(BaseAllRecipe):
    id: int

    class Config:
        orm_mode = True
