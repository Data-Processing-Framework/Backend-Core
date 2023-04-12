from app import create_app
from dotenv import load_dotenv
import os

if not os.path.exists("./app/data/modules"):
    os.makedirs("./app/data/modules")

with open("./app/data/modules.json", "a+"):
    pass
with open("./app/data/graph.json", "a+"):
    pass

load_dotenv()

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
