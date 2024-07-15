from enum import Enum


# For more error definitions, please refer to this link
# https://www.postgresql.org/docs/current/errcodes-appendix.html


class IntegrityErrorCode(Enum):

    INTEGRITY_CONSTRAINT_VIOLATION = "23000"  # Integrity constraint of the database is violated.
    # Example: Trying to delete a row that is referenced by another table via a foreign key.

    RESTRICT_VIOLATION = "23001"  # A restriction violation occurred when deleting or updating a record.
    # Example: Deleting a parent row that has dependent children restricted by a foreign key.

    NOT_NULL_VIOLATION = "23502"  # Attempt to insert a null value into a column that is defined as not null.
    # Example: Inserting a new user without specifying the user's name where the name column is not null.

    FOREIGN_KEY_VIOLATION = "23503"  # Foreign key constraint fails because a referenced entry does not exist.
    # Example: Inserting an order with a customer ID that does not exist in the customers table.

    UNIQUE_VIOLATION = "23505"  # Insertion or modification of record violates a unique constraint.
    # Example: Adding a new user with an email that already exists in the user database.
