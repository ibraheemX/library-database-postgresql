# Library Database Project

A library database system built with PostgreSQL and psycopg2 (no ORM), to
showcase raw SQL skills and database schema design.

## Tables and Relationships (ERD)

| Table | Relationship | Description |
|---|---|---|
| `authors` | — | Book authors |
| `categories` | — | Book categories |
| `books` | many-to-one with `categories` | The book as a general "literary work" |
| `book_authors` | many-to-many (junction) between `books` and `authors` | Allows more than one author per book |
| `book_copies` | one-to-many with `books` | Each physical copy on its own, with its own status (`available`, `borrowed`, `damaged`, `lost`) |
| `members` | — | Library members |
| `borrowings` | junction between `book_copies` and `members` | Records who borrowed which copy, and when |

**Key design point:** `borrowings` references `book_copies` (a specific
physical copy) rather than `books` directly, because the same book can
have several copies, and each copy can be borrowed independently of the
others.

## Project Structure

```
library_project/
├── .env                  # Connection credentials (not pushed to GitHub)
├── .gitignore
├── requirements.txt
├── db_connection.py      # Database connection
├── schema.py              # Creates all tables
├── seed_data.py           # Seed/sample data
├── authors.py             # Inserts authors
├── categories.py          # Inserts categories
├── books.py                # Inserts books + links authors + creates copies
├── members.py             # Inserts members
├── borrowings.py          # Inserts borrowings
├── queries.py             # Retrieval queries (JOIN, GROUP BY, aggregates)
├── queries.sql            # Same queries as raw SQL, viewable without running any code
├── run_queries.py         # Runs and displays the queries
└── main.py                 # Main entry point
```

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update the `.env` file with your actual connection details (database
   name, user, password...).

3. Create the tables and seed the data:
   ```bash
   python main.py
   ```

4. Run the retrieval queries:
   ```bash
   python run_queries.py
   ```

   Alternatively, `queries.sql` contains the same queries as raw SQL and
   can be opened directly in pgAdmin or any SQL client, without running
   any Python code.

## Technical Concepts Applied

- **Foreign Keys** and **ON DELETE CASCADE / SET NULL**
- **Junction tables** for many-to-many relationships (`book_authors`, `borrowings`)
- **CHECK constraints** to restrict allowed values (`status` in `book_copies`)
- **RETURNING** to get the generated ID immediately after each INSERT
- **Environment variables** to protect sensitive connection data
- **Separation of concerns**: each table has its own file for insert logic
- **`with conn`** for automatic commit/rollback instead of manual transaction handling
- **INNER JOIN / LEFT JOIN / GROUP BY / COUNT** across multiple retrieval queries