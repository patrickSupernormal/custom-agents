# Python FastAPI Patterns

```yaml
---
skill: python-fastapi-patterns
version: 1.0.0
used-by:
  - python-engineer
  - backend-engineer
  - api-architect
---
```

## 1. Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application factory
│   ├── config.py               # Pydantic settings
│   ├── dependencies.py         # Shared dependencies
│   ├── exceptions.py           # Custom exceptions
│   ├── middleware.py           # Custom middleware
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py           # Main API router
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # v1 router aggregator
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── users.py
│   │           ├── items.py
│   │           └── auth.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # Auth utilities
│   │   └── logging.py          # Logging configuration
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py          # Database session
│   │   ├── base.py             # Base model class
│   │   └── migrations/         # Alembic migrations
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # SQLAlchemy models
│   │   └── item.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Pydantic schemas
│   │   ├── item.py
│   │   └── common.py           # Shared schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py             # Base service class
│   │   ├── user.py
│   │   └── item.py
│   │
│   └── tasks/
│       ├── __init__.py
│       └── email.py            # Background tasks
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_api/
│   │   └── test_users.py
│   └── test_services/
│       └── test_user_service.py
│
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── docker-compose.yml
```

---

## 2. Application Factory Pattern

```python
# app/main.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.router import api_router
from app.config import settings
from app.db.session import engine
from app.exceptions import register_exception_handlers
from app.middleware import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")

    # Optionally create tables (use Alembic in production)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown
    await engine.dispose()
    print("Application shutdown complete")


def create_application() -> FastAPI:
    """Application factory for creating FastAPI instance."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # Add middleware (order matters - last added is first executed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(RequestLoggingMiddleware)

    # Register exception handlers
    register_exception_handlers(app)

    # Include routers
    app.include_router(api_router, prefix=settings.api_prefix)

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        return {"status": "healthy"}

    return app


app = create_application()
```

---

## 3. Configuration with Pydantic Settings

```python
# app/config.py
from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "FastAPI Application"
    app_version: str = "1.0.0"
    app_description: str = "Production-ready FastAPI application"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # API
    api_prefix: str = "/api"

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/dbname"
    )
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_echo: bool = False

    # Security
    secret_key: str = Field(min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Redis (for caching/background tasks)
    redis_url: str = "redis://localhost:6379/0"

    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def async_database_url(self) -> str:
        """Ensure async driver is used."""
        url = str(self.database_url)
        if "postgresql://" in url and "asyncpg" not in url:
            return url.replace("postgresql://", "postgresql+asyncpg://")
        return url


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()
```

---

## 4. Database (Async SQLAlchemy, Session Management)

```python
# app/db/session.py
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import settings

# Create async engine
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_timeout=settings.database_pool_timeout,
    pool_pre_ping=True,  # Verify connections before use
    # Use NullPool for testing or serverless environments
    # poolclass=NullPool,
)

# Session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database sessions."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# app/db/base.py
from datetime import datetime
from typing import Any

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all models."""

    metadata = MetaData(naming_convention=convention)

    # Common columns for all models
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
```

---

## 5. Models and Pydantic Schemas

```python
# app/models/user.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.item import Item


class User(Base):
    """User model."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    bio: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


# app/models/item.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Item(Base):
    """Item model."""

    __tablename__ = "items"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title={self.title})>"


# app/schemas/common.py
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

DataT = TypeVar("DataT")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Generic paginated response."""

    items: list[DataT]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str
    success: bool = True


# app/schemas/user.py
from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from app.schemas.common import BaseSchema, TimestampMixin


class UserBase(BaseSchema):
    """Base user schema."""

    email: EmailStr
    full_name: str | None = Field(None, max_length=255)
    bio: str | None = Field(None, max_length=1000)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseSchema):
    """Schema for updating a user."""

    full_name: str | None = Field(None, max_length=255)
    bio: str | None = Field(None, max_length=1000)
    password: str | None = Field(None, min_length=8, max_length=128)


class UserResponse(UserBase, TimestampMixin):
    """Schema for user response."""

    id: int
    is_active: bool
    is_verified: bool


class UserWithItems(UserResponse):
    """User response with items included."""

    from app.schemas.item import ItemResponse

    items: list[ItemResponse] = []


# app/schemas/item.py
from decimal import Decimal

from pydantic import Field

from app.schemas.common import BaseSchema, TimestampMixin


