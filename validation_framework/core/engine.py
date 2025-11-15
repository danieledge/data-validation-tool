"""
Validation engine - orchestrates the entire validation process.

The engine:
1. Loads configuration
2. Creates data loaders for each file
3. Executes validations in order
4. Collects and aggregates results
5. Generates reports
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from validation_framework.core.config import ValidationConfig
from validation_framework.core.registry import get_registry, ValidationRegistry
from validation_framework.core.results import (
    ValidationReport,
    FileValidationReport,
    Status,
)
from validation_framework.loaders.factory import LoaderFactory
from validation_framework.core.logging_config import get_logger

# Import to trigger registration of built-in validations
import validation_framework.validations.builtin.registry  # noqa

logger = get_logger(__name__)

# Optional imports for colored output
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Create dummy color classes
    class Fore:
        CYAN = ''
        YELLOW = ''
        GREEN = ''
        RED = ''
    class Style:
        RESET_ALL = ''


class ValidationEngine:
    """
    Main validation engine that orchestrates the validation process.

    The engine loads configuration, creates appropriate data loaders,
    executes validations, and generates comprehensive reports.

    Example usage:
        # From config file
        engine = ValidationEngine.from_config('validation_config.yaml')
        report = engine.run()

        # Generate reports
        engine.generate_html_report(report, 'report.html')
        engine.generate_json_report(report, 'report.json')
    """

    def __init__(self, config: ValidationConfig) -> None:
        """
        Initialize the validation engine.

        Args:
            config: Validation configuration object
        """
        self.config: ValidationConfig = config
        self.registry: ValidationRegistry = get_registry()

    @classmethod
    def from_config(cls, config_path: str) -> "ValidationEngine":
        """
        Create engine from YAML configuration file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            ValidationEngine instance

        Raises:
            ConfigError: If configuration is invalid
        """
        config = ValidationConfig.from_yaml(config_path)
        return cls(config)

    def run(self, verbose: bool = True) -> ValidationReport:
        """
        Execute all validations defined in the configuration.

        Args:
            verbose: If True, print progress information

        Returns:
            ValidationReport with complete validation results
        """
        logger.info(f"Starting validation job: {self.config.job_name}")
        logger.debug(f"Number of files to validate: {len(self.config.files)}")

        if verbose:
            print(f"\n{Fore.CYAN}{'='*80}")
            print(f"{Fore.CYAN}Data Validation Framework")
            print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
            print(f"Job: {self.config.job_name}")
            print(f"Files to validate: {len(self.config.files)}\n")

        start_time = time.time()

        # Create overall report
        report = ValidationReport(
            job_name=self.config.job_name,
            execution_time=datetime.now(),
            duration_seconds=0,  # Will be updated at end
            overall_status=Status.PASSED,
            config=self.config.to_dict(),
            description=self.config.description,
        )
        logger.debug("Validation report initialized")

        # Process each file
        for file_idx, file_config in enumerate(self.config.files, 1):
            logger.info(f"Processing file {file_idx}/{len(self.config.files)}: {file_config['name']}")
            logger.debug(f"File path: {file_config['path']}, Format: {file_config['format']}")

            if verbose:
                print(f"\n{Fore.YELLOW}[{file_idx}/{len(self.config.files)}] Processing: {file_config['name']}{Style.RESET_ALL}")
                print(f"  Path: {file_config['path']}")
                print(f"  Format: {file_config['format']}")
                print(f"  Validations: {len(file_config['validations'])}")

            # Validate the file
            file_report = self._validate_file(file_config, verbose)
            logger.info(f"File validation completed: {file_config['name']} - Status: {file_report.status.value}")

            # Add to overall report
            report.add_file_report(file_report)

            # Print summary for this file
            if verbose:
                status_color = Fore.GREEN if file_report.status == Status.PASSED else Fore.RED
                print(f"\n  {status_color}Status: {file_report.status.value}{Style.RESET_ALL}")
                print(f"  Errors: {file_report.error_count}")
                print(f"  Warnings: {file_report.warning_count}")
                print(f"  Duration: {file_report.execution_time:.2f}s")

        # Update overall status and duration
        report.update_overall_status()
        report.duration_seconds = time.time() - start_time

        logger.info(f"Validation job completed in {report.duration_seconds:.2f}s")
        logger.info(f"Overall status: {report.overall_status.value} (Errors: {report.total_errors}, Warnings: {report.total_warnings})")

        # Print final summary
        if verbose:
            self._print_summary(report)

        return report

    def _validate_file(self, file_config: Dict[str, Any], verbose: bool) -> FileValidationReport:
        """
        Validate a single file.

        Args:
            file_config: File configuration dictionary
            verbose: Whether to print progress

        Returns:
            FileValidationReport with all validation results for this file
        """
        start_time = time.time()

        # Create file report
        file_report = FileValidationReport(
            file_name=file_config["name"],
            file_path=file_config["path"],
            file_format=file_config["format"],
            status=Status.PASSED,
        )

        try:
            # Create data loader
            loader = LoaderFactory.create_loader(
                file_path=file_config["path"],
                file_format=file_config["format"],
                chunk_size=self.config.chunk_size,
                delimiter=file_config.get("delimiter"),
                encoding=file_config.get("encoding"),
                header=file_config.get("header"),
                sheet_name=file_config.get("sheet_name"),
            )

            # Get file metadata
            metadata = loader.get_metadata()
            file_report.metadata = metadata

            # Build validation context
            context = {
                "file_path": file_config["path"],
                "file_name": file_config["name"],
                "file_format": file_config["format"],
                "max_sample_failures": self.config.max_sample_failures,
                **metadata,
            }

            # Execute each validation
            validations = file_config.get("validations", [])

            if verbose and validations:
                print(f"\n  Executing validations:")

            for validation_config in validations:
                if not validation_config.get("enabled", True):
                    continue

                validation_type = validation_config["type"]

                if verbose:
                    print(f"    - {validation_type}...", end=" ", flush=True)

                try:
                    # Get validation class from registry
                    validation_class = self.registry.get(validation_type)

                    # Instantiate validation
                    validation = validation_class(
                        name=validation_type,
                        severity=validation_config["severity"],
                        params=validation_config.get("params", {}),
                        condition=validation_config.get("condition"),
                    )

                    # Execute validation
                    exec_start = time.time()

                    # Create fresh data iterator for this validation
                    data_iterator = loader.load()

                    result = validation.validate(data_iterator, context)
                    result.execution_time = time.time() - exec_start

                    # Add result to report
                    file_report.add_result(result)

                    if verbose:
                        if result.passed:
                            print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}✗ FAIL{Style.RESET_ALL}")

                except KeyError:
                    if verbose:
                        print(f"{Fore.RED}✗ NOT FOUND{Style.RESET_ALL}")
                    # Create error result for unknown validation
                    from validation_framework.core.results import ValidationResult, Severity
                    error_result = ValidationResult(
                        rule_name=validation_type,
                        severity=validation_config["severity"],
                        passed=False,
                        message=f"Validation type '{validation_type}' not found in registry",
                        failed_count=1,
                    )
                    file_report.add_result(error_result)

                except Exception as e:
                    if verbose:
                        print(f"{Fore.RED}✗ ERROR{Style.RESET_ALL}")
                    # Create error result
                    from validation_framework.core.results import ValidationResult
                    error_result = ValidationResult(
                        rule_name=validation_type,
                        severity=validation_config["severity"],
                        passed=False,
                        message=f"Error executing validation: {str(e)}",
                        failed_count=1,
                    )
                    file_report.add_result(error_result)

        except FileNotFoundError:
            if verbose:
                print(f"{Fore.RED}  ✗ File not found!{Style.RESET_ALL}")
            # Create error result
            from validation_framework.core.results import ValidationResult, Severity
            error_result = ValidationResult(
                rule_name="FileExistence",
                severity=Severity.ERROR,
                passed=False,
                message=f"File not found: {file_config['path']}",
                failed_count=1,
            )
            file_report.add_result(error_result)

        except Exception as e:
            if verbose:
                print(f"{Fore.RED}  ✗ Error: {str(e)}{Style.RESET_ALL}")
            # Create error result
            from validation_framework.core.results import ValidationResult, Severity
            error_result = ValidationResult(
                rule_name="FileProcessing",
                severity=Severity.ERROR,
                passed=False,
                message=f"Error processing file: {str(e)}",
                failed_count=1,
            )
            file_report.add_result(error_result)

        # Update file report status and duration
        file_report.update_status()
        file_report.execution_time = time.time() - start_time

        return file_report

    def _print_summary(self, report: ValidationReport) -> None:
        """
        Print a summary of the validation results.

        Args:
            report: ValidationReport to summarize
        """
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}Validation Summary")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

        # Overall status
        status_color = Fore.GREEN if report.overall_status == Status.PASSED else Fore.RED
        print(f"Overall Status: {status_color}{report.overall_status.value}{Style.RESET_ALL}")
        print(f"Total Errors: {Fore.RED}{report.total_errors}{Style.RESET_ALL}")
        print(f"Total Warnings: {Fore.YELLOW}{report.total_warnings}{Style.RESET_ALL}")
        print(f"Total Duration: {report.duration_seconds:.2f}s")

        # Per-file summary
        print(f"\nFile Results:")
        for file_report in report.file_reports:
            status_color = Fore.GREEN if file_report.status == Status.PASSED else Fore.RED
            print(f"  {status_color}{'✓' if file_report.status == Status.PASSED else '✗'}{Style.RESET_ALL} "
                  f"{file_report.file_name}: "
                  f"{file_report.error_count} errors, "
                  f"{file_report.warning_count} warnings")

        print()

    def generate_html_report(self, report: ValidationReport, output_path: str) -> None:
        """
        Generate HTML report.

        Args:
            report: ValidationReport to convert to HTML
            output_path: Path for output HTML file
        """
        from validation_framework.reporters.html_reporter import HTMLReporter
        reporter = HTMLReporter()
        reporter.generate(report, output_path)

    def generate_json_report(self, report: ValidationReport, output_path: str) -> None:
        """
        Generate JSON report.

        Args:
            report: ValidationReport to convert to JSON
            output_path: Path for output JSON file
        """
        from validation_framework.reporters.json_reporter import JSONReporter
        reporter = JSONReporter()
        reporter.generate(report, output_path)

    def list_available_validations(self) -> List[str]:
        """
        Get list of all available validation types.

        Returns:
            List of validation type names
        """
        return self.registry.list_available()
