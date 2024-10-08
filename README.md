# clex LLM for cpast

A W.I.P. implementation for LLM for clex, aimed to generate [clex](https://github.com/rootCircle/cpast/blob/54e7f6820aa97f70c25047afd4ce14042b25838a/docs/clex/CLEX_LANG_SPECS.md) from Human readable _Input Format_ and _Constraints_.

## Install & setup

Create a `.env` containing the gemini api key. Make sure you have [rye](https://rye-up.com/guide/installation/) installed on your local system.

```bash
make init
```

## Run

```bash
make run
```
or

```bash
rye run dev
```

## Help!

Go to `{base url}/docs` for help!

Example usage
```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/api/llm/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_format": "string",
  "constraints": "string"
}'
```

## Resources (Good to read)

https://arxiv.org/abs/2305.19234

https://github.com/berlino/grammar-prompting

https://github.com/r2d4/parserllm

https://matt-rickard.com/context-free-grammar-parsing-with-llms

https://matt-rickard.com/rellm

https://github.com/r2d4/rellm

https://doc.rust-lang.org/stable/reference/notation.html

https://github.com/rootCircle/cpast/blob/main/clex.specs.md




