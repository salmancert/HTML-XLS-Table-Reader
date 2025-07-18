import os
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Union, Optional, Tuple
import chardet
from bs4 import BeautifulSoup
import warnings
import knime.extension as knext

# Set up logging
LOGGER = logging.getLogger(__name__)

# Category definition
html_category = knext.category(
    path="/community/file-readers",
    level_id="html_xls",
    name="HTML-XLS Reader",
    description="Nodes for reading HTML tables from XLS files",
    icon="icon.png",
)

@knext.parameter_group(label="File Selection")
class FileSelectionSettings:
    """Settings for file selection and batch processing"""
    
    file_path = knext.StringParameter(
        "File Path",
        "Path to the HTML-XLS file. Leave empty to use flow variable.",
        "",
    )
    
    folder_path = knext.StringParameter(
        "Folder Path (Batch)",
        "Path to folder containing multiple HTML-XLS files (for batch processing).",
        "",
    )
    
    batch_mode = knext.BoolParameter(
        "Batch Processing Mode",
        "Enable to process multiple files from a folder.",
        False,
    )
    
    file_pattern = knext.StringParameter(
        "File Pattern",
        "Pattern to match files (e.g., *.xls, report_*.xls)",
        "*.xls",
    ).rule(knext.OneOf(batch_mode, [True]), knext.Effect.SHOW)
    
    recursive = knext.BoolParameter(
        "Recursive Search",
        "Search for files recursively in subdirectories.",
        False,
    ).rule(knext.OneOf(batch_mode, [True]), knext.Effect.SHOW)

@knext.parameter_group(label="Table Parsing Options")
class ParsingSettings:
    """Advanced options for parsing HTML tables"""
    
    encoding = knext.StringParameter(
        "File Encoding",
        "Character encoding of the file. Use 'auto' for automatic detection.",
        "auto",
        enum=["auto", "utf-8", "latin-1", "cp1252", "iso-8859-1", "utf-16"]
    )
    
    table_index = knext.IntParameter(
        "Table Index",
        "Index of the table to extract (0-based). Use -1 for all tables.",
        0,
        min_value=-1
    )
    
    header_rows = knext.IntParameter(
        "Header Rows",
        "Number of rows to use as column headers.",
        1,
        min_value=0,
        max_value=10
    )
    
    skip_rows = knext.IntParameter(
        "Skip Rows",
        "Number of rows to skip from the beginning.",
        0,
        min_value=0
    )
    
    parse_dates = knext.BoolParameter(
        "Parse Dates",
        "Attempt to parse date columns automatically.",
        True
    )
    
    thousands_sep = knext.StringParameter(
        "Thousands Separator",
        "Character used as thousands separator (e.g., comma).",
        ","
    )
    
    decimal_sep = knext.StringParameter(
        "Decimal Separator",
        "Character used as decimal separator.",
        "."
    )
    
    na_values = knext.StringParameter(
        "NA Values",
        "Comma-separated list of strings to treat as missing values.",
        "NA,N/A,null,NULL,None,NONE"
    )

@knext.parameter_group(label="Table Selection GUI", is_advanced=True)
class GUISettings:
    """Settings for the table selection GUI"""
    
    show_preview = knext.BoolParameter(
        "Show Table Preview",
        "Show a preview of available tables during configuration.",
        True
    )
    
    preview_rows = knext.IntParameter(
        "Preview Rows",
        "Number of rows to show in preview.",
        10,
        min_value=5,
        max_value=100
    )
    
    enable_interactive = knext.BoolParameter(
        "Enable Interactive Selection",
        "Enable interactive table selection (requires restart).",
        False
    )

@knext.parameter_group(label="Output Options")
class OutputSettings:
    """Options for output formatting"""
    
    include_metadata = knext.BoolParameter(
        "Include Metadata",
        "Add metadata columns (source file, table index, etc.).",
        True
    )
    
    clean_column_names = knext.BoolParameter(
        "Clean Column Names",
        "Clean column names (remove special characters, spaces).",
        True
    )
    
    drop_empty_rows = knext.BoolParameter(
        "Drop Empty Rows",
        "Remove rows that are completely empty.",
        True
    )
    
    drop_empty_cols = knext.BoolParameter(
        "Drop Empty Columns",
        "Remove columns that are completely empty.",
        True
    )

