from sqlalchemy import Column, String, Integer


from database import Base

class Recipe(Base):
    """
    Recipe Model
    id - Integer Primary Key
    title - String, название блюда
    views - Integer, просмотры
    time - Integer, время приготовления в минутах
    """
    __tablename__ = 'Recipe'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    views = Column(Integer, index=True, default=0)
    time = Column(Integer, index=True)



class AllRecipes(Base):
    """
    AllRecipes Model
    id - Integer Primary Key
    title - String, название блюда
    time - Integer, время приготовления в минутах
    ingredients - String, необходимые ингредиенты
    description - String, описание блюда
    """
    __tablename__ = 'All_Recipes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,  index=True)
    time = Column(Integer, index=True)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
