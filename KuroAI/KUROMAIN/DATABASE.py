from motor.motor_asyncio import AsyncIOMotorClient 


MONGO_DB_URI = "mongodb+srv://sufyan532011:2011@Kuroai.ftifibh.mongodb.net/?retryWrites=true&w=majority&appName=KuroAI"

DATABASE = AsyncIOMotorClient(MONGO_DB_URI) 
auth_col = DATABASE["authorized_users"]
ban_col = DATABASE["BANNED_USERS"]
order_col = DATABASE["orders"]
pending_col = DATABASE["PENDING_ORDERS"]
completed_col = DATABASE["COMPLETED_ORDERS"]



