# Development

Install dependencies:

```bash
uv sync
```

Sort imports:

```bash
uv run ruff check --select I --fix
```

Format code:

```bash
uv run ruff format
```

Run unit tests:

```bash
uv run pytest
```

Start services:

```bash
docker compose up -w
```

Run integration tests:

```bash
uv run pytest -m integration
```

Stop services:

```bash
docker compose down
```
