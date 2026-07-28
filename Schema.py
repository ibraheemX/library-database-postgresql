import logging

logger = logging.getLogger(__name__)


def create_all_tables(conn):

    try:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS authors(
                    author_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    bio TEXT NOT NULL
                );
            ''')

        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS categories(
                    category_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            ''')

        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS books(
                    book_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    published_date DATE NOT NULL,
                    category_id INTEGER REFERENCES categories(category_id)
                );
            ''')

        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS book_authors(
                    author_id INTEGER REFERENCES authors(author_id),
                    book_id INTEGER REFERENCES books(book_id),
                    PRIMARY KEY (book_id, author_id)
                );
            ''')

        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS book_copies(
                    copy_id SERIAL PRIMARY KEY,
                    book_id INTEGER NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
                    status VARCHAR(50) NOT NULL DEFAULT 'available'
                        CHECK (status IN ('available', 'borrowed', 'damaged', 'lost'))
                );
            ''')

        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS members(
                    member_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    joined_at TIMESTAMP DEFAULT NOW()
                );
            ''')

        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS borrowings(
                    borrowing_id SERIAL PRIMARY KEY,
                    copy_id INTEGER NOT NULL REFERENCES book_copies(copy_id) ON DELETE CASCADE,
                    member_id INTEGER NOT NULL REFERENCES members(member_id) ON DELETE CASCADE,
                    borrowed_at TIMESTAMP DEFAULT NOW(),
                    due_date DATE NOT NULL,
                    returned_at TIMESTAMP
                );
            ''')

        logger.info(" TABLES CREATED ")

    except Exception as e:
        logger.error(f" SOMTHING WENT WRONG: {e}")
        raise
