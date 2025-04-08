from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, root_validator
from typing import List, Dict, Union, Optional
import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

app = FastAPI(
    title="Text Processing API",
    description="API for text tokenization and lemmatization",
    version="1.0.0"
)

class TokenizeRequest(BaseModel):
    """Request with either a single text or multiple texts."""
    text: Optional[str] = None
    texts: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "examples": [
                {"text": "The quick brown fox jumps over the lazy dog"},
                {"texts": ["The quick brown fox jumps", "Machine learning models"]}
            ]
        }
        
    @root_validator(pre=True)
    def check_text_or_texts(cls, values):
        """Validate that at least one of text or texts is provided."""
        if not values.get('text') and not values.get('texts'):
            raise ValueError('Either text or texts must be provided')
        return values

class TokenResultWithText(BaseModel):
    """Result with both original text and tokens."""
    text: str
    tokens: List[str]

class SingleTokenizeResponse(BaseModel):
    """Response for a single text input."""
    text: str
    tokens: List[str]
    
    class Config:
        exclude_none = True

class BatchTokenizeResponse(BaseModel):
    """Response for multiple text inputs."""
    results: List[TokenResultWithText]
    
    class Config:
        exclude_none = True

def process_text(text: str) -> List[str]:
    """Process a single text string and return tokenized results."""
    # Process with spaCy
    doc = nlp(text.lower())
    
    # Keep all tokens in original order, including duplicates
    tokens = [
        token.lemma_
        for token in doc
        if (not token.is_stop and                  # Remove stop words
            token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN'] and  # Only actual words
            len(token.lemma_) >= 2)                # Must be at least 2 chars
    ]
    
    return tokens

@app.post("/tokenize")
async def tokenize_text(request: TokenizeRequest):
    """
    Process text to return lemmatized tokens. Can handle either:
    - A single text string (using the 'text' field)
    - Multiple texts (using the 'texts' array field)
    
    Returns:
    - For single text: {"text": "...", "tokens": [...]}
    - For multiple texts: {"results": [{"text": "...", "tokens": [...]}, {"text": "...", "tokens": [...]}, ...]}
    """
    try:
        # Handle single text case
        if request.text is not None:
            tokens = process_text(request.text)
            return SingleTokenizeResponse(text=request.text, tokens=tokens)
            
        # Handle batch case
        if request.texts is not None:
            results = []
            for text in request.texts:
                tokens = process_text(text)
                results.append(TokenResultWithText(text=text, tokens=tokens))
            
            return BatchTokenizeResponse(results=results)
    
    except ValueError as e:
        # This catches the validator error
        raise HTTPException(status_code=400, detail=str(e))
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