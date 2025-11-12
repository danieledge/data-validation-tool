#!/usr/bin/env python3
"""
Test script to run data validation without installing the CLI.

Author: daniel edge
"""

import sys
from pathlib import Path

# Add validation_framework to path
sys.path.insert(0, str(Path(__file__).parent))

from validation_framework.core.engine import ValidationEngine

def main():
    """Run validation test."""
    config_file = "examples/sample_config.yaml"

    print(f"Testing Data Validation Framework")
    print(f"Configuration: {config_file}\n")

    try:
        # Create engine and run validation
        engine = ValidationEngine.from_config(config_file)
        report = engine.run(verbose=True)

        # Generate reports
        print("\nGenerating reports...")
        engine.generate_html_report(report, "examples/validation_report.html")
        engine.generate_json_report(report, "examples/validation_summary.json")

        print("\n" + "="*80)
        print("Test Complete!")
        print("="*80)
        print(f"\nReports generated:")
        print(f"  - HTML: examples/validation_report.html")
        print(f"  - JSON: examples/validation_summary.json")
        print(f"\nOpen the HTML report in your browser to view results.\n")

        # Return exit code
        if report.has_errors():
            sys.exit(1)
        elif report.has_warnings():
            sys.exit(0)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
