"""
HTML report generator.

Generates comprehensive, interactive HTML reports with:
- Executive summary
- Per-file validation results
- Interactive tables
- Visual charts
- Collapsible sections
- Export capabilities
"""

from pathlib import Path
from jinja2 import Template
from validation_framework.reporters.base import Reporter
from validation_framework.core.results import ValidationReport, Status


class HTMLReporter(Reporter):
    """
    Generates rich HTML validation reports.

    The HTML report includes:
    - Executive summary with overall status
    - Detailed validation results per file
    - Sample failures with context
    - Statistics and charts
    - Interactive filtering and sorting
    """

    def generate(self, report: ValidationReport, output_path: str):
        """
        Generate HTML report from validation results.

        Args:
            report: ValidationReport with validation results
            output_path: Path where HTML file should be written

        Raises:
            IOError: If unable to write report file
        """
        try:
            # Prepare template data
            template_data = self._prepare_template_data(report)

            # Render HTML
            html_content = self._render_html(template_data)

            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Write HTML file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"HTML report generated: {output_path}")

        except Exception as e:
            raise IOError(f"Error generating HTML report: {str(e)}")

    def _prepare_template_data(self, report: ValidationReport) -> dict:
        """
        Prepare data for template rendering.

        Args:
            report: ValidationReport to extract data from

        Returns:
            Dictionary with template data
        """
        # Calculate summary statistics
        total_validations = sum(f.total_validations for f in report.file_reports)
        passed_validations = total_validations - report.total_errors - report.total_warnings

        return {
            "report": report,
            "total_validations": total_validations,
            "passed_validations": passed_validations,
            "Status": Status,
        }

    def _render_html(self, template_data: dict) -> str:
        """
        Render HTML using embedded template.

        Args:
            template_data: Data to pass to template

        Returns:
            Rendered HTML string
        """
        template = Template(HTML_TEMPLATE)
        return template.render(**template_data)


