"""Class Models for Users.

All transaction to table Users, must defined here

"""


from datetime import datetime

from passlib.context import CryptContext 
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship

from database import Base, session
from .schemas import UserModel


passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EnumRole:
    SUPER_ADMIN = "superadmin"
    ADMIN = "admin"

class Users(Base):

    __tablename__ = "users"
    
    id_admin = Column(Integer,primary_key=True, index=True)
    nama_admin = Column(String, nullable=False, default="My Name")
    username = Column(String, nullable=False, unique=True, index=True, default="")
    password = Column(String, nullable=False, default="password")
    alamat = Column(String, default="")
    no_hp = Column(String, default="")
    hashed_password = Column(String, nullable=False, default=passwd_context.hash("password"))
    role = Column(String, nullable=False, default=EnumRole.ADMIN)
    is_active = Column(Boolean, default=False)
    is_super = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    token = relationship('AuthToken', back_populates='user')

    @staticmethod
    def exist(*args, **kwargs):
        return session.query(Users).filter(*args, **kwargs).first()

    @staticmethod
    def get_hash_password(password : str) -> str:
        return passwd_context.hash(password)
    
    def verify_password(self, password):
        return passwd_context.verify(password, self.hashed_password)

    @staticmethod
    def fromModel(user : UserModel):
        return Users(
            nama_admin=user.nama_admin,
            username=user.username,
            password=user.password,
            hashed_password=Users.get_hash_password(user.password),
            alamat=user.alamat,
            no_hp=user.no_hp,
            role=user.role,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
    
    
    @staticmethod
    def addUser(user : UserModel):
        user_exist = Users.exist(Users.username==user.username)
        if user_exist is not None:
            return None
        user_created = Users.fromModel(user)
        session.add(user_created)
        session.commit()
        return user_created
    
    @staticmethod
    def getUsers(limit, page):
        return session.query(Users).limit(limit).offset(limit*page).all()

    @staticmethod
    def getUsersBy(*args, **kwargs):
      return session.query(Users).filter(*args, **kwargs).first()

    def setNamaAdmin(self,newName):
      if newName is not None and newName:
        self.nama_admin=newName

    def setUsername(self,newUsername):
      if newUsername is not None and newUsername:
        self.username=newUsername

    def setPassword(self,newPassword):
      if newPassword is not None and newPassword:
        self.password=newPassword

    def setHashPassword(self,newHashPassword):
      if newHashPassword is not None and newHashPassword:
        self.password=Users.get_hash_password(newHashPassword)

    def setALamat(self,newAlamat):
      if newAlamat is not None and newAlamat:
        self.alamat=newAlamat

    def setNoHp(self,newNoHp):
      if newNoHp is not None:
        self.no_hp=newNoHp

    def setRole(self,newRole):
      if newRole is not None:
        self.role=newRole

    def setUpdatedAt(self):
        self.role=datetime.now()

    @staticmethod
    def update(user :UserModel,id):
      old_users : Users=Users.getUsersBy(Users.id_admin==id)
      if old_users is not None:
        old_users.setNamaAdmin(user.nama_admin)
        old_users.setUsername(user.username)
        old_users.setPassword(user.password)
        old_users.setALamat(user.alamat)
        old_users.setNoHp(user.no_hp)
        old_users.setRole(user.role)
        old_users.setUpdatedAt()
        session.commit()
      return old_users

    @staticmethod
    def delete(id):
      user: Users = Users.getUsersBy(Users.id_admin==id)
      if user is not None:
        session.delete(user)
        session.commit()
        return True
      return user