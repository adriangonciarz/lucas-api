import os
from typing import Optional, List

import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

load_dotenv()

app = FastAPI(
    title="Lucas API",
    summary="API delivering product feed to Lucas App",
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client.products
products_collection = db.get_collection("products")

PyObjectId = Annotated[str, BeforeValidator(str)]


class Product(BaseModel):
    """
    Container for a single product record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    brand: str = Field(...)
    price: float = Field(...)
    currency: Optional[str] = None
    description: str = Field(...)
    main_image: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "66e5e656780c8d12a96ebebb",
                "name": "Tom Anderson Classic S Sunburst 2001",
                "brand": "Tom Anderson Guitarworks",
                "price": 14000.0,
                "currency": None,
                "description": "base64_string",
                "main_image": "https://example.com/example_image.jpg"
            },
        },
    )


class ProductsCollection(BaseModel):
    products: List[Product]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get(
    "/products/",
    response_description="List all products",
    response_model=ProductsCollection,
    response_model_by_alias=False,
)
async def get_all_products():
    return ProductsCollection(products=await products_collection.find().to_list(1000))
