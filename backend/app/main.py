from app.api.endpoints import chat, document
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



def create_application() -> FastAPI:
    app = FastAPI(title="Voice RAG Chatbot")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(chat.router, prefix="/chat", tags=["chat"])
    app.include_router(document.router, prefix="/document", tags=["document"])

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
