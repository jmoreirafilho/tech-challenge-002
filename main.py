import uvicorn


if __name__ == "__main__":
    from app.api import aplicacao

    uvicorn.run(aplicacao, host="0.0.0.0", port=8000)

