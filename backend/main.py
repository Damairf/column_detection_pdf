from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import template_router
from routers import detection_router
from routers import beranda_router
from routers import auth
from routers import profile_router
from database.database import engine
from database import models

# Buat tabel otomatis jika belum ada
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Document Detection API",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router auth (daftar & masuk)
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Router template
app.include_router(
    template_router.router,
    prefix="/template",
    tags=["Template"]
)

# Router detection
app.include_router(
    detection_router.router,
    prefix="/detection",
    tags=["Detection"]
)

# Router beranda (tabel dokumen)
app.include_router(
    beranda_router.router,
    prefix="/beranda",
    tags=["Beranda"]
)

# Router profile
app.include_router(
    profile_router.router,
    prefix="/profile",
    tags=["Profile"]
)


@app.get("/")
def root():
    return {
        "message": "Document Detection API Running"
    }