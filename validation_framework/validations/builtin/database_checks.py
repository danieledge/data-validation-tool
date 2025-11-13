"""
Database-specific validation rules.

These validations are designed for validating data in databases:
- SQL-based custom checks
- Database referential integrity
- Database constraint validation
"""

from typing import Iterator, Dict, Any
import pandas as pd
from validation_framework.validations.base import DataValidationRule, ValidationResult
import logging

logger = logging.getLogger(__name__)


class SQLCustomCheck(DataValidationRule):
    """
    Execute custom SQL-based validation logic.

    Allows complex validations using SQL queries. The query should return
    rows that FAIL the validation (i.e., problematic records).

    Configuration:
        params:
            connection_string (str, required): Database connection string
            sql_query (str, required): SQL query that returns failing records
            db_type (str, optional): Database type (postgresql, mysql, mssql, oracle, sqlite). Default: postgresql
            max_sample_size (int, optional): Maximum number of sample failures to return. Default: 10

    Example YAML:
        # Find customers with invalid email domains
        - type: "SQLCustomCheck"
          severity: "WARNING"
          params:
            connection_string: "postgresql://user:pass@localhost/db"
            db_type: "postgresql"
            sql_query: |
              SELECT customer_id, email
              FROM customers
              WHERE email NOT LIKE '%@%'
                 OR email NOT LIKE '%.%'

        # Find orders with negative amounts
        - type: "SQLCustomCheck"
          severity: "ERROR"
          params:
            connection_string: "postgresql://user:pass@localhost/db"
            sql_query: |
              SELECT order_id, total_amount
              FROM orders
              WHERE total_amount < 0
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        sql_query = self.params.get("sql_query", "")
        # Extract first line as description
        first_line = sql_query.strip().split('\n')[0][:100]
        return f"Executes SQL validation: {first_line}"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        """
        Execute SQL validation query.

        Note: data_iterator is not used for SQL checks - the SQL query
        operates directly on the database.

        Args:
            data_iterator: Not used for SQL checks
            context: Optional context information

        Returns:
            ValidationResult with failing records
        """
        try:
            # Get parameters
            connection_string = self.params.get("connection_string")
            sql_query = self.params.get("sql_query")
            db_type = self.params.get("db_type", "postgresql")
            max_samples = self.params.get("max_sample_size", 10)

            # Validate required parameters
            if not connection_string:
                return self._create_result(
                    passed=False,
                    message="Parameter 'connection_string' is required",
                    failed_count=1,
                )

            if not sql_query:
                return self._create_result(
                    passed=False,
                    message="Parameter 'sql_query' is required",
                    failed_count=1,
                )

            # Import SQLAlchemy
            try:
                from sqlalchemy import create_engine
            except ImportError:
                return self._create_result(
                    passed=False,
                    message="SQLAlchemy is required for SQL checks. Install with: pip install sqlalchemy",
                    failed_count=1,
                )

            # Create engine
            engine = create_engine(connection_string)

            # Execute query to find failures
            logger.info(f"Executing SQL validation query")
            logger.debug(f"Query: {sql_query}")

            failing_records = pd.read_sql_query(sql_query, engine)
            engine.dispose()

            # Count failures
            failure_count = len(failing_records)

            if failure_count == 0:
                return self._create_result(
                    passed=True,
                    message="SQL validation passed: No failing records found",
                    total_count=1,
                )

            # Collect sample failures
            sample_failures = []
            for idx, row in failing_records.head(max_samples).iterrows():
                sample_failures.append({
                    "row_index": int(idx),
                    "record": row.to_dict(),
                })

            return self._create_result(
                passed=False,
                message=f"SQL validation failed: Found {failure_count} records that fail the validation",
                failed_count=failure_count,
                sample_failures=sample_failures,
            )

        except Exception as e:
            logger.error(f"Error in SQLCustomCheck: {str(e)}", exc_info=True)
            return self._create_result(
                passed=False,
                message=f"Error executing SQL validation: {str(e)}",
                failed_count=1,
            )


class DatabaseReferentialIntegrityCheck(DataValidationRule):
    """
    Validates foreign key relationships within a database.

    Similar to ReferentialIntegrityCheck but optimized for database-to-database
    validation using SQL joins instead of loading data into memory.

    Configuration:
        params:
            connection_string (str, required): Database connection string
            foreign_key_table (str, required): Table with foreign key
            foreign_key_column (str, required): Foreign key column
            reference_table (str, required): Reference table
            reference_key_column (str, required): Primary key column in reference table
            allow_null (bool, optional): Whether NULL values are allowed. Default: false
            db_type (str, optional): Database type. Default: postgresql

    Example YAML:
        # Validate order.customer_id references customers.id
        - type: "DatabaseReferentialIntegrityCheck"
          severity: "ERROR"
          params:
            connection_string: "postgresql://user:pass@localhost/db"
            foreign_key_table: "orders"
            foreign_key_column: "customer_id"
            reference_table: "customers"
            reference_key_column: "id"
            allow_null: false
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        fk_table = self.params.get("foreign_key_table", "?")
        fk_col = self.params.get("foreign_key_column", "?")
        ref_table = self.params.get("reference_table", "?")
        ref_col = self.params.get("reference_key_column", "?")

        return f"Validates {fk_table}.{fk_col} references {ref_table}.{ref_col}"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        """
        Check referential integrity using SQL.

        Args:
            data_iterator: Not used for database checks
            context: Optional context information

        Returns:
            ValidationResult indicating foreign key violations
        """
        try:
            # Get parameters
            connection_string = self.params.get("connection_string")
            fk_table = self.params.get("foreign_key_table")
            fk_column = self.params.get("foreign_key_column")
            ref_table = self.params.get("reference_table")
            ref_column = self.params.get("reference_key_column")
            allow_null = self.params.get("allow_null", False)
            db_type = self.params.get("db_type", "postgresql")
            max_samples = self.params.get("max_sample_size", 10)

            # Validate required parameters
            if not connection_string:
                return self._create_result(
                    passed=False,
                    message="Parameter 'connection_string' is required",
                    failed_count=1,
                )

            required_params = {
                "foreign_key_table": fk_table,
                "foreign_key_column": fk_column,
                "reference_table": ref_table,
                "reference_key_column": ref_column,
            }

            for param_name, param_value in required_params.items():
                if not param_value:
                    return self._create_result(
                        passed=False,
                        message=f"Parameter '{param_name}' is required",
                        failed_count=1,
                    )

            # Import SQLAlchemy
            try:
                from sqlalchemy import create_engine
            except ImportError:
                return self._create_result(
                    passed=False,
                    message="SQLAlchemy is required. Install with: pip install sqlalchemy",
                    failed_count=1,
                )

            # Create engine
            engine = create_engine(connection_string)

            # Build SQL query to find orphaned foreign keys
            null_condition = "" if allow_null else f"AND fk.{fk_column} IS NOT NULL"

            sql_query = f"""
                SELECT fk.{fk_column}
                FROM {fk_table} fk
                LEFT JOIN {ref_table} ref ON fk.{fk_column} = ref.{ref_column}
                WHERE ref.{ref_column} IS NULL
                  {null_condition}
            """

            logger.info("Checking database referential integrity")
            logger.debug(f"Query: {sql_query}")

            # Execute query
            violations = pd.read_sql_query(sql_query, engine)

            # Get total count for context
            count_query = f"SELECT COUNT(*) as total FROM {fk_table}"
            total_result = pd.read_sql_query(count_query, engine)
            total_count = total_result['total'].iloc[0]

            engine.dispose()

            # Count violations
            violation_count = len(violations)

            if violation_count == 0:
                return self._create_result(
                    passed=True,
                    message=f"All {total_count} foreign keys are valid",
                    total_count=total_count,
                )

            # Collect sample violations
            sample_failures = []
            for idx, row in violations.head(max_samples).iterrows():
                sample_failures.append({
                    "row_index": int(idx),
                    "foreign_key": fk_column,
                    "value": str(row[fk_column]),
                    "reason": f"Value not found in {ref_table}.{ref_column}"
                })

            return self._create_result(
                passed=False,
                message=f"Found {violation_count} referential integrity violations",
                failed_count=violation_count,
                total_count=total_count,
                sample_failures=sample_failures,
            )

        except Exception as e:
            logger.error(f"Error in DatabaseReferentialIntegrityCheck: {str(e)}", exc_info=True)
            return self._create_result(
                passed=False,
                message=f"Error checking database referential integrity: {str(e)}",
                failed_count=1,
            )


