import logging
from Seed_data import AUTHOR_DATA

logger = logging.getLogger(__name__)


def insert_authors(conn):

    author_ids = {}
    try:
        with conn.cursor() as cur:
            for name, bio in AUTHOR_DATA:
                cur.execute('''
                    INSERT INTO authors(name, bio)
                    VALUES (%s, %s)
                    ON CONFLICT (name) DO UPDATE
                        SET bio = EXCLUDED.bio
                    RETURNING author_id
                ''', (name, bio))

                author_id = cur.fetchone()[0]
                author_ids[name] = author_id
                logger.info(f"{name} author_id -> {author_id}")

    except Exception as e:
        logger.error(f"Failed to insert authors: {e}")
        raise

    return author_ids
