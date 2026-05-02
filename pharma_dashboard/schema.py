import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship
import datetime as datetime_

Base = declarative_base()

# ============================================================
# USERS
# ============================================================
class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True, nullable=False)
    role = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime_.datetime.utcnow)

    sites = relationship("UserSite", back_populates="user")
    assignments = relationship(
        "TrainingAssignment",
        back_populates="user",
        foreign_keys="TrainingAssignment.user_id"
    )
    attempts = relationship("TrainingAttempt", back_populates="user")


# ============================================================
# SITES
# ============================================================
class Site(Base):
    __tablename__ = "sites"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    code = sqlalchemy.Column(sqlalchemy.String, unique=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)
    country = sqlalchemy.Column(sqlalchemy.String)

    users = relationship("UserSite", back_populates="site")
    assignments = relationship("TrainingAssignment", back_populates="site")


# ============================================================
# USER ↔ SITE ASSIGNMENTS
# ============================================================
class UserSite(Base):
    __tablename__ = "user_sites"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    site_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sites.id"), nullable=False)
    role_at_site = sqlalchemy.Column(sqlalchemy.String(100))
    start_date = sqlalchemy.Column(sqlalchemy.Date)
    end_date = sqlalchemy.Column(sqlalchemy.Date)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user = relationship("User", back_populates="sites")
    site = relationship("Site", back_populates="users")


# ============================================================
# TRAINING MODULES
# ============================================================
class TrainingModule(Base):
    __tablename__ = "training_modules"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(200), unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    assignments = relationship("TrainingAssignment", back_populates="module")


# ============================================================
# TRAINING ASSIGNMENTS
# ============================================================
class TrainingAssignment(Base):
    __tablename__ = "training_assignments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    module_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("training_modules.id"), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    site_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sites.id"))
    assigned_by = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    assigned_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime_.datetime.utcnow)
    due_date = sqlalchemy.Column(sqlalchemy.Date)
    status = sqlalchemy.Column(sqlalchemy.String(50), default="assigned")

    module = relationship("TrainingModule", back_populates="assignments")
    user = relationship("User", foreign_keys=[user_id], back_populates="assignments")
    assigner = relationship("User", foreign_keys=[assigned_by])
    site = relationship("Site", back_populates="assignments")
    attempts = relationship("TrainingAttempt", back_populates="assignment")


# ============================================================
# TRAINING ATTEMPTS
# ============================================================
class TrainingAttempt(Base):
    __tablename__ = "training_attempts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    assignment_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("training_assignments.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    completed_at = sqlalchemy.Column(sqlalchemy.DateTime)
    score_percent = sqlalchemy.Column(sqlalchemy.Integer)
    passed = sqlalchemy.Column(sqlalchemy.Boolean)

    assignment = relationship("TrainingAssignment", back_populates="attempts")
    user = relationship("User", back_populates="attempts")


# ============================================================
# TRAINING
# ============================================================
class Training(Base):
    __tablename__ = "training"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)


# ============================================================
# TRAINING RECORDS
# ============================================================
class TrainingRecord(Base):
    __tablename__ = "training_records"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    training_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("training.id"))
    completed_at = sqlalchemy.Column(sqlalchemy.DateTime)
    expiry_date = sqlalchemy.Column(sqlalchemy.Date)
    certificate_url = sqlalchemy.Column(sqlalchemy.String(500))
    status = sqlalchemy.Column(sqlalchemy.String(50))


# ============================================================
# USER CREDENTIALS
# ============================================================
class UserCredential(Base):
    __tablename__ = "user_credential"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    credential_type = sqlalchemy.Column(sqlalchemy.String(100))
    credential_value = sqlalchemy.Column(sqlalchemy.String(255))
    issued_date = sqlalchemy.Column(sqlalchemy.Date)
    expiry_date = sqlalchemy.Column(sqlalchemy.Date)