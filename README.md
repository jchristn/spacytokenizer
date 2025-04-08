# Tokenizer Microservice

This microservice exposes an API endpoint to take input text and then tokenize and lemmatize it.  This microservice uses the fantastic [spaCy](https://github.com/explosion/spaCy) library.

## Example (Non-Batch)
```
POST /tokenize
Content-Type: application/json
{
  "text": "The quick brown fox jumps over the lazy dog"
}

Response: 200/OK
{
  "text": "The quick brown fox jumps over the lazy dog",
  "tokens": [
    "quick",
    "brown",
    "fox",
    "jump",
    "lazy",
    "dog"
  ]
}
```

## Example (Batch)
```
POST /tokenize
Content-Type: application/json
{
  "texts": [
    "The quick brown fox jumps over the lazy dog",
    "Machine learning models are powerful tools"
  ]
}

Response: 200/OK
{
  "results": [
    {
      "text": "The quick brown fox jumps over the lazy dog",
      "tokens": [
        "quick",
        "brown",
        "fox",
        "jump",
        "lazy",
        "dog"
      ]
    },
    {
      "text": "Machine learning models are powerful tools",
      "tokens": [
        "machine",
        "learning",
        "model",
        "powerful",
        "tool"
      ]
    }
  ]
}
```

Use `GET` or `HEAD` to the root URL to validate connectivity.

# Download from Docker Hub

Use repository name `jchristn/spacytokenizer`, which can be found [here](https://hub.docker.com/r/jchristn/spacytokenizer).  The `Dockerfile` and scripts for building and running are also in the root of the repository.

# Version History

Refer to `CHANGELOG.md` for changelog and version history.
