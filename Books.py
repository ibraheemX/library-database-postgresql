import logging
from Seed_data import BOOKS_DATA, BOOK_AUTHORS_DATA, BOOK_COPIES_DATA

logger = logging.getLogger(__name__)


def insert_books(conn, category_ids):

    books_ids = {}
    try:
        with conn.cursor() as cur:
            for title, published_date, category_name in BOOKS_DATA:
                category_id = category_ids[category_name]

                cur.execute('''
                    INSERT INTO books (title, published_date, category_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (title) DO UPDATE
                        SET published_date = EXCLUDED.published_date,
                            category_id = EXCLUDED.category_id
                    RETURNING book_id
                ''', (title, published_date, category_id))

                book_id = cur.fetchone()[0]
                books_ids[title] = book_id
                logger.info(f"{title} book_id -> {book_id}")

    except Exception as e:
        logger.error(f"Failed to insert books: {e}")
        raise

    return books_ids


def insert_book_authors(conn, author_ids, books_ids):

    try:
        with conn.cursor() as cur:
            for author_name, book_name in BOOK_AUTHORS_DATA:
                author_id = author_ids[author_name]
                book_id = books_ids[book_name]

                cur.execute('''
                    INSERT INTO book_authors(author_id, book_id)
                    VALUES (%s, %s)
                    ON CONFLICT (book_id, author_id) DO NOTHING
                ''', (author_id, book_id))

                logger.info(f"{author_name}: {book_name}")

    except Exception as e:
        logger.error(f"Failed to link books to authors: {e}")
        raise


def insert_book_copies(conn, books_ids):

    copy_ids = {}
    try:
        with conn.cursor() as cur:
            for book_name, num_copies in BOOK_COPIES_DATA:
                book_id = books_ids[book_name]
                copy_ids[book_name] = []

                for _ in range(num_copies):
                    cur.execute('''
                        INSERT INTO book_copies (book_id)
                        VALUES (%s)
                        RETURNING copy_id
                    ''', (book_id,))

                    copy_id = cur.fetchone()[0]
                    copy_ids[book_name].append(copy_id)
                    logger.info(f"{book_name} copy_id -> {copy_id}")

    except Exception as e:
        logger.error(f"Failed to create book copies: {e}")
        raise

    return copy_ids
