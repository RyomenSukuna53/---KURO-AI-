from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DB_URI = "mongodb+srv://sufyan532011:2011@Kuroai.ftifibh.mongodb.net/?retryWrites=true&w=majority&appName=KuroAI"

client = AsyncIOMotorClient(MONGO_DB_URI)
db = client["KuroAI"]

# Collections
auth_col = db["authorized_users"]
ban_col = db["BANNED_USERS"]
order_col = db["orders"]              # All orders
pending_col = db["PENDING_ORDERS"]    # Yet to approve
completed_col = db["COMPLETED_ORDERS"]# Approved or rejected orders
