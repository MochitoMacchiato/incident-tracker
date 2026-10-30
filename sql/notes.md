# SQL notes
- Primary key: a column whose value is unique per row and identifies that row.
- Foreign key: a column that must match a primary key in another table.
- JOIN: combines rows from two tables where a shared column matches.
- Index: a sorted lookup structure that lets Postgres find rows without reading the whole table.
- Indexes speed up reads: Postgres jumps to matching rows instead of scanning every row.
- Indexes slow down writes: every INSERT, UPDATE or DELETE must also update each index.