@knext.node(
    name="HTML-XLS Table Reader",
    node_type=knext.NodeType.SOURCE,
    icon_path="icon.png",
    category=html_category
)
@knext.output_table(
    name="Extracted Tables",
    description="Tables extracted from HTML-XLS files"
)
class HTMLXLSReaderNode:
    """Read HTML tables from XLS files.
    
    This node reads HTML content saved as .xls files and extracts tables from them.
    It supports automatic encoding detection, batch processing of multiple files,
    and provides advanced parsing options for complex table structures.
    
    The node can handle:
    - HTML tables saved with .xls extension
    - Multiple tables within a single file
    - Various character encodings
    - Malformed HTML structures
    - Batch processing of entire directories
    """
    
    file_settings = FileSelectionSettings()
    parsing_settings = ParsingSettings()
    gui_settings = GUISettings()
    output_settings = OutputSettings()
    
    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding automatically"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']
                
                LOGGER.info(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
                
                if confidence < 0.7:
                    LOGGER.warning("Low confidence in encoding detection, using utf-8")
                    return 'utf-8'
                
                return encoding or 'utf-8'
        except Exception as e:
            LOGGER.error(f"Error detecting encoding: {e}")
            return 'utf-8'
    
    def _read_html_xls(self, file_path: str) -> str:
        """Read HTML content from XLS file"""
        encoding = self.parsing_settings.encoding
        
        if encoding == 'auto':
            encoding = self._detect_encoding(file_path)
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            LOGGER.warning(f"Failed to read with {encoding}, trying latin-1")
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def _extract_tables(self, html_content: str) -> List[pd.DataFrame]:
        """Extract tables from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            raise ValueError("No tables found in the HTML content")
        
        extracted_tables = []
        na_values = [v.strip() for v in self.parsing_settings.na_values.split(',')]
        
        for i, table in enumerate(tables):
            try:
                # Convert HTML table to pandas DataFrame
                df = pd.read_html(
                    str(table),
                    header=list(range(self.parsing_settings.header_rows)) if self.parsing_settings.header_rows > 0 else None,
                    skiprows=self.parsing_settings.skip_rows,
                    thousands=self.parsing_settings.thousands_sep,
                    decimal=self.parsing_settings.decimal_sep,
                    parse_dates=self.parsing_settings.parse_dates,
                    na_values=na_values
                )[0]
                
                # Clean the dataframe
                df = self._clean_dataframe(df)
                
                extracted_tables.append(df)
                
            except Exception as e:
                LOGGER.warning(f"Failed to parse table {i}: {e}")
                continue
        
        return extracted_tables
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and format the dataframe"""
        # Drop empty rows
        if self.output_settings.drop_empty_rows:
            df = df.dropna(how='all')
        
        # Drop empty columns
        if self.output_settings.drop_empty_cols:
            df = df.dropna(axis=1, how='all')
        
        # Clean column names
        if self.output_settings.clean_column_names:
            df.columns = [self._clean_column_name(str(col)) for col in df.columns]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
    
    def _clean_column_name(self, name: str) -> str:
        """Clean column name by removing special characters"""
        import re
        # Remove HTML tags if any
        name = re.sub('<.*?>', '', name)
        # Replace special characters with underscore
        name = re.sub(r'[^\w\s]', '_', name)
        # Replace multiple spaces/underscores with single underscore
        name = re.sub(r'[\s_]+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        # If empty, generate a name
        if not name:
            name = 'column'
        return name
    
    def _process_single_file(self, file_path: str) -> List[Tuple[pd.DataFrame, Dict]]:
        """Process a single HTML-XLS file"""
        LOGGER.info(f"Processing file: {file_path}")
        
        # Read HTML content
        html_content = self._read_html_xls(file_path)
        
        # Extract tables
        tables = self._extract_tables(html_content)
        
        if not tables:
            raise ValueError(f"No valid tables found in {file_path}")
        
        # Filter tables based on index
        if self.parsing_settings.table_index >= 0:
            if self.parsing_settings.table_index >= len(tables):
                raise ValueError(f"Table index {self.parsing_settings.table_index} out of range. "
                               f"File contains {len(tables)} tables.")
            tables = [tables[self.parsing_settings.table_index]]
        
        # Add metadata
        results = []
        for i, table in enumerate(tables):
            metadata = {
                'source_file': os.path.basename(file_path),
                'file_path': file_path,
                'table_index': i,
                'num_rows': len(table),
                'num_cols': len(table.columns)
            }
            results.append((table, metadata))
        
        return results
    
    def _get_files_to_process(self, exec_context) -> List[str]:
        """Get list of files to process based on settings"""
        files = []
        
        if self.file_settings.batch_mode:
            # Batch mode - process folder
            folder = Path(self.file_settings.folder_path)
            if not folder.exists():
                raise ValueError(f"Folder does not exist: {folder}")
            
            pattern = self.file_settings.file_pattern
            if self.file_settings.recursive:
                files = list(folder.rglob(pattern))
            else:
                files = list(folder.glob(pattern))
            
            files = [str(f) for f in files if f.is_file()]
            
            if not files:
                raise ValueError(f"No files matching pattern '{pattern}' found in {folder}")
                
        else:
            # Single file mode
            file_path = self.file_settings.file_path
            
            # Check flow variables
            if not file_path and 'file_path' in exec_context.flow_variables:
                file_path = exec_context.flow_variables['file_path']
            
            if not file_path:
                raise ValueError("No file path specified")
            
            if not os.path.exists(file_path):
                raise ValueError(f"File does not exist: {file_path}")
            
            files = [file_path]
        
        return files
    
    def configure(self, config_context):
        """Configure the node"""
        # Create output schema
        columns = []
        
        # Add metadata columns if enabled
        if self.output_settings.include_metadata:
            columns.extend([
                knext.Column(knext.string(), "source_file"),
                knext.Column(knext.string(), "file_path"),
                knext.Column(knext.int32(), "table_index"),
                knext.Column(knext.int32(), "num_rows"),
                knext.Column(knext.int32(), "num_cols")
            ])
        
        # We can't determine the actual table columns until execution
        # So we'll add a placeholder column
        columns.append(knext.Column(knext.string(), "data"))
        
        schema = knext.Schema(columns)
        
        # Show preview if enabled and in single file mode
        if (self.gui_settings.show_preview and 
            not self.file_settings.batch_mode and 
            self.file_settings.file_path):
            try:
                self._show_preview(self.file_settings.file_path)
            except Exception as e:
                config_context.set_warning(f"Could not generate preview: {str(e)}")
        
        return schema
    
    def _show_preview(self, file_path: str):
        """Show preview of available tables"""
        try:
            html_content = self._read_html_xls(file_path)
            soup = BeautifulSoup(html_content, 'html.parser')
            tables = soup.find_all('table')
            
            LOGGER.info(f"Found {len(tables)} tables in file")
            
            for i, table in enumerate(tables[:3]):  # Show first 3 tables
                try:
                    df = pd.read_html(str(table))[0]
                    LOGGER.info(f"\nTable {i}: {df.shape[0]} rows × {df.shape[1]} columns")
                    LOGGER.info(f"Columns: {list(df.columns)[:5]}...")
                    LOGGER.info(f"Preview:\n{df.head(self.gui_settings.preview_rows)}")
                except Exception as e:
                    LOGGER.warning(f"Could not preview table {i}: {e}")
                    
        except Exception as e:
            LOGGER.error(f"Preview failed: {e}")
    
    def execute(self, exec_context):
        """Execute the node"""
        # Get files to process
        files = self._get_files_to_process(exec_context)
        
        LOGGER.info(f"Processing {len(files)} file(s)")
        
        all_results = []
        
        # Process each file
        for file_path in files:
            try:
                results = self._process_single_file(file_path)
                
                for df, metadata in results:
                    if self.output_settings.include_metadata:
                        # Add metadata columns to dataframe
                        for key, value in metadata.items():
                            df[key] = value
                    
                    all_results.append(df)
                    
            except Exception as e:
                LOGGER.error(f"Error processing {file_path}: {e}")
                if not self.file_settings.batch_mode:
                    raise
                else:
                    exec_context.set_warning(f"Failed to process {file_path}: {str(e)}")
        
        if not all_results:
            raise ValueError("No tables were successfully extracted")
        
        # Combine all results
        if len(all_results) == 1:
            final_df = all_results[0]
        else:
            # Concatenate with outer join to handle different columns
            final_df = pd.concat(all_results, ignore_index=True, sort=False)
        
        # Set flow variables
        exec_context.flow_variables['num_files_processed'] = len(files)
        exec_context.flow_variables['num_tables_extracted'] = len(all_results)
        exec_context.flow_variables['total_rows'] = len(final_df)
        
        LOGGER.info(f"Successfully extracted {len(all_results)} tables with {len(final_df)} total rows")
        
        return knext.Table.from_pandas(final_df)
