from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sites = relationship("UserSite", back_populates="user")
    credentials = relationship("UserCredential", back_populates="user")
    training_records = relationship("TrainingRecord", back_populates="user")
    assignments = relationship(
    "TrainingAssignment",
    back_populates="user",
    foreign_keys="[TrainingAssignment.user_id]"
)

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String, unique=True)
    city = Column(String)
    state = Column(String)
    country = Column(String)

    users = relationship("UserSite", back_populates="site")
    assignments = relationship("TrainingAssignment", back_populates="site")


class UserSite(Base):
    __tablename__ = "user_site"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sites")
    site = relationship("Site", back_populates="users")


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrainingModule(Base):
    __tablename__ = "training_modules"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    records = relationship("TrainingRecord", back_populates="module")
    assignments = relationship("TrainingAssignment", back_populates="module")


class TrainingRecord(Base):
    __tablename__ = "training_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    module_id = Column(Integer, ForeignKey("training_modules.id", ondelete="CASCADE"))
    status = Column(String)  # completed, in_progress, failed
    score = Column(Integer)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="training_records")
    module = relationship("TrainingModule", back_populates="records")


class UserCredential(Base):
    __tablename__ = "user_credential"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    credential_name = Column(String, nullable=False)
    credential_value = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="credentials")


class TrainingAssignment(Base):
    __tablename__ = "training_assignments"

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("training_modules.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"))
    assigned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    assigned_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    status = Column(String, default="pending")

    module = relationship("TrainingModule", back_populates="assignments")
    user = relationship("User", foreign_keys=[user_id], back_populates="assignments")
    site = relationship("Site", back_populates="assignments")

class TrainingAttempt(Base):
    __tablename__ = "training_attempts"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("training_assignments.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    completed_at = Column(DateTime)
    score_percent = Column(Integer)
    passed = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)