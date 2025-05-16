import scrapy
import json
import os

class DutchieDispensarySpider(scrapy.Spider):
    name = "dutchie_dispensaries"
    allowed_domains = ["dutchie.com"]
    graphql_url = "https://dutchie.com/graphql"

    def start_requests(self):
        variables = {
            "dispensaryFilter": {
                "medical": False,
                "recreational": False,
                "sortBy": "distance",
                "activeOnly": True,
                "country": "United States",
                "nearLat": 40.712749,
                "nearLng": -74.005994,
                "destinationTaxState": "NY",
                "distance": 3000,
                "openNowForPickup": False,
                "acceptsCreditCardsPickup": False,
                "acceptsDutchiePay": False,
                "offerCurbsidePickup": False,
                "offerPickup": True
            }
        }

        payload = {
            "operationName": "DispensarySearch",
            "variables": variables,
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "c15335c61b3aa861f8959251f17b6ba5f0a1d5f1d2bdd4c0d691b6bae6f3ceb3"
                }
            }
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://dutchie.com",
            "Referer": "https://dutchie.com/",
            "X-Requested-With": "XMLHttpRequest",
        }

        yield scrapy.Request(
            url=self.graphql_url,
            method="POST",
            body=json.dumps(payload),
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):
        data = json.loads(response.text)
        dispensaries = data.get("data", {}).get("filteredDispensaries", {})
        output_path = os.path.join("..","..","data" ,"response_data.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dispensaries, f, indent=2, ensure_ascii=False)

        for d in dispensaries:
            yield {
                "id": d.get("id"),
                "name": d.get("name"),
                "slug": d.get("slug"),
                "url": f"https://dutchie.com/dispensary/{d.get('cName')}",
                "city": d.get("location").get("city"),
                "state": d.get("state"),
                "lat": d.get("lat"),
                "lng": d.get("lng"),
                "address": d.get("address"),
            }