class DatabaseConstraintCheck(DataValidationRule):
    """
    Validates database constraints are not violated.

    Checks for violations of:
    - CHECK constraints
    - UNIQUE constraints
    - NOT NULL constraints

    Configuration:
        params:
            connection_string (str, required): Database connection string
            table (str, required): Table to check
            constraint_query (str, required): SQL query to find constraint violations
            constraint_name (str, optional): Name of constraint for reporting
            db_type (str, optional): Database type. Default: postgresql

    Example YAML:
        # Check for age constraint violations
        - type: "DatabaseConstraintCheck"
          severity: "ERROR"
          params:
            connection_string: "postgresql://user:pass@localhost/db"
            table: "customers"
            constraint_name: "age_check"
            constraint_query: |
              SELECT customer_id, age
              FROM customers
              WHERE age < 0 OR age > 150

        # Check for email uniqueness
        - type: "DatabaseConstraintCheck"
          severity: "ERROR"
          params:
            connection_string: "postgresql://user:pass@localhost/db"
            table: "users"
            constraint_name: "unique_email"
            constraint_query: |
              SELECT email, COUNT(*) as count
              FROM users
              GROUP BY email
              HAVING COUNT(*) > 1
    """

    def get_description(self) -> str:
        """Get human-readable description."""
        table = self.params.get("table", "?")
        constraint = self.params.get("constraint_name", "constraint")

        return f"Validates {constraint} constraint on {table}"

    def validate(self, data_iterator: Iterator[pd.DataFrame], context: Dict[str, Any]) -> ValidationResult:
        """
        Check database constraints.

        Args:
            data_iterator: Not used for database checks
            context: Optional context information

        Returns:
            ValidationResult indicating constraint violations
        """
        try:
            # Get parameters
            connection_string = self.params.get("connection_string")
            table = self.params.get("table")
            constraint_query = self.params.get("constraint_query")
            constraint_name = self.params.get("constraint_name", "constraint")
            db_type = self.params.get("db_type", "postgresql")
            max_samples = self.params.get("max_sample_size", 10)

            # Validate required parameters
            if not connection_string:
                return self._create_result(
                    passed=False,
                    message="Parameter 'connection_string' is required",
                    failed_count=1,
                )

            if not table:
                return self._create_result(
                    passed=False,
                    message="Parameter 'table' is required",
                    failed_count=1,
                )

            if not constraint_query:
                return self._create_result(
                    passed=False,
                    message="Parameter 'constraint_query' is required",
                    failed_count=1,
                )

            # Import SQLAlchemy
            try:
                from sqlalchemy import create_engine
            except ImportError:
                return self._create_result(
                    passed=False,
                    message="SQLAlchemy is required. Install with: pip install sqlalchemy",
                    failed_count=1,
                )

            # Create engine
            engine = create_engine(connection_string)

            # Execute constraint check query
            logger.info(f"Checking database constraint: {constraint_name}")
            logger.debug(f"Query: {constraint_query}")

            violations = pd.read_sql_query(constraint_query, engine)
            engine.dispose()

            # Count violations
            violation_count = len(violations)

            if violation_count == 0:
                return self._create_result(
                    passed=True,
                    message=f"Constraint '{constraint_name}' is satisfied",
                    total_count=1,
                )

            # Collect sample violations
            sample_failures = []
            for idx, row in violations.head(max_samples).iterrows():
                sample_failures.append({
                    "row_index": int(idx),
                    "constraint": constraint_name,
                    "record": row.to_dict(),
                })

            return self._create_result(
                passed=False,
                message=f"Found {violation_count} violations of constraint '{constraint_name}'",
                failed_count=violation_count,
                sample_failures=sample_failures,
            )

        except Exception as e:
            logger.error(f"Error in DatabaseConstraintCheck: {str(e)}", exc_info=True)
            return self._create_result(
                passed=False,
                message=f"Error checking database constraint: {str(e)}",
                failed_count=1,
            )
