import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int
    name: str
    parent_id: int | None


class Product(BaseModel):
    uuid: UUID
    marketplace_id: int | None = Field(default=None)
    product_id: int
    title: str
    description: str | None = Field(default=None)
    brand: int | None = Field(default=None)
    seller_id: int | None = Field(default=None)
    seller_name: str | None = Field(default=None)
    first_image_url: str
    category_id: int
    category_lvl_1: str | None = Field(default=None)
    category_lvl_2: str | None = Field(default=None)
    category_lvl_3: str | None = Field(default=None)
    category_remaining: str | None = Field(default=None)
    features: str
    rating_count: int | None = Field(default=None)
    rating_value: float | None = Field(default=None)
    price_before_discounts: float | None = Field(default=None)
    discount: float | None = Field(default=None)
    price_after_discounts: float | None = Field(default=None)
    bonuses: int | None = Field(default=None)
    sales: int | None = Field(default=None)
    inserted_at: datetime.datetime
    updated_at: datetime.datetime
    currency: str
    barcode: int | None = Field(default=None)
