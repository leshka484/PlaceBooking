from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[list[User]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Role] = relationship(back_populates="users")

    bookings: Mapped[list[Booking]] = relationship(back_populates="user")
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(back_populates="user")


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(Text)

    resources: Mapped[list[Resource]] = relationship(back_populates="location")


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("resource_types.id"))

    location: Mapped[Location] = relationship(back_populates="resources")
    type: Mapped[ResourceType] = relationship(back_populates="resources")
    bookings: Mapped[list[Booking]] = relationship(back_populates="resource")
    tags: Mapped[list[ResourceTag]] = relationship(back_populates="resource")


class ResourceType(Base):
    __tablename__ = "resource_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    resources: Mapped[list[Resource]] = relationship(back_populates="type")
    tags: Mapped[list[Tag]] = relationship(back_populates="resource_type")


class ResourceTag(Base):
    __tablename__ = "resource_tags"
    
    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    resource_type_id: Mapped[int] = mapped_column(ForeignKey("resource_types.id"))
    resource_type: Mapped[str] = relationship(back_populates="tags")
    resource_links: Mapped[list[ResourceTag]] = relationship(back_populates="tag")
    pass


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint(
            "resource_id", "start_time", "end_time", name="uq_booking_resource_time"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="bookings")
    resource: Mapped[Resource] = relationship(back_populates="bookings")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime]

    user: Mapped[User] = relationship(back_populates="refresh_tokens")
