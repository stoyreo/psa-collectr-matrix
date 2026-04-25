"""Main Entry Point - Pokémon TCG Portfolio Intelligence System"""
import sys
import logging
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from config import CSV_INPUT_PATH, EXCEL_OUTPUT_PATH, LOGGING_CONFIG
from refresh_live import live_refresh

logging.basicConfig(
    level=LOGGING_CONFIG["level"],
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOGGING_CONFIG["file"]),
    ],
)

logger = logging.getLogger(__name__)

def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("POKEMON TCG PORTFOLIO INTELLIGENCE SYSTEM")
    logger.info("=" * 80)
    
    try:
        logger.info("\nRunning live portfolio refresh (Collectr prices)...")
        refresh_result = live_refresh()

        status = refresh_result.get("status")
        if status == "success":
            
            logger.info("\n" + "=" * 80)
            logger.info("EXECUTION COMPLETE")
            logger.info("=" * 80)
            summary = refresh_result.get("summary", {})
            logger.info(f"Portfolio Size: {summary.get('card_count', 0)} cards")
            logger.info(f"Total Cost: ${summary.get('total_cost', 0):.2f}")
            logger.info(f"Total Market Value: ${summary.get('total_market_value', 0):.2f}")
            logger.info(f"Total P&L: ${summary.get('total_pnl', 0):+.2f}")
            logger.info(f"Return: {summary.get('pnl_pct', 0):.2f}%")
            logger.info(f"\nExcel Output: {EXCEL_OUTPUT_PATH}")
            logger.info(f"Log File: {LOGGING_CONFIG['file']}")
            logger.info("=" * 80)
            return 0
        else:
            logger.error(f"Refresh failed: {status}")
            return 1
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
