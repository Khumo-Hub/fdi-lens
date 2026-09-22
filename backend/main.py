import os

import uvicorn

from app.create_db import create_database
from app.seed import seed_database


def start():
    create_database()
    seed_database()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                "8000",
            )
        ),
    )


if __name__ == "__main__":
    start()
