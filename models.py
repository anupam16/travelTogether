
from sqlalchemy import Column, Integer, String, Date
from database import Base

class Traveller(Base):
    __tablename__ = "travellers"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String, index=True)
    place_from = Column(String, index=True)
    place_to = Column(String, index=True)
    date = Column(Date, index=True)
