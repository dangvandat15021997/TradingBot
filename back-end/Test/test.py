from fastapi import FastAPI, Request, Form
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI() 


@app.get("/")
async def index(request: Request):
    test = 6
    test_param = request.query_params._dict
    if 'filter' in test_param:
        test = test_param['filter'] 
    
    list_test = [1,2,3,4]
    templates = Jinja2Templates(directory="templates")
    
    # test = 4
    # try:
    #     test = request.query_params['filter']
    # except:
    #     test = 5




    return templates.TemplateResponse("index_test.html", {"request": request, "test": test, 'list_test':list_test })    