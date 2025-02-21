from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

app = FastAPI(
    title="Tokenization and Lemmatization API",
    description="API for text tokenization and lemmatization",
    version="1.0.0"
)

class TokenizeRequest(BaseModel):
    text: str

class TokenizeResponse(BaseModel):
    tokens: List[str]

@app.post("/tokenize", response_model=TokenizeResponse)
async def tokenize_text(request: TokenizeRequest):
    """
    Process text to return lemmatized tokens.
    """
    try:
        # Process with spaCy
        doc = nlp(request.text.lower())
        
        # Only get actual word tokens
        tokens = {
            token.lemma_
            for token in doc
            if (not token.is_stop and                  # Remove stop words
                token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN'] and  # Only actual words
                len(token.lemma_) >= 2)                # Must be at least 2 chars
        }
        
        return TokenizeResponse(tokens=sorted(list(tokens)))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint health check"""
    return {"status": "healthy"}

@app.head("/")
async def head_root():
    """Root endpoint HEAD check"""
    return