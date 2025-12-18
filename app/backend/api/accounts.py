from fastapi import APIRouter, Depends, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.backend.models.account import Account, AccountCreate
from app.backend.services import account_service

router = APIRouter()

# Dependency to get the DB connection
async def get_database(request: Request) -> AsyncIOMotorDatabase:
    return request.app.mongodb

@router.post("/accounts/", response_model=Account, tags=["accounts"])
async def create_account_endpoint(account: AccountCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await account_service.create_account(db=db, account=account)

@router.get("/accounts/", response_model=List[Account], tags=["accounts"])
async def read_accounts_endpoint(skip: int = 0, limit: int = 100, db: AsyncIOMotorDatabase = Depends(get_database)):
    accounts = await account_service.get_accounts(db=db, skip=skip, limit=limit)
    return accounts

@router.get("/accounts/{account_id}", response_model=Account, tags=["accounts"])
async def read_account_endpoint(account_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    db_account = await account_service.get_account(db=db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

# I will add update and delete endpoints too, as they are part of CRUD.
from pydantic import BaseModel
class AccountUpdate(BaseModel):
    email: str | None = None
    wanuncios_password: str | None = None
    is_active: bool | None = None

@router.patch("/accounts/{account_id}", response_model=Account, tags=["accounts"])
async def update_account_endpoint(account_id: str, account: AccountUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_data = account.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    success = await account_service.update_account(db=db, account_id=account_id, account_data=update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found or no changes made")

    updated_account = await account_service.get_account(db=db, account_id=account_id)
    if updated_account is None:
        raise HTTPException(status_code=404, detail="Account not found after update")
    return updated_account


@router.delete("/accounts/{account_id}", status_code=204, tags=["accounts"])
async def delete_account_endpoint(account_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    success = await account_service.delete_account(db=db, account_id=account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {} # No content
