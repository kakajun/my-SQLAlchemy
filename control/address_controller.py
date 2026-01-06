from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from entity.database import get_session
from entity.models import User as UserModel, Address as AddressModel
from dto.schemas import Address, AddressCreate
from common.router import APIRouterPro

router = APIRouterPro(prefix="/addresses", tags=["addresses"], order_num=101)


@router.post("/users/{user_id}", response_model=Address)
def create_address_endpoint(user_id: int, address: AddressCreate, session: Session = Depends(get_session)):
    """为用户创建地址"""
    return create_address(user_id, address, session)


# 保持原有的业务逻辑函数
def create_address(user_id: int, address: AddressCreate, session: Session = Depends(get_session)):
    """为用户创建地址"""
    user = session.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 使用 Pydantic 验证后的数据
    db_address = AddressModel(
        email_address=address.email_address, user_id=user_id)
    session.add(db_address)
    session.commit()
    session.refresh(db_address)
    return db_address


@router.get("/users/{user_id}", response_model=list[Address])
def list_addresses_endpoint(user_id: int, session: Session = Depends(get_session)):
    """获取用户的所有地址"""
    return list_addresses(user_id, session)


# 保持原有的业务逻辑函数
def list_addresses(user_id: int, session: Session = Depends(get_session)):
    """获取用户的所有地址"""
    user = session.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    addresses = session.query(AddressModel).filter(
        AddressModel.user_id == user_id).all()
    return addresses


@router.get("/{address_id}", response_model=Address)
def get_address_endpoint(address_id: int, session: Session = Depends(get_session)):
    """获取指定地址"""
    return get_address(address_id, session)


# 保持原有的业务逻辑函数
def get_address(address_id: int, session: Session = Depends(get_session)):
    """获取指定地址"""
    address = session.query(AddressModel).filter(
        AddressModel.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="地址不存在")
    return address


@router.delete("/{address_id}")
def delete_address_endpoint(address_id: int, session: Session = Depends(get_session)):
    """删除地址"""
    return delete_address(address_id, session)


# 保持原有的业务逻辑函数
def delete_address(address_id: int, session: Session = Depends(get_session)):
    """删除地址"""
    address = session.query(AddressModel).filter(
        AddressModel.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="地址不存在")

    session.delete(address)
    session.commit()
    return {"message": "地址已删除"}
