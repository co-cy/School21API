from sqlalchemy import Column, String, Integer
from database import BaseTable


class User(BaseTable):
    __tablename__ = "user"

    login = Column(String(64), primary_key=True)
    userId = Column(String(36))
    studentId = Column(String(36))
    schoolId = Column(String(36))

    avatarUrl = Column(String(128))

    firstName = Column(String(32))
    lastName = Column(String(32))
    level = Column(Integer)
    xp = Column(Integer)

    coinsCount = Column(Integer)
    cookiesCount = Column(Integer)
    codeReviewPoints = Column(Integer)

    stageGroupId = Column(String(16))

    countFeedback = Column(Integer)
