import os
import pathlib
import zipfile
import shutil
import pandas as pd
from abc import ABC, abstractmethod

# Define an abstract class for Data Ingestor
class DataIngestor(ABC):
    """
    Abstract class that defines a contract for data ingestion.
    Any subclass must implement the `ingest` method.
    """
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        """Abstract method to ingest data from a given file."""
        pass

# Implement concrete classes for various file types
class CSVDataIngestor(DataIngestor):
    """Handles ingestion of CSV files."""
    def ingest(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

class JSONDataIngestor(DataIngestor):
    """Handles ingestion of JSON files."""
    def ingest(self, file_path: str) -> pd.DataFrame:
        return pd.read_json(file_path)

class ParquetDataIngestor(DataIngestor):
    """Handles ingestion of Parquet files."""
    def ingest(self, file_path: str) -> pd.DataFrame:
        return pd.read_parquet(file_path)

# Implement a class to handle ZIP ingestion
class ZipDataIngestor(DataIngestor):
    """Handles ingestion of ZIP files containing supported file formats (CSV, JSON, Parquet)."""
    SUPPORTED_FORMATS = {".csv": CSVDataIngestor, ".json": JSONDataIngestor, ".parquet": ParquetDataIngestor}
    
    def ingest(self, file_path: str, file_name: str = None) -> pd.DataFrame:
        """
        Extracts files from a ZIP archive and ingests the first supported file found.
        If multiple supported files exist, an error is raised unless `file_name` is specified.
        """
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a .zip file.")
        
        extraction_path = "extracted_data"
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extraction_path)
        
        # Get list of extracted files that are in supported formats
        extracted_files = os.listdir(extraction_path)
        supported_files = [f for f in extracted_files if os.path.splitext(f)[1] in self.SUPPORTED_FORMATS]
        
        if not supported_files:
            shutil.rmtree(extraction_path)
            raise FileNotFoundError("No supported file format found in the extracted data.")
        
        if len(supported_files) > 1 and not file_name:
            shutil.rmtree(extraction_path)
            raise ValueError(f"Multiple supported files found in the ZIP. Please specify the file name to ingest. Available files: {supported_files}")
        
        selected_file = file_name if file_name else supported_files[0]
        
        if selected_file not in supported_files:
            shutil.rmtree(extraction_path)
            raise FileNotFoundError(f"The specified file '{selected_file}' was not found in the extracted data. Available files: {supported_files}")
        
        # Determine the file extension and get the corresponding ingestor class
        selected_ext = os.path.splitext(selected_file)[1]
        ingestor_class = self.SUPPORTED_FORMATS[selected_ext]()
        
        # Read the selected file into a DataFrame
        df = ingestor_class.ingest(os.path.join(extraction_path, selected_file))
        
        return df

# Implement a Factory to create DataIngestors
class DataIngestorFactory:
    """
    Factory class to return the appropriate DataIngestor based on the file extension.
    """
    INGESTORS = {".csv": CSVDataIngestor, ".json": JSONDataIngestor, ".parquet": ParquetDataIngestor, ".zip": ZipDataIngestor}
    
    @staticmethod
    def get_data_ingestor(file_path: str) -> DataIngestor:
        """
        Determines the correct DataIngestor based on the file extension.
        Raises an error if the file extension is not supported.
        """
        file_extension = os.path.splitext(file_path)[1]
        
        if file_extension not in DataIngestorFactory.INGESTORS:
            raise ValueError(f"No ingestor available for file extension: {file_extension}")
        
        return DataIngestorFactory.INGESTORS[file_extension]()

# Example usage
if __name__ == "__main__":
    
    # Get the current working directory
    folder_path = os.getcwd()

    # Ensure the path ends with a proper slash for the OS
    folder_path = str(pathlib.Path(folder_path).as_posix()) + "/"
    file_path = folder_path + "data/archive.zip"  # Replace with actual file path
    data_ingestor = DataIngestorFactory.get_data_ingestor(file_path)
    
    # Specify file_name if multiple supported files exist
    df = data_ingestor.ingest(file_path, file_name=None)  
    
    print(df.head())
