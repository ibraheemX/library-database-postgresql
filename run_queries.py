

import logging

from db_connection import get_connection
from queries import (
    get_books_with_authors,
    get_books_with_categories,
    get_available_copies_count_per_book,
    get_active_borrowings,
    get_borrow_count_per_member,
    get_books_count_per_category,
    print_query_results,
)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    conn = None
    try:
        conn = get_connection()

        print_query_results(
            get_books_with_authors(conn)
        )

        print_query_results(

            get_books_with_categories(conn)
        )

        print_query_results(

            get_available_copies_count_per_book(conn)
        )

        print_query_results(

            get_active_borrowings(conn)
        )

        print_query_results(

            get_borrow_count_per_member(conn)
        )

        print_query_results(

            get_books_count_per_category(conn)
        )

    except Exception as e:
        logging.error(f"فشل تنفيذ الاستعلامات: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
