#%%
from fastapi import FastAPI
import uvicorn
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from chatbot import app
import nest_asyncio
nest_asyncio.apply()

App = FastAPI(title="Dynamic chatbot App")

# Set all CORS enabled origins
App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(App, app)

if __name__ == "__main__":
   
    uvicorn.run(App, host="localhost", port=8080)






# %%
