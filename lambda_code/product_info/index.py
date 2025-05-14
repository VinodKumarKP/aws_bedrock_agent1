```python
import json
import os
import boto3
import logging
from typing import Dict, Any, List, Optional
import re

# Configure logging with more secure settings
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize boto3 clients
bedrock_runtime = boto3.client('bedrock-runtime')

# Mock product database (to be replaced with actual database)
PRODUCT_DATABASE = {
    "prod-001": {
        "productId": "prod-001",
        "name": "Premium Coffee Maker",
        "description": "High-end coffee maker with temperature control and built-in grinder",
        "price": 199.99,
        "inStock": True,
        "features": ["Temperature control", "Built-in grinder", "Timer", "12-cup capacity"]
    },
    # ... other products
}

def validate_product_id(product_id: str) -> bool:
    """Validate product ID format"""
    return bool(re.match(r'^prod-\d{3}$', product_id))

def sanitize_search_query(query: Optional[str]) -> Optional[str]:
    """Sanitize search query to prevent potential injection"""
    if not query:
        return None
    # Remove any potentially harmful characters
    return re.sub(r'[^\w\s]', '', query)

def validate_price_range(min_price: Optional[float], max_price: Optional[float]) -> bool:
    """Validate price range parameters"""
    if min_price is not None and max_price is not None:
        return 0 <= min_price <= max_price
    return True

def get_product_details(product_id: str) -> Dict[str, Any]:
    """Retrieve details for a specific product by ID"""
    if not validate_product_id(product_id):
        return {
            "error": "Invalid product ID format",
            "productId": product_id
        }

    product = PRODUCT_DATABASE.get(product_id)

    if not product:
        return {
            "error": "Product not found",
            "productId": product_id
        }

    return product

def search_products(query: Optional[str] = None,
                    category: Optional[str] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None) -> Dict[str, Any]:
    """Search for products based on criteria"""
    # Validate price range
    if not validate_price_range(min_price, max_price):
        return {
            "error": "Invalid price range",
            "results": [],
            "totalResults": 0
        }

    # Sanitize query
    sanitized_query = sanitize_search_query(query)

    results = []

    for product_id, product in PRODUCT_DATABASE.items():
        # Apply filters with more robust checking
        if sanitized_query and sanitized_query.lower() not in product["name"].lower() and \
           sanitized_query.lower() not in product["description"].lower():
            continue

        if min_price is not None and product["price"] < min_price:
            continue

        if max_price is not None and product["price"] > max_price:
            continue

        # Add to results as a summary
        results.append({
            "productId": product["productId"],
            "name": product["name"],
            "price": product["price"],
            "inStock": product["inStock"]
        })

    return {
        "results": results,
        "totalResults": len(results)
    }

def lambda_handler(event, context):
    """Main Lambda handler function with improved error handling"""
    try:
        # Log event without sensitive details
        logger.info(f"Received request for action group: {event.get('actionGroup', 'N/A')}")

        # Parse the input from Bedrock Agent
        action_group = event.get("actionGroup", "")
        api_path = event.get("apiPath", "")
        parameters = event.get("parameters", [])

        # Convert parameters list to dict for easier handling
        params = {param["name"]: param["value"] for param in parameters}

        response = None

        # Handle different API endpoints with specific error handling
        if api_path == "/getProductDetails":
            product_id = params.get("productId")
            if not product_id:
                response = {"error": "Product ID is required"}
            else:
                response = get_product_details(product_id)

        elif api_path == "/searchProducts":
            query = params.get("query")
            category = params.get("category")
            
            try:
                min_price = float(params.get("minPrice")) if params.get("minPrice") else None
                max_price = float(params.get("maxPrice")) if params.get("maxPrice") else None
            except ValueError:
                response = {"error": "Invalid price format"}
                
            if not response:
                response = search_products(query, category, min_price, max_price)

        else:
            response = {
                "error": "Unsupported API path",
                "apiPath": api_path
            }

        # Format response for Bedrock Agent
        bedrock_response = {
            "response": response
        }

        logger.info("Request processed successfully")
        return bedrock_response

    except Exception as e:
        # More specific logging without exposing sensitive details
        logger.error(f"Error in lambda handler: {type(e).__name__}")
        return {
            "response": {
                "error": "An unexpected error occurred during request processing"
            }
        }
```