class ItemBase(BaseSchema):
    """Base item schema."""

    title: str = Field(max_length=255)
    description: str | None = Field(None, max_length=2000)
    price: Decimal = Field(ge=0, decimal_places=2)


class ItemCreate(ItemBase):
    """Schema for creating an item."""

    pass


class ItemUpdate(BaseSchema):
    """Schema for updating an item."""

    title: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price: Decimal | None = Field(None, ge=0, decimal_places=2)


class ItemResponse(ItemBase, TimestampMixin):
    """Schema for item response."""

    id: int
    owner_id: int
```

---

## 6. Router Patterns (CRUD, Nested)

```python
# app/api/router.py
from fastapi import APIRouter

from app.api.v1.router import v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")


# app/api/v1/router.py
from fastapi import APIRouter

from app.api.v1.endpoints import users, items, auth

v1_router = APIRouter()

v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(users.router, prefix="/users", tags=["Users"])
v1_router.include_router(items.router, prefix="/items", tags=["Items"])


# app/api/v1/endpoints/users.py
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_current_user, get_current_superuser
from app.models.user import User
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserWithItems
from app.services.user import UserService, get_user_service

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    summary="List all users",
    description="Retrieve a paginated list of users (admin only).",
)
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_superuser)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginatedResponse[UserResponse]:
    """List users with pagination."""
    return await service.get_paginated(page=page, page_size=page_size)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    """Create a new user account."""
    return await service.create(user_data)


