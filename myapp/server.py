import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI


def main():
    """WebApp server for local debug"""
    load_dotenv()
    uvicorn.run("myapp.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
