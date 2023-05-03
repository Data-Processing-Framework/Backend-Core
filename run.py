from app import create_app
from dotenv import load_dotenv
from app.helpers.controller import controller
import os

if not os.path.exists("./app/data/modules"):
    os.makedirs("./app/data/modules")
if not os.path.exists("./app/data/modules.json"):
    with open("./app/data/modules.json", "a+") as f:
        f.write("{}")
if not os.path.exists("./app/data/graph.json"):
    with open("./app/data/graph.json", "a+") as f:
        f.write("{}")

load_dotenv()

app = create_app()

controller()

if __name__ == "__main__":
    if os.getenv("DEBUG") == "1":
        import time

        while True:
            time.sleep(10)
    else:
        app.run(debug=True)
