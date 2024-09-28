from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class CustomerManagementRole(Base):
  __tablename__ = "Customer_Management_Roles"
  id: Mapped[int] = mapped_column(primary_key=True)
  customer_management_id: Mapped[int] = mapped_column(db.ForeignKey('Customer_Accounts.id'))
  role_id: Mapped[int] = mapped_column(db.ForeignKey('Roles.id'))