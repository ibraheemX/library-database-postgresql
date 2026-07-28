import logging

logger = logging.getLogger(__name__)


def get_books_with_authors(conn):


    with conn.cursor() as cur:
        cur.execute('''
            SELECT books.title, authors.name
            FROM books
            JOIN book_authors ON books.book_id = book_authors.book_id
            JOIN authors ON book_authors.author_id = authors.author_id
            ORDER BY books.title;
        ''')
        return cur.fetchall()






def get_books_with_categories(conn):

    with conn.cursor() as cur:
        cur.execute('''

            SELECT books.title, categories.name AS category_name
            FROM books
            LEFT JOIN categories ON books.category_id = categories.category_id
            ORDER BY books.title;
        '''
                    )
        return cur.fetchall()







def get_available_copies_count_per_book(conn):

    with conn.cursor() as cur:
        cur.execute('''
            SELECT books.title, COUNT(book_copies.copy_id) AS available_copies
            FROM books
            JOIN book_copies ON books.book_id = book_copies.book_id
            WHERE book_copies.status = 'available'
            GROUP BY books.title
            ORDER BY available_copies DESC;
        ''')
        return cur.fetchall()







def get_active_borrowings(conn):

    with conn.cursor() as cur:
        cur.execute('''
            SELECT members.name AS member_name,
                books.title AS book_title,
                borrowings.borrowed_at,
                borrowings.due_date
            FROM borrowings
            JOIN members ON borrowings.member_id = members.member_id
            JOIN book_copies ON borrowings.copy_id = book_copies.copy_id
            JOIN books ON book_copies.book_id = books.book_id
            WHERE borrowings.returned_at IS NULL
            ORDER BY borrowings.due_date;
        ''')
        return cur.fetchall()






def get_borrow_count_per_member(conn):

    with conn.cursor() as cur:
        cur.execute('''
            SELECT members.name, COUNT(borrowings.borrowing_id) AS total_borrowings
            FROM members
            LEFT JOIN borrowings ON members.member_id = borrowings.member_id
            GROUP BY members.name
            ORDER BY total_borrowings DESC;
        ''')
        return cur.fetchall()






def get_books_count_per_category(conn):

    with conn.cursor() as cur:
        cur.execute('''
            SELECT categories.name AS category_name, COUNT(books.book_id) AS total_books
            FROM categories
            LEFT JOIN books ON categories.category_id = books.category_id
            GROUP BY categories.name
            ORDER BY total_books DESC;
        ''')
        return cur.fetchall()






def print_query_results(title, rows):

    print(f"\n--- {title} ---")
    if not rows:
        print("(لا توجد نتائج)")
        return
    for row in rows:
        print(row)