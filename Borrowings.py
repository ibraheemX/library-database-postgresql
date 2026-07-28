import logging

logger = logging.getLogger(__name__)

BORROWINGS_DATA = [
    ('1984', 0, 'Ahmad Khaled', '2026-08-01'),
    ('1984', 1, 'Sara Ali', '2026-08-03'),
    ('totalitarianism', 0, 'Lina Youssef', '2026-08-10'),
]


def insert_borrowings(conn, copy_ids, member_ids):

    try:
        with conn.cursor() as cur:
            for book_name, copy_index, member_name, due_date in BORROWINGS_DATA:
                copy_id = copy_ids[book_name][copy_index]
                member_id = member_ids[member_name]

                cur.execute('''
                    INSERT INTO borrowings (copy_id, member_id, due_date)
                    VALUES (%s, %s, %s)
                    RETURNING borrowing_id
                ''', (copy_id, member_id, due_date))

                borrowing_id = cur.fetchone()[0]
                logger.info(
                    f"{member_name} borrowed copy {copy_id}, borrowing_id -> {borrowing_id}"
                )

    except Exception as e:
        logger.error(f"Failed to insert borrowings: {e}")
        raise