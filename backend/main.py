from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import crud, models, database
import random

app = FastAPI()

# Mount static files and templates
templates = Jinja2Templates(directory="frontend")

# Initialize DB
models.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    variant = random.choice(["A", "B"])
    template = "index.html" if variant == "A" else "variant_b.html"
    return templates.TemplateResponse(template, {"request": request, "variant": variant})

@app.post("/interact/")
async def track_interaction(
    variant: str = Form(...),
    event_type: str = Form(...),
    plan: str = Form(None),
    revenue: float = Form(None)
):
    crud.log_event(variant, event_type, plan, revenue)
    return JSONResponse({"status": "logged"})

@app.get("/results", response_class=HTMLResponse)
async def get_results(request: Request):
    metrics = crud.get_metrics()
    return templates.TemplateResponse("results.html", {"request": request, "metrics": metrics})

@app.get("/variant_a", response_class=HTMLResponse)
def show_variant_a():
    return templates.TemplateResponse("variant_a.html", {"request": Request})
