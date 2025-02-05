from flask import Flask, render_template, request
import asyncio
from agent.graph import graph, InputState, Configuration

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
async def index():  # Make the route asynchronous
    output_state = None
    error_message = None
    company_name = None
    founding_year = None
    founder_names = []
    product_description = None
    funding_summary = None
    open_jobs = []

    if request.method == "POST":
        try:
            # Retrieve form inputs
            company_name = request.form.get("company_name")
            max_search_queries = int(request.form.get("max_search_queries", 3))
            max_search_results = int(request.form.get("max_search_results", 10))
            max_reflection_steps = int(request.form.get("max_reflection_steps", 5))

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
            output_state = await graph.ainvoke(input=input_state, config=config_dict)

            # Process output
            company_name = output_state.get("company_name") or company_name
            founding_year = output_state.get("founding_year")
            founder_names = output_state.get("founder_names", [])
            product_description = output_state.get("product_description")
            funding_summary = output_state.get("funding_summary")
            open_jobs = output_state.get("open_jobs", [])

        except Exception as e:
            error_message = f"Error processing request: {str(e)}"
            app.logger.error(f"Full error: {str(e)}")
            app.logger.error("Traceback", exc_info=True)

    return render_template(
        "index.html",
        output_state=output_state,
        error_message=error_message,
        company_name=company_name,
        founding_year=founding_year,
        founder_names=founder_names,
        product_description=product_description,
        funding_summary=funding_summary,
        open_jobs=open_jobs,
    )

if __name__ == "__main__":
    app.run(debug=True)
