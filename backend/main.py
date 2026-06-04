from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import template_router
from routers import beranda_router
from routers import auth
from routers import profile_router
from routers import user_router
from routers import evaluasi_router
from routers import cabang_router
from routers import spk_router
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

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

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

# Router pengguna (admin only)
app.include_router(
    user_router.router,
    prefix="/pengguna",
    tags=["Pengguna"]
)

# Router evaluasi
app.include_router(
    evaluasi_router.router,
    prefix="/evaluasi",
    tags=["Evaluasi"]
)

# Router cabang (admin only)
app.include_router(
    cabang_router.router,
    prefix="/cabang",
    tags=["Cabang"]
)

# Router SPK
app.include_router(
    spk_router.router,
    prefix="/spk",
    tags=["SPK"]
)

@app.get("/")
def root():
    return {
        "message": "Document Detection API Running"
    }