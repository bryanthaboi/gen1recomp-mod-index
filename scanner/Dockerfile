FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=America/New_York
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv ca-certificates curl git nodejs libicu74 libssl3t64 zlib1g tzdata && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
COPY scanner/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY scanner /opt/scanner
COPY scripts/lib/lua-scan.mjs /opt/scripts/lib/lua-scan.mjs
RUN useradd --create-home --uid 1001 scanner && mkdir /state /references && chown scanner /state
USER scanner
WORKDIR /opt/scanner
CMD ["python", "service.py"]
