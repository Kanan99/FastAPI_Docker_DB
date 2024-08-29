# Advanced Tips for FastAPI and RESTful API Design

## 1. Use Dependency Injection
FastAPI's dependency injection system is powerful. Use it for:
- Database connections
- Authentication
- Request validation
- Caching

Example:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

## 2. Implement Proper Status Codes
Use appropriate HTTP status codes for different scenarios:
- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## 3. Use Pydantic for Request and Response Models
Pydantic models provide automatic validation and serialization:

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str = None
    price: float

@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate):
    return item
```

## 4. Implement Pagination
For large datasets, implement pagination:

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100):
    return items[skip : skip + limit]
```

## 5. Use Background Tasks
For time-consuming operations, use background tasks:

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent in the background"}
```

## 6. Implement HATEOAS
HATEOAS (Hypertext As The Engine Of Application State) makes your API more discoverable:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = get_item(item_id)
    return {
        "id": item.id,
        "name": item.name,
        "links": [
            {"rel": "self", "href": f"/items/{item.id}"},
            {"rel": "delete", "href": f"/items/{item.id}"}
        ]
    }
```

## 7. Use API Versioning
Implement API versioning to maintain backward compatibility:

```python
from fastapi import APIRouter

router_v1 = APIRouter(prefix="/v1")
router_v2 = APIRouter(prefix="/v2")

@router_v1.get("/items/")
async def read_items_v1():
    return {"version": "v1", "items": get_items_v1()}

@router_v2.get("/items/")
async def read_items_v2():
    return {"version": "v2", "items": get_items_v2()}

app.include_router(router_v1)
app.include_router(router_v2)
```

## 8. Implement Rate Limiting
Use a library like `slowapi` to implement rate limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/limited")
@limiter.limit("5/minute")
async def limited():
    return {"data": "This is a limited endpoint"}
```

## 9. Use Caching
Implement caching for frequently accessed, rarely changing data:

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache:")

@app.get("/cached")
@cache(expire=60)
async def get_cached_data():
    return {"data": "This response will be cached"}
```

## 10. Implement Proper Error Handling
Use exception handlers for consistent error responses:

```python
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

These advanced tips will help you create more robust, efficient, and user-friendly APIs with FastAPI.

