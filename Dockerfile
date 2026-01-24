FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_NO_SYNC=1

RUN \
    apt-get update && \
    apt-get install -y gettext && \
    \
    uv sync --no-default-groups --locked && \
    \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

COPY --chmod=755 run-server ./

EXPOSE 8000

CMD [ "/app/run-server" ]