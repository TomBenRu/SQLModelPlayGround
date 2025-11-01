import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Name des Produkts"
    )
    description: str | None = Field(
        default=None,
        description="Beschreibung des Produkts"
    )
    price: float = Field(
        gt=0,
        description="Preis des Produkts"
    )
    in_stock: bool = Field(
        default=True,
        description="Ist das Produkt noch im Lager?"
    )
    sku: str = Field(
        max_length=50,
        unique=True,
        description="Stock Keeping Unit (SKU) des Produkts"
    )


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    updated_at: Optional[datetime.datetime] = Field(
        default=None
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    description: Optional[str] = None
    price: Optional[float] = Field(
        default=None,
        gt=0
    )
    in_stock: Optional[bool] = None
    sku: Optional[str] = Field(
        default=None,
        max_length=50
    )


class ProductRead(ProductBase):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