@router.get(
    "/me",
    response_model=UserWithItems,
    summary="Get current user",
)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserWithItems:
    """Get the current authenticated user with their items."""
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
)
async def update_current_user(
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    """Update the current user's profile."""
    return await service.update(current_user.id, user_data)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
async def get_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Get a specific user by ID."""
    return await service.get_by_id(user_id)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Delete user",
)
async def delete_user(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_superuser)],
) -> MessageResponse:
    """Delete a user (admin only)."""
    await service.delete(user_id)
    return MessageResponse(message="User deleted successfully")


# Nested router for user items
@router.get(
    "/{user_id}/items",
    response_model=list[ItemResponse],
    summary="Get user's items",
)
async def get_user_items(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ItemResponse]:
    """Get all items belonging to a user."""
    from app.schemas.item import ItemResponse
    user = await service.get_by_id(user_id)
    return user.items


# app/api/v1/endpoints/items.py
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item import ItemService, get_item_service

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[ItemResponse],
    summary="List items",
)
async def list_items(
    service: Annotated[ItemService, Depends(get_item_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    owner_id: Annotated[int | None, Query()] = None,
) -> PaginatedResponse[ItemResponse]:
    """List items with optional filtering by owner."""
    filters = {}
    if owner_id:
        filters["owner_id"] = owner_id
    return await service.get_paginated(page=page, page_size=page_size, **filters)


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create item",
)
async def create_item(
    item_data: ItemCreate,
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ItemResponse:
    """Create a new item for the current user."""
    return await service.create(item_data, owner_id=current_user.id)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item",
)
async def get_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_item_service)],
) -> ItemResponse:
    """Get a specific item by ID."""
    return await service.get_by_id(item_id)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update item",
)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ItemResponse:
    """Update an item (owner only)."""
    return await service.update(item_id, item_data, owner_id=current_user.id)


@router.delete(
    "/{item_id}",
    response_model=MessageResponse,
    summary="Delete item",
)
async def delete_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> MessageResponse:
    """Delete an item (owner only)."""
    await service.delete(item_id, owner_id=current_user.id)
    return MessageResponse(message="Item deleted successfully")
```

---

## 7. Service Layer Pattern

```python
# app/services/base.py
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.exceptions import NotFoundError
from app.schemas.common import PaginatedResponse

ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class BaseService(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    """Base service with CRUD operations."""

    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> ModelT:
        """Get a single record by ID."""
        result = await self.session.get(self.model, id)
        if not result:
            raise NotFoundError(f"{self.model.__name__} with id {id} not found")
        return result

    async def get_all(self, **filters: Any) -> list[ModelT]:
        """Get all records with optional filters."""
        query = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        **filters: Any,
    ) -> PaginatedResponse[ModelT]:
        """Get paginated records with optional filters."""
        # Base query
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
                count_query = count_query.where(getattr(self.model, key) == value)

        # Get total count
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # Execute query
        result = await self.session.execute(query)
        items = list(result.scalars().all())

        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    async def create(self, data: CreateSchemaT, **extra: Any) -> ModelT:
        """Create a new record."""
        obj_data = data.model_dump()
        obj_data.update(extra)
        db_obj = self.model(**obj_data)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: int, data: UpdateSchemaT, **extra: Any) -> ModelT:
        """Update an existing record."""
        db_obj = await self.get_by_id(id)

        # Check ownership if owner_id provided
        if "owner_id" in extra:
            if hasattr(db_obj, "owner_id") and db_obj.owner_id != extra["owner_id"]:
                raise NotFoundError(f"{self.model.__name__} not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int, **extra: Any) -> None:
        """Delete a record."""
        db_obj = await self.get_by_id(id)

        # Check ownership if owner_id provided
        if "owner_id" in extra:
            if hasattr(db_obj, "owner_id") and db_obj.owner_id != extra["owner_id"]:
                raise NotFoundError(f"{self.model.__name__} not found")

        await self.session.delete(db_obj)
        await self.session.flush()


# app/services/user.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.db.session import get_async_session
from app.exceptions import ConflictError, UnauthorizedError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """User-specific service with authentication methods."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate, **extra) -> User:
        """Create user with hashed password."""
        # Check for existing email
        existing = await self.get_by_email(data.email)
        if existing:
            raise ConflictError("Email already registered")

        # Hash password
        hashed_password = get_password_hash(data.password)

        # Create user
        user = User(
            email=data.email,
            hashed_password=hashed_password,
            full_name=data.full_name,
            bio=data.bio,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, id: int, data: UserUpdate, **extra) -> User:
        """Update user, handling password changes."""
        user = await self.get_by_id(id)

        update_data = data.model_dump(exclude_unset=True)

        # Hash new password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> User:
        """Authenticate user with email and password."""
        user = await self.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid email or password")
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("User account is disabled")
        return user


async def get_user_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserService:
    """Dependency for UserService."""
    return UserService(session)


# app/services/item.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.base import BaseService


class ItemService(BaseService[Item, ItemCreate, ItemUpdate]):
    """Item-specific service."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Item)


async def get_item_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ItemService:
    """Dependency for ItemService."""
    return ItemService(session)
```

---

## 8. Dependencies (Auth, Database)

```python
# app/dependencies.py
from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_async_session
from app.exceptions import ForbiddenError, UnauthorizedError
from app.models.user import User
from app.services.user import UserService

# Security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)] = None,
) -> User:
    """Get the current authenticated user from JWT token."""
    if not credentials:
        raise UnauthorizedError("Authentication required")

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid token payload")
    except Exception:
        raise UnauthorizedError("Invalid or expired token")

    service = UserService(session)
    user = await service.get_by_id(int(user_id))

    if not user.is_active:
        raise UnauthorizedError("User account is disabled")

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure the current user is active."""
    if not current_user.is_active:
        raise ForbiddenError("Inactive user")
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure the current user is a superuser."""
    if not current_user.is_superuser:
        raise ForbiddenError("Superuser privileges required")
    return current_user


async def get_current_verified_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure the current user is verified."""
    if not current_user.is_verified:
        raise ForbiddenError("Email verification required")
    return current_user


# Optional dependencies
async def get_optional_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)] = None,
) -> User | None:
    """Get the current user if authenticated, None otherwise."""
    if not credentials:
        return None

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            return None
        service = UserService(session)
        return await service.get_by_id(int(user_id))
    except Exception:
        return None


# Rate limiting dependency
class RateLimiter:
    """Simple in-memory rate limiter (use Redis in production)."""

    def __init__(self, requests: int, period: int) -> None:
        self.requests = requests
        self.period = period
        self._cache: dict[str, list[float]] = {}

    async def __call__(
        self,
        x_forwarded_for: Annotated[str | None, Header()] = None,
    ) -> None:
        import time

        client_ip = x_forwarded_for or "unknown"
        now = time.time()

        if client_ip not in self._cache:
            self._cache[client_ip] = []

        # Remove old requests
        self._cache[client_ip] = [
            t for t in self._cache[client_ip]
            if now - t < self.period
        ]

        if len(self._cache[client_ip]) >= self.requests:
            from app.exceptions import RateLimitError
            raise RateLimitError("Rate limit exceeded")

        self._cache[client_ip].append(now)


rate_limiter = RateLimiter(requests=100, period=60)


# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    if extra_claims:
        to_encode.update(extra_claims)

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(subject: str | int) -> str:
    """Create a JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
```

---

## 9. Error Handling

```python
# app/exceptions.py
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppError):
    """Resource not found error."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
        )


class ConflictError(AppError):
    """Resource conflict error."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
        )


class UnauthorizedError(AppError):
    """Authentication required error."""

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )


class ForbiddenError(AppError):
    """Permission denied error."""

    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )


class ValidationError(AppError):
    """Validation error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class RateLimitError(AppError):
    """Rate limit exceeded error."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class ServiceError(AppError):
    """External service error."""

    def __init__(self, message: str, service_name: str) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="SERVICE_UNAVAILABLE",
            details={"service": service_name},
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers on the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
        # Log the error in production
        import logging
        logging.error(f"Unhandled exception: {exc}", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "details": {},
                }
            },
        )
```

---

## 10. Background Tasks

```python
# app/tasks/email.py
import asyncio
from typing import Any

from fastapi import BackgroundTasks

from app.config import settings


async def send_email_async(
    to: str,
    subject: str,
    body: str,
    template: str | None = None,
    context: dict[str, Any] | None = None,
) -> None:
    """Send email asynchronously (implement with your email provider)."""
    # Simulate email sending
    await asyncio.sleep(1)
    print(f"Email sent to {to}: {subject}")


def send_email_background(
    background_tasks: BackgroundTasks,
    to: str,
    subject: str,
    body: str,
) -> None:
    """Queue email for background sending."""
    background_tasks.add_task(send_email_async, to, subject, body)


# Usage in endpoint
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


@router.post("/send-notification")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    """Send notification email in background."""
    send_email_background(
        background_tasks,
        to=email,
        subject="Notification",
        body="This is your notification.",
    )
    return {"message": "Notification queued"}


# For more complex background tasks, use Celery
# app/tasks/celery_tasks.py
from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, to: str, subject: str, body: str) -> dict[str, str]:
    """Celery task for sending emails."""
    try:
        # Implement actual email sending
        print(f"Sending email to {to}: {subject}")
        return {"status": "sent", "to": to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task
def process_data_task(data: dict[str, Any]) -> dict[str, Any]:
    """Celery task for data processing."""
    # Heavy processing
    result = {"processed": True, "input": data}
    return result


# Using Celery tasks in endpoints
@router.post("/process")
async def process_data(data: dict[str, Any]) -> dict[str, str]:
    """Queue data processing task."""
    task = process_data_task.delay(data)
    return {"task_id": task.id, "status": "queued"}


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict[str, Any]:
    """Get status of a background task."""
    from celery.result import AsyncResult

    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
```

---

## 11. Testing Patterns

```python
# tests/conftest.py
import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import Settings
from app.db.base import Base
from app.db.session import get_async_session
from app.main import create_application


# Test settings override
def get_test_settings() -> Settings:
    return Settings(
        database_url="postgresql+asyncpg://test:test@localhost:5432/test_db",
        secret_key="test-secret-key-minimum-32-characters",
        debug=True,
    )


# Test database engine
test_engine = create_async_engine(
    get_test_settings().async_database_url,
    poolclass=NullPool,
    echo=False,
)

TestSessionFactory = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionFactory() as session:
        yield session
        await session.rollback()

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database session override."""
    app = create_application()

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def authenticated_client(
    client: AsyncClient,
    db_session: AsyncSession,
) -> AsyncGenerator[tuple[AsyncClient, dict[str, Any]], None]:
    """Create authenticated test client with a test user."""
    from app.core.security import create_access_token, get_password_hash
    from app.models.user import User

    # Create test user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("TestPassword123"),
        full_name="Test User",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create access token
    token = create_access_token(subject=user.id)

    # Add auth header
    client.headers["Authorization"] = f"Bearer {token}"

    yield client, {"user": user, "token": token}


# tests/test_api/test_users.py
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    """Test user creation endpoint."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "full_name": "New User",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient) -> None:
    """Test that duplicate emails are rejected."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "SecurePass123",
        "full_name": "First User",
    }

    # Create first user
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201

    # Try to create duplicate
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 409
    assert "already registered" in response.json()["error"]["message"].lower()


