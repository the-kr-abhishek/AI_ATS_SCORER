# ── Base image ──
FROM python:3.11-slim

# ── System dependencies (WeasyPrint + python-magic need these) ──
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libmagic1 \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Set working directory ──
WORKDIR /app

# ── Copy and install Python dependencies ──
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Download spaCy models (primary + fallback) ──
RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_sm

# ── Copy project files ──
COPY . .

# ── HF Spaces expects port 7860 ──
ENV PORT=7860

# ── Environment variables (values set in HF Spaces secrets) ──
ENV ALLOWED_ORIGINS=""
ENV GROQ_API_KEY=""
ENV SENTENCE_TRANSFORMER_MODEL=""
ENV SUPABASE_ANON_KEY=""
ENV SUPABASE_KEY=""
ENV SUPABASE_URL=""

# ── Start the backend ──
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]