import json


def generate_response(co2=0, energy=0, water=0, is_authorized=True):
    data = {
        "result": {
            "blocks": {
                "personalImpact": {
                    "data": {
                        "co2": co2,
                        "energy": energy,
                        "materials": 0,
                        "pineYears": 0,
                        "water": water
                    }
                }
            },
            "isAuthorized": is_authorized
        },
        "status": "ok"
    }

    return json.dumps(data)
