#!/usr/bin/env python

from fastapi import FastAPI
from pydantic import BaseModel, Field

from tasmota_control_center.modules.logger import rotate_log_file, setup_logger


class RootResponse(BaseModel):
    """Response model for root endpoint"""

    status: str = Field(..., description="Status of the API")
    message: str = Field(..., description="Message about the API")
    endpoints: dict[str, str] = Field(..., description="Available API endpoints")


class Info(BaseModel):
    """Response model for API information"""

    api_version: str = Field(..., description="API version")
    title: str = Field(..., description="API title")
    description: str = Field(..., description="API description")
    endpoints: dict[str, str] = Field(..., description="Available API endpoints")


app = FastAPI(title="Fahrplan Generator API", description="Generate transit timetables", version="1.0.0", root_path="/api")


@app.get("/", response_model=RootResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Tasmota Control Center API",
        "endpoints": {
            "GET /info": "Get API information",
        },
    }


@app.get("/info", response_model=Info)
async def get_info():
    """Get API information and available options"""
    return {
        "api_version": "0.0.1",
        "title": "Tasmota Control Center",
        "description": "Control tasmota devices",
        "endpoints": {
            "GET /": "Health check",
            "GET /info": "Get API information",
        },
    }


def main():
    import uvicorn

    rotate_log_file(compress=True)
    setup_logger()
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, forwarded_allow_ips="*")


if __name__ == "__main__":
    main()
