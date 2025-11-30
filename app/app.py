from fastapi import FastAPI

from app.routers import (
    booking,
    locations,
    main,
    resource,
    resource_type,
    roles,
    tag,
    users,
)

app = FastAPI()

app.include_router(main.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(locations.router)
app.include_router(resource_type.router)
app.include_router(resource.router)
app.include_router(tag.router)
app.include_router(booking.router)