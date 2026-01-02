from fastapi import FastAPI
from middleware.request_middleware import LoggingMiddleware
from routes.user_router import router as user_router
from routes.authentication_router import router as authentication_router
from routes.holiday_router import router as holiday_router


app = FastAPI(
    title="Enterprise User Management API/Swagger",
    version="1.0.0",
    description="Enterprise API - CRUD operations for users",
    swagger_ui_parameters={
         "tryItOutEnabled": True,
        "defaultModelsExpandDepth": -1  # This hides the 'Schemas' section at the bottom
    },
    docs_url="/api-explorer/swagger" 
)



app.add_middleware(LoggingMiddleware)

app.include_router(user_router)
app.include_router(authentication_router)
app.include_router(holiday_router)


@app.get("/")
async def root():
    return {"message": "Server is running"}







