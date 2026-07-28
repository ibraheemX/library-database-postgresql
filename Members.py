import logging
from Seed_data import MEMBER_DATA

logger = logging.getLogger(__name__)


def insert_members(conn):

    member_ids = {}
    try:
        with conn.cursor() as cur:
            for name, email in MEMBER_DATA:
                cur.execute('''
                    INSERT INTO members (name, email)
                    VALUES (%s, %s)
                    RETURNING member_id
                ''', (name, email))

                member_id = cur.fetchone()[0]
                member_ids[name] = member_id
                logger.info(f"{name} member_id -> {member_id}")

    except Exception as e:
        logger.error(f"Failed to insert members: {e}")
        raise

    return member_ids
