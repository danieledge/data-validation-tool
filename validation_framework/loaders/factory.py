"""
Data loader factory for creating appropriate loaders based on file format.

The factory pattern allows easy extension with new file formats without
modifying existing code.
"""

from typing import Dict, Type
from pathlib import Path
from validation_framework.loaders.base import DataLoader
from validation_framework.loaders.csv_loader import CSVLoader
from validation_framework.loaders.excel_loader import ExcelLoader
from validation_framework.loaders.parquet_loader import ParquetLoader


class LoaderFactory:
    """
    Factory for creating data loaders based on file format.

    This factory automatically selects the appropriate loader implementation
    based on the specified file format or file extension.

    Supported formats:
        - CSV and delimited text files (csv, tsv, txt)
        - Excel files (xls, xlsx)
        - Parquet files (parquet)
    """

    # Mapping of format names to loader classes
    _loaders: Dict[str, Type[DataLoader]] = {
        "csv": CSVLoader,
        "excel": ExcelLoader,
        "parquet": ParquetLoader,
    }

    @classmethod
    def create_loader(
        cls,
        file_path: str,
        file_format: str = None,
        chunk_size: int = 50000,
        **kwargs
    ) -> DataLoader:
        """
        Create an appropriate data loader for the given file.

        Args:
            file_path (str): Path to the data file
            file_format (str, optional): File format ('csv', 'excel', 'parquet').
                                        If None, will be inferred from file extension.
            chunk_size (int): Number of rows per chunk for memory-efficient processing.
                             Default is 50,000 rows. For 200GB files, you may want
                             to adjust this based on available memory.
            **kwargs: Additional loader-specific parameters:
                - delimiter: Column delimiter for CSV files (default: ',')
                - encoding: File encoding for CSV files (default: 'utf-8')
                - header: Row number to use as column names (default: 0)
                - sheet_name: Sheet name or index for Excel files (default: 0)

        Returns:
            DataLoader: An instance of the appropriate loader class

        Raises:
            ValueError: If the file format is not supported or cannot be inferred
            FileNotFoundError: If the specified file does not exist

        Examples:
            >>> # Create CSV loader with custom delimiter
            >>> loader = LoaderFactory.create_loader(
            ...     'data.csv',
            ...     file_format='csv',
            ...     delimiter='|',
            ...     chunk_size=100000
            ... )

            >>> # Create Parquet loader (format auto-detected)
            >>> loader = LoaderFactory.create_loader('large_data.parquet')

            >>> # Create Excel loader for specific sheet
            >>> loader = LoaderFactory.create_loader(
            ...     'report.xlsx',
            ...     file_format='excel',
            ...     sheet_name='Sheet1'
            ... )
        """
        # Verify file exists
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Infer format from extension if not provided
        if file_format is None:
            file_format = cls._infer_format(file_path)

        # Normalize format name
        file_format = file_format.lower().strip()

        # Get the appropriate loader class
        loader_class = cls._loaders.get(file_format)

        if loader_class is None:
            supported_formats = ', '.join(cls._loaders.keys())
            raise ValueError(
                f"Unsupported file format: '{file_format}'. "
                f"Supported formats are: {supported_formats}"
            )

        # Instantiate and return the loader
        try:
            return loader_class(file_path, chunk_size=chunk_size, **kwargs)
        except Exception as e:
            raise RuntimeError(
                f"Error creating loader for {file_path}: {str(e)}"
            )

    @classmethod
    def _infer_format(cls, file_path: str) -> str:
        """
        Infer file format from file extension.

        Args:
            file_path (str): Path to the file

        Returns:
            str: Inferred format name

        Raises:
            ValueError: If format cannot be inferred from extension
        """
        suffix = Path(file_path).suffix.lower()

        # Map file extensions to format names
        extension_map = {
            ".csv": "csv",
            ".tsv": "csv",
            ".txt": "csv",
            ".xls": "excel",
            ".xlsx": "excel",
            ".parquet": "parquet",
        }

        inferred_format = extension_map.get(suffix)

        if inferred_format is None:
            raise ValueError(
                f"Cannot infer format from file extension '{suffix}'. "
                f"Please specify the format explicitly. "
                f"Supported extensions: {', '.join(extension_map.keys())}"
            )

        return inferred_format

    @classmethod
    def register_loader(cls, format_name: str, loader_class: Type[DataLoader]):
        """
        Register a custom data loader for a new format.

        This allows users to extend the factory with their own loader implementations.

        Args:
            format_name (str): Name to register the format under
            loader_class (Type[DataLoader]): Loader class (must inherit from DataLoader)

        Raises:
            TypeError: If loader_class is not a subclass of DataLoader

        Example:
            >>> class CustomLoader(DataLoader):
            ...     def load(self):
            ...         # Custom implementation
            ...         pass
            ...     def get_metadata(self):
            ...         return {}
            >>>
            >>> LoaderFactory.register_loader('custom', CustomLoader)
        """
        if not issubclass(loader_class, DataLoader):
            raise TypeError(
                f"{loader_class.__name__} must be a subclass of DataLoader"
            )

        cls._loaders[format_name.lower()] = loader_class

    @classmethod
    def list_supported_formats(cls) -> list:
        """
        Get list of all supported file formats.

        Returns:
            list: List of supported format names
        """
        return list(cls._loaders.keys())
