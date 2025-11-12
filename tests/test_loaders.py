"""
Unit tests for data loaders and loader factory.

Tests the factory pattern and individual loader implementations.
"""

import pytest
import tempfile
import pandas as pd
from pathlib import Path

from validation_framework.loaders.factory import LoaderFactory
from validation_framework.loaders.csv_loader import CSVLoader
from validation_framework.loaders.base import DataLoader


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [25, 30, 35, 40, 45],
        "balance": [100.50, 200.75, 300.00, 400.25, 500.50]
    })

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def large_csv_file():
    """Create a larger CSV file for chunking tests."""
    df = pd.DataFrame({
        "id": range(1000),
        "value": range(1000, 2000)
    })

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name

    yield temp_path

    Path(temp_path).unlink()


@pytest.mark.unit
class TestLoaderFactory:
    """Tests for LoaderFactory."""

    def test_create_csv_loader_explicit(self, temp_csv_file):
        """Test creating CSV loader with explicit format."""
        loader = LoaderFactory.create_loader(
            file_path=temp_csv_file,
            file_format="csv"
        )

        assert isinstance(loader, CSVLoader)

    def test_create_csv_loader_auto_detect(self, temp_csv_file):
        """Test creating CSV loader with auto-detection."""
        loader = LoaderFactory.create_loader(file_path=temp_csv_file)

        assert isinstance(loader, CSVLoader)

    def test_create_loader_nonexistent_file_raises_error(self):
        """Test that creating loader for non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            LoaderFactory.create_loader(
                file_path="nonexistent.csv",
                file_format="csv"
            )

    def test_create_loader_unsupported_format_raises_error(self, temp_csv_file):
        """Test that unsupported format raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            LoaderFactory.create_loader(
                file_path=temp_csv_file,
                file_format="unsupported"
            )

        assert "Unsupported file format" in str(exc_info.value)

    def test_list_supported_formats(self):
        """Test listing supported formats."""
        formats = LoaderFactory.list_supported_formats()

        assert isinstance(formats, list)
        assert "csv" in formats
        assert "excel" in formats
        assert "parquet" in formats

    def test_infer_format_from_extension(self):
        """Test format inference from file extension."""
        assert LoaderFactory._infer_format("data.csv") == "csv"
        assert LoaderFactory._infer_format("data.xlsx") == "excel"
        assert LoaderFactory._infer_format("data.parquet") == "parquet"
        assert LoaderFactory._infer_format("data.tsv") == "csv"

    def test_infer_format_unknown_extension_raises_error(self):
        """Test that unknown extension raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            LoaderFactory._infer_format("data.unknown")

        assert "Cannot infer format" in str(exc_info.value)

    def test_custom_chunk_size(self, temp_csv_file):
        """Test creating loader with custom chunk size."""
        loader = LoaderFactory.create_loader(
            file_path=temp_csv_file,
            file_format="csv",
            chunk_size=100
        )

        assert loader.chunk_size == 100


@pytest.mark.unit
class TestCSVLoader:
    """Tests for CSVLoader."""

    def test_csv_loader_initialization(self, temp_csv_file):
        """Test CSVLoader initialization."""
        loader = CSVLoader(
            file_path=temp_csv_file,
            chunk_size=50000
        )

        assert str(loader.file_path) == temp_csv_file  # file_path is stored as Path object
        assert loader.chunk_size == 50000

    def test_csv_loader_load_returns_iterator(self, temp_csv_file):
        """Test that load() returns an iterator."""
        loader = CSVLoader(file_path=temp_csv_file)
        data_iterator = loader.load()

        # Check it's an iterator
        assert hasattr(data_iterator, '__iter__')
        assert hasattr(data_iterator, '__next__')

    def test_csv_loader_read_data(self, temp_csv_file):
        """Test reading data from CSV file."""
        loader = CSVLoader(file_path=temp_csv_file)
        data_iterator = loader.load()

        # Get first chunk
        chunk = next(data_iterator)

        assert isinstance(chunk, pd.DataFrame)
        assert len(chunk) == 5
        assert list(chunk.columns) == ["id", "name", "age", "balance"]

    def test_csv_loader_chunking(self, large_csv_file):
        """Test that chunking works correctly."""
        chunk_size = 250
        loader = CSVLoader(
            file_path=large_csv_file,
            chunk_size=chunk_size
        )

        chunks = list(loader.load())

        # Should have 4 chunks (1000 / 250)
        assert len(chunks) == 4

        # Each chunk (except possibly last) should have chunk_size rows
        for chunk in chunks[:-1]:
            assert len(chunk) == chunk_size

    def test_csv_loader_get_metadata(self, temp_csv_file):
        """Test getting file metadata."""
        loader = CSVLoader(file_path=temp_csv_file)
        metadata = loader.get_metadata()

        assert metadata["file_path"] == temp_csv_file
        # Note: file_format is not included in CSV loader metadata
        assert "file_size_bytes" in metadata
        assert "file_size_mb" in metadata
        assert metadata["is_empty"] is False
        assert "columns" in metadata
        assert len(metadata["columns"]) == 4
        assert "id" in metadata["columns"]
        assert "estimated_rows" in metadata

    def test_csv_loader_custom_delimiter(self):
        """Test CSV loader with custom delimiter."""
        # Create CSV with pipe delimiter
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, sep='|', index=False)
            temp_path = f.name

        try:
            loader = CSVLoader(
                file_path=temp_path,
                delimiter='|'
            )
            data_iterator = loader.load()
            chunk = next(data_iterator)

            assert len(chunk) == 2
            assert list(chunk.columns) == ["a", "b"]
        finally:
            Path(temp_path).unlink()

    def test_csv_loader_empty_file(self):
        """Test loading an empty CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Write nothing - create truly empty file (0 bytes)
            pass
            temp_path = f.name

        try:
            loader = CSVLoader(file_path=temp_path)
            metadata = loader.get_metadata()

            # Empty file has 0 bytes
            assert metadata["is_empty"] is True
            assert metadata["file_size_bytes"] == 0
        finally:
            Path(temp_path).unlink()


@pytest.mark.unit
class TestCustomLoaderRegistration:
    """Tests for registering custom loaders."""

    class CustomLoader(DataLoader):
        """Mock custom loader for testing."""

        def load(self):
            """Return empty iterator."""
            return iter([])

        def get_metadata(self):
            """Return empty metadata."""
            return {}

    def test_register_custom_loader(self):
        """Test registering a custom loader."""
        LoaderFactory.register_loader("custom", self.CustomLoader)

        assert "custom" in LoaderFactory.list_supported_formats()

    def test_use_custom_loader(self, temp_csv_file):
        """Test using a registered custom loader."""
        LoaderFactory.register_loader("custom", self.CustomLoader)

        loader = LoaderFactory.create_loader(
            file_path=temp_csv_file,
            file_format="custom"
        )

        assert isinstance(loader, self.CustomLoader)

    def test_register_non_loader_raises_error(self):
        """Test that registering non-DataLoader class raises TypeError."""
        class NotALoader:
            pass

        with pytest.raises(TypeError) as exc_info:
            LoaderFactory.register_loader("invalid", NotALoader)

        assert "must be a subclass of DataLoader" in str(exc_info.value)
