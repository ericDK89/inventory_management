"""File to create product schema
- ProductCreate: Just regular product with infos that must be send to create a product
- ProductOut: Product with all props, and add the id
"""

from pydantic import BaseModel


class ProductBase(BaseModel):
    """Class ProductBase to set all props to product"""

    name: str
    description: str
    price: float
    stock_quantity: int


class ProductCreate(ProductBase):
    """Class of product create with all bases props"""

    pass


class ProductOut(ProductBase):
    """Class of product out, the product that will be return, adding the id"""

    id: int

    class Config:
        """Makes easy to pydantic understand orm type
        removing the need to turn the orm to a dict
        with this config, you can pass the orm type directly
        """

        orm_mode = True