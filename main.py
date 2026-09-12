import logging

from db_connection import get_connection
from Schema import create_all_tables
from Authors import insert_authors
from Categories import insert_categories
from Books import insert_books, insert_book_authors, insert_book_copies
from Members import insert_members
from Borrowings import insert_borrowings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def has_book_copies(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM book_copies")
        return cur.fetchone()[0] > 0


def main():
    conn = None
    try:
        conn = get_connection()

        with conn:
            create_all_tables(conn)

            author_ids = insert_authors(conn)
            category_ids = insert_categories(conn)
            books_ids = insert_books(conn, category_ids)
            insert_book_authors(conn, author_ids, books_ids)
            member_ids = insert_members(conn)

            if has_book_copies(conn):
                logger.info("Book copies and borrowings already seeded, skipping.")
            else:
                copy_ids = insert_book_copies(conn, books_ids)
                insert_borrowings(conn, copy_ids, member_ids)

        logger.info("all data inserted and committed successfully")

    except Exception as e:
        logger.error(f"Failed to run the project: {e}")

    finally:
        if conn:
            conn.close()
            logger.info(" database connection closed")


if __name__ == '__main__':
    main()