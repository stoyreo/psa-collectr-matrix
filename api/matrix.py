"""
Vercel Serverless Function: Quantitative Investment Matrix API
Endpoint: /api/matrix
Method: GET
Returns: JSON with matrix analysis, summary, key drivers, risk flags
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Import the quantitative matrix module
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.quantitative_matrix import parse_csv, analyze_cards


def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        # Get CSV path (relative to Vercel deployment)
        csv_path = Path(__file__).parent.parent / "My Collection CSV - 19.csv"

        if not csv_path.exists():
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "error",
                    "message": f"CSV file not found at {csv_path}"
                })
            }

        # Parse CSV and analyze
        cards = parse_csv(str(csv_path))
        result = analyze_cards(cards)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }
