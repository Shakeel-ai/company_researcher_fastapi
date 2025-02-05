from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from agent.graph import graph, InputState, Configuration
import asyncio


app = FastAPI()

# Mount the static directory for serving static files (like CSS, images, etc.)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Set up the template directory
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    # Initial state with no data yet
    return templates.TemplateResponse(
        "index.html", {"request": request, "output_state": None, "error_message": None}
    )


@app.post("/")
async def run_graph(
    request: Request,
    company_name: str = Form(...),
    max_search_queries: int = Form(),
    max_search_results: int = Form(),
    max_reflection_steps: int = Form(),
):
    output_state = None
    error_message = None
    founding_year = None
    founder_names = []
    product_description = None
    funding_summary = None
    open_jobs = []

    try:
        # Create InputState instance
        input_state = InputState(company=company_name)

        # Create Configuration instance
        config = Configuration(
            max_search_queries=max_search_queries,
            max_search_results=max_search_results,
            max_reflection_steps=max_reflection_steps,
        )

        # Convert config to proper dictionary
        config_dict = {
            "max_search_queries": config.max_search_queries,
            "max_search_results": config.max_search_results,
            "max_reflection_steps": config.max_reflection_steps
        }

        # ✅ Proper async execution
        task = asyncio.create_task(graph.ainvoke(input_state, config_dict))
        output_state = await task

        info = output_state.get("info", {})

        # Process output
        company_name = info.get("company_name") or company_name
        founding_year = info.get("founding_year")
        founder_names = info.get("founder_names", [])
        product_description = info.get("product_description")
        funding_summary = info.get("funding_summary")
        open_jobs = info.get("open_jobs", [])

    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        print(f"Full error: {str(e)}")  # Replace logging with print for now in FastAPI

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "output_state": output_state,
            "error_message": error_message,
            "company_name": company_name,
            "founding_year": founding_year,
            "founder_names": founder_names,
            "product_description": product_description,
            "funding_summary": funding_summary,
            "open_jobs": open_jobs,
        }
    )
