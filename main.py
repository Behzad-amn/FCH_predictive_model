from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fch_predictive_model.core.model import FCHPerformanceModel  # Adjusted import

app = FastAPI()

# Set up Jinja2 templates (adjusted path for Docker)
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """
    Serve the main HTML page.
    
    Parameters:
    request (Request): The request object containing client request data.
    
    Returns:
    HTMLResponse: The HTML content for the root page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/run_model/", response_class=HTMLResponse)
def run_model(
    request: Request,
    product_model: str = Form(...),
    layer_count: int = Form(...),
    life_cycle: str = Form(...),
    mass_flow_dry: float = Form(...),
    mass_flow_wet: float = Form(...),
    temp_dry: int = Form(...),
    temp_wet: int = Form(...),
    humidity_dry: int = Form(...),
    humidity_wet: int = Form(...),
    pressure_dry: int = Form(...),
    pressure_wet: int = Form(...)
):
    """
    Run the FCH Performance Model with the provided inputs and return results.
    
    Parameters:
    request (Request): The request object containing client request data.
    product_model (str): The product model identifier.
    layer_count (int): The number of layers in the model.
    life_cycle (str): The lifecycle stage.
    mass_flow_dry (float): Mass flow rate for the dry side in kg/s.
    mass_flow_wet (float): Mass flow rate for the wet side in kg/s.
    temp_dry (int): Temperature on the dry side in Celsius.
    temp_wet (int): Temperature on the wet side in Celsius.
    humidity_dry (int): Relative humidity on the dry side in percent.
    humidity_wet (int): Relative humidity on the wet side in percent.
    pressure_dry (int): Pressure on the dry side in kPa.
    pressure_wet (int): Pressure on the wet side in kPa.
    
    Returns:
    HTMLResponse: The HTML content with the model results included.
    
    Raises:
    HTTPException: If an error occurs during model execution.
    """
    try:
        # Prepare the input data
        mass_flow_rates = {'dry': mass_flow_dry, 'wet': mass_flow_wet}
        temperatures = {'dry': temp_dry, 'wet': temp_wet}
        relative_humidities = {'dry': humidity_dry, 'wet': humidity_wet}
        pressures = {'dry': pressure_dry, 'wet': pressure_wet}

        # Instantiate the model with input data
        model = FCHPerformanceModel(
            product_model,
            layer_count,
            life_cycle,
            mass_flow_rates,
            temperatures,
            relative_humidities,
            pressures
        )

        # Compile the results
        results = model.compile_results()

        # Render the template with the results
        return templates.TemplateResponse("index.html", {"request": request, "results": results})

    except Exception as e:
        # Raise an HTTP exception with the error details
        raise HTTPException(status_code=500, detail=str(e))
