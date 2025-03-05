import asyncio
import json
from pathlib import Path
from typing import Any, Literal

import httpx
from selectolax.parser import HTMLParser

BASE_URL = "https://housing.com"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}
COOKIES = {
    "service": "buy",
    "category": "residential",
    "ssrExperiments": "edge_hp_how_it_works_server%3Dtrue%3Bkey_highlights%3Dtrue%3Bnewrelic_browser%3Dold_90%3Bchurnable_score_boost_experiment%3Dfalse%3Bsrp_images_auto_scroll%3Dfalse%3Bedge_rm_assistance%3Dtrue%3BnewRendering%3Dtrue",
    "experiments": "query_search%3Dfalse%3Bedge_loans_qc_profile_hook%3Dtrue%3Bedge_hp_lead_logic%3Dfalse%3Bedge_loans_user_contact_details%3Dfalse%3Bedge_hp_how_it_works_client%3Dtrue%3Bedge_pl_multi_offer%3Dtrue%3Bedge_hp_promise_nudge%3Dfalse%3Bedge_hp_custom_checkout%3Dfalse%3Bedge_hp_surprise_gift%3Dfalse",
    "organicOrDirectTraffic": "true",
    "_psid": "1",
    # "_uuid": "a443d928-a2db-41a7-f3da-9ade2130449",
    "traffic": "sourcemedium%3Ddirect%20%2F%20none%3B",
    "tvc_sm_fc_new": "direct%7Cnone",
    "tvc_sm_lc": "direct%7Cnone",
    "_cs_mk_ga": "0.43665213702889893_1719388955185",
    "outbrain_pid": "undefined",
    "taboola_pid": "undefined",
    "is_return_user": "true",
    "is_return_session": "true",
    # "userCity": "1cdd81323d5286e9fa47",
    # "cityUrl": "gurgaon",
}


async def fetch_properties_page(
    client: httpx.AsyncClient,
    city: str,
    page: int,
    *,
    errors: Literal["ignore", "raise"] = "ignore",
) -> bytes:
    # Update cookies for current request
    client.cookies.set("cityUrl", city)

    response = await client.get(f"/in/buy/{city}/{city}", params={"page": page},timeout=30)
    print("Fetching:", response.url)

    if response.status_code != 200:
        msg = (
            f"Bad status [{response.status_code}] while fetching properties details of "
            f"{city=} with {page=}."
        )
        if errors == "ignore":
            print(f"Ignoring {msg}")
            return b""  # return empty string in byte format
        raise httpx.HTTPStatusError(msg, request=response.request, response=response)
    return response.content


async def parse_data_from_html(
    html: bytes,
    *,
    errors: Literal["ignore", "raise"] = "ignore",
) -> list[dict[str, Any]]:
    parser = HTMLParser(html)
    selector = "script#initialState"
    data = parser.css_first(selector, strict=True)
    if data is None:
        msg = f"selector=`{selector}` not available."
        if errors == "ignore":
            print(f"Ignoring Error: {msg}")
            return []
    whole_data: dict[str, Any] = json.loads(json.loads(data.text()[36:-2]))
    properties = whole_data.get("searchResults", {}).get("data", {}).values()
    
    # Extract only essential fields
    filtered_properties = []
    for prop in properties:
        filtered_prop = {
            "title": prop.get("title"),
            "subtitle": prop.get("subtitle"),
            "property_type": prop.get("propertyType"),
            "possession_status": prop.get("currentPossessionStatus"),
            "price_range": prop.get("displayPrice", {}).get("displayValue"),
            "location": {
                "address": prop.get("address", {}).get("longAddress"),
                "locality": prop.get("polygonsHash", {}).get("locality", {}).get("name"),
                "city": prop.get("polygonsHash", {}).get("city", {}).get("name"),
                "coordinates": prop.get("coords")
            },
            "features": [
                {
                    "label": feature.get("label"),
                    "description": feature.get("description")
                }
                for feature in prop.get("features", [])
            ],
            "cover_image": prop.get("coverImage", {}).get("src"),
            "builder": prop.get("brands", [{}])[0].get("name") if prop.get("brands") else None,
            "configurations": [
                {
                    "type": config.get("label"),
                    "carpet_area": config.get("data", [{}])[0].get("areaConfig", [{}])[0].get("areaInfo", {}).get("displayArea"),
                    "price": config.get("data", [{}])[0].get("price", {}).get("displayValue")
                }
                for config in prop.get("details", {}).get("config", {}).get("propertyConfig", [])
            ]
        }
        filtered_properties.append(filtered_prop)
    
    return filtered_properties



def store_properties_details(data: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        data.extend(json.loads(path.read_bytes()))
    with path.open("w") as f:
        json.dump(data, f)


async def fetch_multi_page(
    client: httpx.AsyncClient,
    city: str,
    pages: tuple[int, int],
) -> list[dict[str, Any]]:
    html_list = await asyncio.gather(
        *[
            fetch_properties_page(client, city, page)
            for page in range(pages[0], pages[1] + 1)
        ],
    )
    all_data = await asyncio.gather(
        *[parse_data_from_html(html) for html in html_list],
    )
    return [j for i in all_data for j in i]


from flask import Flask, jsonify, request
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/api/properties', methods=['GET'])
async def get_properties():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers=HEADERS,
        cookies=COOKIES,
    ) as client:
        data = await fetch_multi_page(client, city, (1, 10))

        if not data:
            return jsonify({"error": "No data found"}), 404

        return jsonify(data), 200

if __name__ == "__main__":
    config = Config()
    config.bind = ["localhost:5000"]
    asyncio.run(serve(app, config))
