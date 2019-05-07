Alem is a simple revision wrapper of `Alembic <https://github.com/sqlalchemy/alembic>`_.

Usage:

Install by pip, "pip install alem".
Then you get a command "alem".

Difference from Alembic:

* Add two arguments for Alembic subcommand revision, "--upgrade"/"-U" and 
  "--downgrade"/"-D". They accept a string, separated by ";" for multiple sql
  statements, or a file path of sql file. Sql statements in sql file can be
  multiple lines or one line. You can ignore them as you want.
  Attention: comment in sql file is not supported yet.

The rest is to use it as Alembic.
