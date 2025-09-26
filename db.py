# Import standard logging module
import logging

# Import OS module for environment variable access
import os

# Load environment variables from a .env file
from dotenv import load_dotenv

# MongoDB client and error classes
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Typing helper for optional return values
from typing import Optional, List, Dict, Any

# ---------- Load .env file and initialize MongoDB URI ----------

# Load environment variables from the .env file into the environment
load_dotenv()

# Retrieve MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# ---------- Logger Setup ----------

# Create logger with the name "data_base"
logger = logging.getLogger("data_base")

# Configure basic logging level to INFO
logging.basicConfig(level=logging.INFO)

# ---------- MongoDB Connection Setup ----------

try:
    # Initialize MongoDB client with the URI
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable not set.")
    client = MongoClient(MONGO_URI)

    # Access the 'restaurant' database
    db = client["restaurant"]

    # Access the 'orders' collection within the 'restaurant' database
    orders_collection = db["orders"]

    # Log successful connection
    logger.info("MongoDB connection initialized successfully")

except (PyMongoError, ValueError) as e:
    # Log and raise any connection error
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

# ---------- Order Database Driver Class ----------

class DatabaseDriver:
    def __init__(self):
        # Initialize the collection reference to use in other methods
        self.collection = orders_collection

    # Create a new order in the MongoDB collection
    def create_order(self, name: str, phone: str, address: str, items: List[Dict[str, Any]]) -> Optional[dict]:
        order = {
            "name": name,
            "phone": phone,
            "address": address,
            "items": items,
            "status": "confirmed"
        }
        try:
            # Insert the order document into the MongoDB collection
            result = self.collection.insert_one(order)

            # Log the successful creation
            logger.info(f"Order created for phone: {phone} with id: {result.inserted_id}")

            # Return the order data
            return order

        except PyMongoError as e:
            # Log and return None in case of error
            logger.error(f"Error creating order: {e}")
            return None

    # Retrieve an order document by phone number
    def get_order_by_phone(self, phone: str) -> Optional[dict]:
        try:
            # Search for an order with the matching phone number, get the most recent one
            order = self.collection.find_one({"phone": phone}, sort=[("_id", -1)])

            # Log the result of the search
            if order:
                logger.info(f"Order found for phone: {phone}")
            else:
                logger.info(f"Order not found for phone: {phone}")

            # Return the order if found, else None
            return order

        except PyMongoError as e:
            # Log and return None if there's an error during fetch
            logger.error(f"Error fetching order: {e}")
            return None
