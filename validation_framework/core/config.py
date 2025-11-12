"""Configuration parsing and validation."""

import yaml
from typing import Dict, Any, List
from pathlib import Path
from validation_framework.core.results import Severity


class ConfigError(Exception):
    """Configuration error."""
    pass


class ValidationConfig:
    """Configuration for a validation job."""

    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize from configuration dictionary.

        Args:
            config_dict: Configuration dictionary
        """
        self.raw_config = config_dict
        self._parse_config()

    @classmethod
    def from_yaml(cls, config_path: str) -> "ValidationConfig":
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            ValidationConfig instance
        """
        config_file = Path(config_path)
        if not config_file.exists():
            raise ConfigError(f"Configuration file not found: {config_path}")

        with open(config_file, "r") as f:
            config_dict = yaml.safe_load(f)

        return cls(config_dict)

    def _parse_config(self):
        """Parse and validate configuration."""
        if "validation_job" not in self.raw_config:
            raise ConfigError("Configuration must have 'validation_job' key")

        job_config = self.raw_config["validation_job"]

        # Job metadata
        self.job_name = job_config.get("name", "Unnamed Validation Job")
        self.version = job_config.get("version", "1.0")

        # Files to validate
        if "files" not in job_config or not job_config["files"]:
            raise ConfigError("Configuration must specify at least one file to validate")

        self.files = self._parse_files(job_config["files"])

        # Output configuration
        output_config = job_config.get("output", {})
        self.html_report_path = output_config.get("html_report", "validation_report.html")
        self.json_summary_path = output_config.get("json_summary", "validation_summary.json")
        self.fail_on_error = output_config.get("fail_on_error", True)
        self.fail_on_warning = output_config.get("fail_on_warning", False)

        # Processing options
        processing = job_config.get("processing", {})
        self.chunk_size = processing.get("chunk_size", 50000)
        self.parallel_files = processing.get("parallel_files", False)
        self.max_sample_failures = processing.get("max_sample_failures", 100)

    def _parse_files(self, files_config: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse files configuration."""
        parsed_files = []

        for idx, file_config in enumerate(files_config):
            if "path" not in file_config:
                raise ConfigError(f"File configuration {idx} missing 'path'")

            parsed_file = {
                "name": file_config.get("name", f"file_{idx}"),
                "path": file_config["path"],
                "format": file_config.get("format", self._infer_format(file_config["path"])),
                "delimiter": file_config.get("delimiter", ","),
                "encoding": file_config.get("encoding", "utf-8"),
                "header": file_config.get("header", 0),
                "validations": self._parse_validations(file_config.get("validations", [])),
                "metadata": file_config.get("metadata", {}),
            }

            parsed_files.append(parsed_file)

        return parsed_files

    def _parse_validations(self, validations_config: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse validations configuration."""
        parsed_validations = []

        for validation in validations_config:
            if "type" not in validation:
                raise ConfigError("Validation must specify 'type'")

            severity_str = validation.get("severity", "ERROR").upper()
            try:
                severity = Severity[severity_str]
            except KeyError:
                raise ConfigError(f"Invalid severity: {severity_str}. Must be ERROR or WARNING")

            parsed_validation = {
                "type": validation["type"],
                "severity": severity,
                "params": validation.get("params", {}),
                "enabled": validation.get("enabled", True),
                "description": validation.get("description", ""),
            }

            parsed_validations.append(parsed_validation)

        return parsed_validations

    def _infer_format(self, file_path: str) -> str:
        """Infer file format from extension."""
        suffix = Path(file_path).suffix.lower()
        format_map = {
            ".csv": "csv",
            ".tsv": "csv",
            ".txt": "csv",
            ".xls": "excel",
            ".xlsx": "excel",
            ".parquet": "parquet",
            ".json": "json",
            ".jsonl": "jsonl",
        }
        return format_map.get(suffix, "csv")

    def get_file_by_name(self, name: str) -> Dict[str, Any]:
        """Get file configuration by name."""
        for file_config in self.files:
            if file_config["name"] == name:
                return file_config
        raise ConfigError(f"File not found: {name}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "job_name": self.job_name,
            "version": self.version,
            "files": [f["name"] for f in self.files],
            "html_report_path": self.html_report_path,
            "json_summary_path": self.json_summary_path,
            "fail_on_error": self.fail_on_error,
            "fail_on_warning": self.fail_on_warning,
        }
