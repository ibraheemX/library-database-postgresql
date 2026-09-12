import logging
from Seed_data import CATEGORY_DATA

logger = logging.getLogger(__name__)


def insert_categories(conn):
    category_ids = {}
    try:
        with conn.cursor() as cur:
            for (name,) in CATEGORY_DATA:
                cur.execute('''
                    INSERT INTO categories (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO UPDATE
                        SET name = EXCLUDED.name
                    RETURNING category_id
                ''', (name,))

                category_id = cur.fetchone()[0]
                category_ids[name] = category_id
                logger.info(f"{name} category_id -> {category_id}")

    except Exception as e:
        logger.error(f"Failed to insert categories: {e}")
        raise

    return category_ids