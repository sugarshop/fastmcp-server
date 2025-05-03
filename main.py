from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP

app = FastAPI(title="Weather MCP Service")

# 定义天气查询接口
@app.get("/weather/{city}")
async def get_weather(city: str):
    if city not in ["Beijing", "Shanghai", "Guangzhou"]:
        raise HTTPException(status_code=404, detail="City not supported")
    return {"city": city, "temperature": 25, "condition": "Sunny"}

# This endpoint will not be registered as a tool, since it was added after the MCP instance was created
@app.get("/new/endpoint/", operation_id="new_endpoint", response_model=dict[str, str])
async def new_endpoint():
    return {"message": "Hello, world!"}

# 先创建 MCP 实例
mcp = FastApiMCP(app)

# 在定义路由之前先挂载 MCP
mcp.mount()

# But if you re-run the setup, the new endpoints will now be exposed.
mcp.setup_server()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)