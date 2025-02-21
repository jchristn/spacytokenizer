# Tokenizer Microservice

This microservice exposes an API endpoint to take input text and then tokenize and lemmatize it.  This microservice uses the fantastic [spaCy](https://github.com/explosion/spaCy) library.

## Example
```
POST /tokenize
Content-Type: application/json
{
  "text": "Attached is some text that needs to be tokenized and lemmatized."
}

Response: 200/OK
{
    "tokens": [
        "attach",
        "lemmatize",
        "need",
        "text",
        "tokenize"
    ]
}
```

Use `GET` or `HEAD` to the root URL to validate connectivity.

# Download from Docker Hub

Use repository name `jchristn/spacytokenizer`, which can be found [here](https://hub.docker.com/r/jchristn/spacytokenizer).  The `Dockerfile` and scripts for building and running are also in the root of the repository.

# Version History

Refer to `CHANGELOG.md` for changelog and version history.
