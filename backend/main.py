import asyncio  
import logging
from contextlib import asynccontextmanager
import spacy  
from sentence_transformers import SentenceTransformer 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    ALLOWED_ORIGINS, SPACY_MODEL_PRIMARY, SPACY_MODEL_SECONDARY, SENTENCE_TRANSFORMER_MODEL
)
from backend.api.routes import router

logger = logging.getLogger("ats_resume_scorer")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI ATS Scorer API...")
    loop = asyncio.get_event_loop()  


    logger.info(f"Loading spaCy model: {SPACY_MODEL_PRIMARY}")
    try:
        app.state.nlp = await loop.run_in_executor(
            None, spacy.load, SPACY_MODEL_PRIMARY
        )
        logger.info(f"Loaded {SPACY_MODEL_PRIMARY}")
    except OSError:
        logger.warning(f"{SPACY_MODEL_PRIMARY} failed -> fallback to {SPACY_MODEL_SECONDARY}")
        app.state.nlp = await loop.run_in_executor(
            None, spacy.load, SPACY_MODEL_SECONDARY
        )
        logger.info(f"Loaded {SPACY_MODEL_SECONDARY}")


    logger.info(f"Loading SentenceTransformer: {SENTENCE_TRANSFORMER_MODEL}")
    app.state.embedder = await loop.run_in_executor(
        None, SentenceTransformer, SENTENCE_TRANSFORMER_MODEL
    )
    logger.info(f"Loaded {SENTENCE_TRANSFORMER_MODEL}")

    logger.info("All models loaded. API ready to serve requests.")
    yield

    logger.info("Shutting down the API !!!")


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )