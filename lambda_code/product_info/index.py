import json
import os
import boto3
import logging
from typing import Dict, Any, List, Optional

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize boto3 clients
bedrock_runtime = boto3.client('bedrock-runtime')

# Mock product database
PRODUCT_DATABASE = {
    "prod-001": {
        "productId": "prod-001",
        "name": "Premium Coffee Maker",
        "description": "High-end coffee maker with temperature control and built-in grinder",
        "price": 199.99,
        "inStock": True,
        "features": ["Temperature control", "Built-in grinder", "Timer", "12-cup capacity"]
    },
    "prod-002": {
        "productId": "prod-002",
        "name": "Smart Blender",
        "description": "Programmable blender with multiple speed settings and preset programs",
        "price": 149.99,
        "inStock": True,
        "features": ["5 speed settings", "Ice crushing", "Smoothie preset", "Soup preset"]
    },
    "prod-003": {
        "productId": "prod-003",
        "name": "Stainless Steel Toaster",
        "description": "4-slice toaster with wide slots and bagel setting",
        "price": 79.99,
        "inStock": False,
        "features": ["4 slots", "Bagel setting", "Defrost function", "High-lift lever"]
    }
}


def get_product_details(product_id: str) -> Dict[str, Any]:
    """Retrieve details for a specific product by ID"""
    logger.info(f"Getting product details for ID: {product_id}")

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
    logger.info(f"Searching products with query: {query}, category: {category}, "
                f"price range: {min_price}-{max_price}")

    results = []

    for product_id, product in PRODUCT_DATABASE.items():
        # Apply filters
        if query and query.lower() not in product["name"].lower() and query.lower() not in product[
            "description"].lower():
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
    """Main Lambda handler function"""
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Parse the input from Bedrock Agent
        action_group = event.get("actionGroup", "")
        api_path = event.get("apiPath", "")
        parameters = event.get("parameters", [])

        # Convert parameters list to dict for easier handling
        params = {}
        for param in parameters:
            params[param["name"]] = param["value"]

        response = None

        # Handle different API endpoints
        if api_path == "/getProductDetails":
            product_id = params.get("productId")
            response = get_product_details(product_id)

        elif api_path == "/searchProducts":
            query = params.get("query")
            category = params.get("category")
            min_price = float(params.get("minPrice")) if params.get("minPrice") else None
            max_price = float(params.get("maxPrice")) if params.get("maxPrice") else None

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

        logger.info(f"Returning response: {json.dumps(bedrock_response)}")
        return bedrock_response

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "response": {
                "error": f"Error processing request: {str(e)}"
            }
        }