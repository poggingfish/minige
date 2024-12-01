import psd_tools
import os
import base64
from io import BytesIO
import json

def extract(psd):
    layers = {}
    with open(psd, "rb") as f:
        data = psd_tools.PSDImage.open(f)
        layers.update({
            "METADATA": {
                "width": data.width,
                "height": data.height
            }
        })
        for i in data._layers:
            b = BytesIO()
            i.topil().save(b, "png")
            img = base64.b85encode(b.getvalue())
            layers.update({
                i.name: {
                    "img_data": img.decode("ascii"),
                    "location": i.bbox,
                    "size": [i.width, i.height]
                }
            })
    return layers

if __name__ == "__main__":
    rooms = {}
    for i in os.listdir("assets"):
        if not i.endswith("psd"):
            continue
        print(i)
        rooms.update({
            os.path.basename(i).split(".")[0]: extract("assets/" + i)
        })
    json.dump(rooms, open("data/rooms.json", "w"))