# Embedded HTML template
# This is self-contained with inline CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Validation Report - {{ report.job_name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
            border-radius: 8px;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        header .subtitle {
            opacity: 0.9;
            font-size: 1.1em;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .summary-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .summary-card h3 {
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .summary-card .value {
            font-size: 2.5em;
            font-weight: bold;
        }

        .status-passed { color: #10b981; }
        .status-failed { color: #ef4444; }
        .status-warning { color: #f59e0b; }

        .bg-passed { background-color: #d1fae5; }
        .bg-failed { background-color: #fee2e2; }
        .bg-warning { background-color: #fef3c7; }

        .file-section {
            background: white;
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .file-header {
            padding: 20px;
            background: #f9fafb;
            border-bottom: 2px solid #e5e7eb;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .file-header:hover {
            background: #f3f4f6;
        }

        .file-header h2 {
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .file-header .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }

        .file-stats {
            display: flex;
            gap: 20px;
            font-size: 0.9em;
        }

        .file-content {
            padding: 20px;
        }

        .file-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f9fafb;
            border-radius: 6px;
        }

        .file-meta-item {
            display: flex;
            flex-direction: column;
        }

        .file-meta-item label {
            font-size: 0.8em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }

        .file-meta-item value {
            font-weight: 600;
        }

        .validation-list {
            margin-top: 20px;
        }

        .validation-item {
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            margin-bottom: 15px;
            overflow: hidden;
        }

        .validation-header {
            padding: 15px;
            background: #fafafa;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }

        .validation-header:hover {
            background: #f5f5f5;
        }

        .validation-header h4 {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1em;
        }

        .validation-icon {
            font-size: 1.2em;
        }

        .validation-stats {
            display: flex;
            gap: 15px;
            font-size: 0.9em;
        }

        .validation-details {
            padding: 20px;
            background: white;
            border-top: 1px solid #e5e7eb;
            display: none;
        }

        .validation-details.show {
            display: block;
        }

        .failures-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        .failures-table th {
            background: #f3f4f6;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #e5e7eb;
        }

        .failures-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #e5e7eb;
        }

        .failures-table tr:hover {
            background: #f9fafb;
        }

        .code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .toggle-icon {
            transition: transform 0.3s;
        }

        .toggle-icon.rotated {
            transform: rotate(180deg);
        }

        @media print {
            body {
                background: white;
            }
            .file-header {
                cursor: default;
            }
            .validation-details {
                display: block !important;
            }
        }

        .metric-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 5px;
        }

        .badge-error {
            background: #fee2e2;
            color: #991b1b;
        }

        .badge-warning {
            background: #fef3c7;
            color: #92400e;
        }

        .badge-success {
            background: #d1fae5;
            color: #065f46;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ report.job_name }}</h1>
            <div class="subtitle">
                Executed: {{ report.execution_time.strftime('%Y-%m-%d %H:%M:%S') }} |
                Duration: {{ "%.2f"|format(report.duration_seconds) }}s
            </div>
        </header>

        <!-- Summary Section -->
        <div class="summary-grid">
            <div class="summary-card {% if report.overall_status == Status.PASSED %}bg-passed{% elif report.overall_status == Status.FAILED %}bg-failed{% else %}bg-warning{% endif %}">
                <h3>Overall Status</h3>
                <div class="value {% if report.overall_status == Status.PASSED %}status-passed{% elif report.overall_status == Status.FAILED %}status-failed{% else %}status-warning{% endif %}">
                    {{ report.overall_status.value }}
                </div>
            </div>

            <div class="summary-card">
                <h3>Total Validations</h3>
                <div class="value">{{ total_validations }}</div>
            </div>

            <div class="summary-card">
                <h3>Errors</h3>
                <div class="value status-failed">{{ report.total_errors }}</div>
            </div>

            <div class="summary-card">
                <h3>Warnings</h3>
                <div class="value status-warning">{{ report.total_warnings }}</div>
            </div>

            <div class="summary-card">
                <h3>Passed</h3>
                <div class="value status-passed">{{ passed_validations }}</div>
            </div>

            <div class="summary-card">
                <h3>Files Processed</h3>
                <div class="value">{{ report.file_reports|length }}</div>
            </div>
        </div>

        <!-- File Sections -->
        {% for file_report in report.file_reports %}
        <div class="file-section">
            <div class="file-header" onclick="toggleFileContent('file-{{ loop.index }}')">
                <h2>
                    <span class="status-badge {% if file_report.status == Status.PASSED %}bg-passed status-passed{% elif file_report.status == Status.FAILED %}bg-failed status-failed{% else %}bg-warning status-warning{% endif %}">
                        {{ file_report.status.value }}
                    </span>
                    {{ file_report.file_name }}
                </h2>
                <div class="file-stats">
                    <span>{{ file_report.total_validations }} checks</span>
                    <span class="status-failed">{{ file_report.error_count }} errors</span>
                    <span class="status-warning">{{ file_report.warning_count }} warnings</span>
                    <span class="toggle-icon" id="toggle-file-{{ loop.index }}">▼</span>
                </div>
            </div>

            <div class="file-content" id="file-{{ loop.index }}" style="display: block;">
                <!-- File Metadata -->
                <div class="file-meta">
                    <div class="file-meta-item">
                        <label>File Path</label>
                        <value>{{ file_report.file_path }}</value>
                    </div>
                    <div class="file-meta-item">
                        <label>Format</label>
                        <value>{{ file_report.file_format }}</value>
                    </div>
                    <div class="file-meta-item">
                        <label>File Size</label>
                        <value>
                            {% if file_report.metadata.file_size_mb %}
                                {{ "%.2f"|format(file_report.metadata.file_size_mb) }} MB
                            {% else %}
                                N/A
                            {% endif %}
                        </value>
                    </div>
                    <div class="file-meta-item">
                        <label>Rows</label>
                        <value>
                            {% if file_report.metadata.total_rows %}
                                {{ "{:,}".format(file_report.metadata.total_rows) }}
                            {% elif file_report.metadata.estimated_rows %}
                                ~{{ "{:,}".format(file_report.metadata.estimated_rows) }}
                            {% else %}
                                N/A
                            {% endif %}
                        </value>
                    </div>
                    <div class="file-meta-item">
                        <label>Columns</label>
                        <value>{{ file_report.metadata.column_count if file_report.metadata.column_count else 'N/A' }}</value>
                    </div>
                    <div class="file-meta-item">
                        <label>Duration</label>
                        <value>{{ "%.2f"|format(file_report.execution_time) }}s</value>
                    </div>
                </div>

                <!-- Validations -->
                <div class="validation-list">
                    <h3>Validation Results</h3>
                    {% for result in file_report.validation_results %}
                    {% set file_idx = loop.index0 %}
                    <div class="validation-item">
                        <div class="validation-header" onclick="toggleValidation('validation-{{ file_report.file_name }}-{{ loop.index }}')">
                            <h4>
                                <span class="validation-icon">
                                    {% if result.passed %}✅{% else %}❌{% endif %}
                                </span>
                                <span>{{ result.rule_name }}</span>
                                <span class="metric-badge {% if result.passed %}badge-success{% else %}{% if result.severity.value == 'ERROR' %}badge-error{% else %}badge-warning{% endif %}{% endif %}">
                                    {{ result.severity.value }}
                                </span>
                            </h4>
                            <div class="validation-stats">
                                {% if not result.passed %}
                                    <span>{{ result.failed_count }} failures</span>
                                {% endif %}
                                {% if result.total_count > 0 %}
                                    <span>{{ "%.1f"|format((result.total_count - result.failed_count) / result.total_count * 100) }}% success rate</span>
                                {% endif %}
                                <span class="toggle-icon" id="toggle-validation-{{ file_report.file_name }}-{{ loop.index }}">▼</span>
                            </div>
                        </div>

                        <div class="validation-details" id="validation-{{ file_report.file_name }}-{{ loop.index }}">
                            <p><strong>Message:</strong> {{ result.message }}</p>

                            {% if not result.passed and result.sample_failures %}
                                <h4 style="margin-top: 20px;">Sample Failures (showing {{ result.sample_failures|length }} of {{ result.failed_count }})</h4>
                                <table class="failures-table">
                                    <thead>
                                        <tr>
                                            <th>Row</th>
                                            {% if result.sample_failures[0].field %}
                                                <th>Field</th>
                                            {% endif %}
                                            {% if result.sample_failures[0].value %}
                                                <th>Value</th>
                                            {% endif %}
                                            <th>Message</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for failure in result.sample_failures %}
                                        <tr>
                                            <td><span class="code">{{ failure.row }}</span></td>
                                            {% if failure.field %}
                                                <td><span class="code">{{ failure.field }}</span></td>
                                            {% endif %}
                                            {% if failure.value %}
                                                <td><span class="code">{{ failure.value }}</span></td>
                                            {% endif %}
                                            <td>{{ failure.message }}</td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <script>
        function toggleFileContent(fileId) {
            const content = document.getElementById(fileId);
            const icon = document.getElementById('toggle-' + fileId);

            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.classList.remove('rotated');
            } else {
                content.style.display = 'none';
                icon.classList.add('rotated');
            }
        }

        function toggleValidation(validationId) {
            const details = document.getElementById(validationId);
            const icon = document.getElementById('toggle-' + validationId);

            details.classList.toggle('show');
            icon.classList.toggle('rotated');
        }

        // Auto-expand failed validations
        document.addEventListener('DOMContentLoaded', function() {
            const failedValidations = document.querySelectorAll('.validation-item');
            failedValidations.forEach(function(item) {
                const icon = item.querySelector('.validation-icon');
                if (icon && icon.textContent.trim() === '❌') {
                    const header = item.querySelector('.validation-header');
                    if (header) {
                        header.click();
                    }
                }
            });
        });
    </script>
</body>
</html>
"""
