import uvicorn

from . import app

if __name__ == "__main__":
    print("Running with Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=1, log_level="debug")