@pytest.mark.asyncio
async def test_get_current_user(authenticated_client: tuple) -> None:
    """Test getting current user info."""
    client, context = authenticated_client

    response = await client.get("/api/v1/users/me")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == context["user"].email


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient) -> None:
    """Test that unauthenticated requests are rejected."""
    response = await client.get("/api/v1/users/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_current_user(authenticated_client: tuple) -> None:
    """Test updating current user."""
    client, _ = authenticated_client

    response = await client.patch(
        "/api/v1/users/me",
        json={"full_name": "Updated Name"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"


# tests/test_services/test_user_service.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    """Test user creation via service."""
    service = UserService(db_session)

    user_data = UserCreate(
        email="service@example.com",
        password="SecurePass123",
        full_name="Service Test",
    )

    user = await service.create(user_data)

    assert user.id is not None
    assert user.email == "service@example.com"
    assert user.full_name == "Service Test"
    assert user.hashed_password != "SecurePass123"  # Password should be hashed


@pytest.mark.asyncio
async def test_create_duplicate_user(db_session: AsyncSession) -> None:
    """Test that duplicate user creation raises ConflictError."""
    service = UserService(db_session)

    user_data = UserCreate(
        email="duplicate@example.com",
        password="SecurePass123",
    )

    await service.create(user_data)

    with pytest.raises(ConflictError):
        await service.create(user_data)


@pytest.mark.asyncio
async def test_get_user_by_id(db_session: AsyncSession) -> None:
    """Test getting user by ID."""
    service = UserService(db_session)

    created = await service.create(
        UserCreate(email="byid@example.com", password="SecurePass123")
    )

    user = await service.get_by_id(created.id)

    assert user.id == created.id
    assert user.email == "byid@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(db_session: AsyncSession) -> None:
    """Test that NotFoundError is raised for missing user."""
    service = UserService(db_session)

    with pytest.raises(NotFoundError):
        await service.get_by_id(99999)


@pytest.mark.asyncio
async def test_authenticate_user(db_session: AsyncSession) -> None:
    """Test user authentication."""
    service = UserService(db_session)

    await service.create(
        UserCreate(email="auth@example.com", password="SecurePass123")
    )

    user = await service.authenticate("auth@example.com", "SecurePass123")

    assert user.email == "auth@example.com"


@pytest.mark.asyncio
async def test_authenticate_wrong_password(db_session: AsyncSession) -> None:
    """Test authentication with wrong password."""
    service = UserService(db_session)

    await service.create(
        UserCreate(email="wrongpass@example.com", password="SecurePass123")
    )

    with pytest.raises(UnauthorizedError):
        await service.authenticate("wrongpass@example.com", "WrongPassword")


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession) -> None:
    """Test user update."""
    service = UserService(db_session)

    user = await service.create(
        UserCreate(email="update@example.com", password="SecurePass123")
    )

    updated = await service.update(
        user.id,
        UserUpdate(full_name="Updated Name", bio="New bio"),
    )

    assert updated.full_name == "Updated Name"
    assert updated.bio == "New bio"


@pytest.mark.asyncio
async def test_delete_user(db_session: AsyncSession) -> None:
    """Test user deletion."""
    service = UserService(db_session)

    user = await service.create(
        UserCreate(email="delete@example.com", password="SecurePass123")
    )

    await service.delete(user.id)

    with pytest.raises(NotFoundError):
        await service.get_by_id(user.id)


# Integration test with mocking
@pytest.mark.asyncio
async def test_user_with_items(db_session: AsyncSession) -> None:
    """Test user with related items."""
    from app.models.item import Item
    from app.services.user import UserService

    service = UserService(db_session)

    user = await service.create(
        UserCreate(email="items@example.com", password="SecurePass123")
    )

    # Add items
    item = Item(title="Test Item", price=9.99, owner_id=user.id)
    db_session.add(item)
    await db_session.commit()

    # Refresh user to load items
    await db_session.refresh(user)

    assert len(user.items) == 1
    assert user.items[0].title == "Test Item"
```

---

## Quick Reference

### Common Imports

```python
from typing import Annotated
from fastapi import APIRouter, Depends, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field, EmailStr
```

### Dependency Injection Pattern

```python
async def get_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> MyService:
    return MyService(session)

@router.get("/items")
async def list_items(
    service: Annotated[MyService, Depends(get_service)],
) -> list[ItemResponse]:
    return await service.get_all()
```

### Response Model Pattern

```python
@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Item not found"},
    },
)
async def get_item(item_id: int) -> ItemResponse:
    ...
```

### Query Parameters with Validation

```python
@router.get("/search")
async def search(
    q: Annotated[str, Query(min_length=1, max_length=100)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SearchResponse:
    ...
```
