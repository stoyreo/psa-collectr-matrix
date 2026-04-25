"""
Vercel Serverless Function: Health Check
Endpoint: /api/health
Method: GET
Returns: JSON with service status
"""

import json
from datetime import datetime


def handler(request):
    """
    Health check endpoint
    """
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "healthy",
            "service": "PSA x Collectr Tracer - Quantitative Matrix",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        })
    }
