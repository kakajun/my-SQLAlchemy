from fastapi import Depends
from sqlalchemy.orm import Session
from entity.database import get_session
from dto.schemas import User, UserCreate
from common.router import APIRouterPro
from common.vo import DataResponseModel, CrudResponseModel
from service.user_service import UserService

router = APIRouterPro(prefix="/users", tags=["users"], order_num=100)


@router.post("/", response_model=DataResponseModel[User])
def create_user_endpoint(user: UserCreate, session: Session = Depends(get_session)):
    """创建新用户"""
    return UserService.create_user(user, session)


@router.get("/", response_model=DataResponseModel[list[User]])
def list_users_endpoint(session: Session = Depends(get_session)):
    """获取所有用户"""
    return UserService.list_users(session)


@router.get("/{user_id}", response_model=DataResponseModel[User])
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    """获取指定用户"""
    return UserService.get_user(user_id, session)


@router.put("/{user_id}", response_model=DataResponseModel[User])
def update_user_endpoint(user_id: int, user: UserCreate, session: Session = Depends(get_session)):
    """更新用户信息"""
    return UserService.update_user(user_id, user, session)


@router.delete("/{user_id}", response_model=CrudResponseModel)
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    """删除用户"""
    return UserService.delete_user(user_id, session)
