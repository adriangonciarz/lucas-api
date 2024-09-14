import base64
from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    brand: str
    price: float
    currency: str
    description: str
    main_image_url: str
    image_urls: [str]


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/products")
async def get_all_products() -> list[Product]:
    all_products = [
        Product(name="Mezzabarba Skill 30 Head, Brown Tolex",
                brand="Mezzabarba",
                price=6500.00,
                currency="PLN",
                description=base64.b64encode("""<p>One of the best modern guitar amplifiers produced today. It is a variation on the Soldano SLO, in a smaller form factor, and with slightly less power. It has two channels that allow 3 configurations: Clean, crunch, and overdrive. Clean is a very tight, fairly compressed round sound, in crunch an aggressive, Marshall-like midrange begins to emerge, and overdrive is a combination of Marshall and Soldano (very aggressive, fast midrange). EQ allows for a palette ranging from fusion to hard rock to modern metal. Although it's an amp for the more aggressive players - it cuts through the mix very well and also allows for achieving the sound of 80s players, such as Steve Luakter or Steve Stevens. One of the most recognized users of Mezzabarba amplifiers is Erik Steckel.</p>
                    <p>It has EQ for both channels, an effects loop, two separate masters, depth and presence controls, and a power control. A footswitch with cable and power cable are included.</p>
                    <ul>
                    <li>100% engineered and handmade in Italy.</li>
                    <li>2 Channels: recallable via footswitch</li>
                    <li>The serial, full-tube effects loop is recallable via footswitch.</li>
                    <li>The bright switch on the Clean channel boosts mid-high frequencies for utmost transparency. Boost switch saturates channel.</li>
                    <li>Innovative Power Control “scales down” amp and allows it to perform at maximum saturation and dynamics even at very low volumes</li>
                    <li>Like all Mezzabarba amps, the power amp section features oversized transformers that deliver the best and most solid sound in any condition, at any volume.</li>
                    <li>Power amp tubes: EL34</li>
                    <li>Presence and Depth controls for ultimate sound chiseling</li>
                    </ul>
                    <!---->""".encode('utf-8')),
                main_image_url="https://cdn.shopify.com/s/files/1/0617/2262/4241/files/mezzabarba_skill-5.jpg?v=1721395311",
                image_urls = []
                ),
    ]
    return all_products


@app.get("/products/{product_id}")
async def read_product(product_id: int, q: Union[str, None] = None):
    return {"item_id": product_id, "q": q}
