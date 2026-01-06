from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from entity.database import get_session
from entity.models import User as UserModel
from dto.schemas import User, UserCreate
from common.router import APIRouterPro

router = APIRouterPro(prefix="/users", tags=["users"], order_num=100)


@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, session: Session = Depends(get_session)):
    """创建新用户"""
    # 使用 Pydantic 验证后的数据
    db_user = UserModel(name=user.name, fullname=user.fullname)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# 保持原有的业务逻辑函数
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """创建新用户"""
    # 使用 Pydantic 验证后的数据
    db_user = UserModel(name=user.name, fullname=user.fullname)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=list[User])
def list_users_endpoint(session: Session = Depends(get_session)):
    """获取所有用户"""
    return list_users(session)


# 保持原有的业务逻辑函数
def list_users(session: Session = Depends(get_session)):
    """获取所有用户"""
    users = session.query(UserModel).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    """获取指定用户"""
    return get_user(user_id, session)


# 保持原有的业务逻辑函数
def get_user(user_id: int, session: Session = Depends(get_session)):
    """获取指定用户"""
    user = session.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: UserCreate, session: Session = Depends(get_session)):
    """更新用户信息"""
    return update_user(user_id, user, session)


# 保持原有的业务逻辑函数
def update_user(user_id: int, user: UserCreate, session: Session = Depends(get_session)):
    """更新用户信息"""
    db_user = session.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 使用 Pydantic 验证后的数据
    db_user.name = user.name
    db_user.fullname = user.fullname
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    """删除用户"""
    return delete_user(user_id, session)


# 保持原有的业务逻辑函数
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """删除用户"""
    db_user = session.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    session.delete(db_user)
    session.commit()
    return {"message": "用户已删除"}
