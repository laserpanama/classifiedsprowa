from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.backend.models.account import Account, AccountCreate

async def get_account(db: AsyncIOMotorDatabase, account_id: str) -> Account | None:
    account = await db.accounts.find_one({"id": account_id})
    if account:
        return Account(**account)
    return None

async def get_accounts(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> List[Account]:
    accounts_cursor = db.accounts.find().skip(skip).limit(limit)
    accounts = await accounts_cursor.to_list(length=limit)
    return [Account(**account) for account in accounts]

async def create_account(db: AsyncIOMotorDatabase, account: AccountCreate) -> Account:
    new_account = Account(**account.dict())
    await db.accounts.insert_one(new_account.dict())
    return new_account

async def update_account(db: AsyncIOMotorDatabase, account_id: str, account_data: dict) -> bool:
    result = await db.accounts.update_one({"id": account_id}, {"$set": account_data})
    return result.modified_count > 0

async def delete_account(db: AsyncIOMotorDatabase, account_id: str) -> bool:
    result = await db.accounts.delete_one({"id": account_id})
    return result.deleted_count > 0
