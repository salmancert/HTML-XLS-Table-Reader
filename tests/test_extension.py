import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from extension import HTMLXLSReaderNode, FileSelectionSettings, ParsingSettings


class TestHTMLXLSReader:
    """Test suite for HTML-XLS Reader Node"""
    
    @pytest.fixture
    def sample_html_content(self):
        """Sample HTML content with tables"""
        return """
        <html>
        <body>
            <table>
                <tr><th>Name</th><th>Age</th><th>City</th></tr>
                <tr><td>John</td><td>30</td><td>New York</td></tr>
                <tr><td>Jane</td><td>25</td><td>London</td></tr>
            </table>
            <table>
                <tr><th>Product</th><th>Price</th></tr>
                <tr><td>Apple</td><td>1.99</td></tr>
                <tr><td>Banana</td><td>0.99</td></tr>
            </table>
        </body>
        </html>
        """
    
    @pytest.fixture
    def temp_html_file(self, sample_html_content):
        """Create a temporary HTML file with .xls extension"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xls', delete=False) as f:
            f.write(sample_html_content)
            temp_path = f.name
        yield temp_path
        os.unlink(temp_path)
    
    @pytest.fixture
    def node(self):
        """Create a node instance"""
        return HTMLXLSReaderNode()
    
    def test_encoding_detection(self, node, temp_html_file):
        """Test automatic encoding detection"""
        encoding = node._detect_encoding(temp_html_file)
        assert encoding in ['utf-8', 'ascii', 'latin-1']
    
    def test_read_html_xls(self, node, temp_html_file):
        """Test reading HTML content from XLS file"""
        node.parsing_settings.encoding = 'auto'
        content = node._read_html_xls(temp_html_file)
        assert '<table>' in content
        assert 'John' in content
    
    def test_extract_single_table(self, node, sample_html_content):
        """Test extracting a single table"""
        node.parsing_settings.table_index = 0
        tables = node._extract_tables(sample_html_content)
        
        assert len(tables) > 0
        df = tables[0]
        assert len(df) == 2  # 2 data rows
        assert list(df.columns) == ['Name', 'Age', 'City']
    
    def test_extract_all_tables(self, node, sample_html_content):
        """Test extracting all tables"""
        node.parsing_settings.table_index = -1
        tables = node._extract_tables(sample_html_content)
        
        assert len(tables) == 2
        assert len(tables[0]) == 2  # First table has 2 rows
        assert len(tables[1]) == 2  # Second table has 2 rows
    
    def test_clean_column_names(self, node):
        """Test column name cleaning"""
        dirty_names = ['Column 1!', 'Column@2', 'Column#3', '  Column 4  ']
        clean_names = [node._clean_column_name(name) for name in dirty_names]
        
        assert clean_names == ['Column_1', 'Column_2', 'Column_3', 'Column_4']
    
    def test_process_single_file(self, node, temp_html_file):
        """Test processing a single file"""
        results = node._process_single_file(temp_html_file)
        
        assert len(results) > 0
        df, metadata = results[0]
        assert 'source_file' in metadata
        assert metadata['table_index'] == 0
    
    def test_batch_processing(self, node, sample_html_content):
        """Test batch processing mode"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create multiple test files
            for i in range(3):
                with open(os.path.join(temp_dir, f'test_{i}.xls'), 'w') as f:
                    f.write(sample_html_content)
            
            node.file_settings.batch_mode = True
            node.file_settings.folder_path = temp_dir
            node.file_settings.file_pattern = '*.xls'
            
            mock_context = Mock()
            mock_context.flow_variables = {}
            
            files = node._get_files_to_process(mock_context)
            assert len(files) == 3
    
    def test_error_handling(self, node):
        """Test error handling for missing files"""
        node.file_settings.file_path = '/nonexistent/file.xls'
        mock_context = Mock()
        mock_context.flow_variables = {}
        
        with pytest.raises(ValueError, match="File does not exist"):
            node._get_files_to_process(mock_context)
    
    def test_metadata_inclusion(self, node, temp_html_file):
        """Test metadata column inclusion"""
        node.output_settings.include_metadata = True
        results = node._process_single_file(temp_html_file)
        
        df, metadata = results[0]
        assert 'source_file' in metadata
        assert 'file_path' in metadata
        assert 'table_index' in metadata
        assert 'num_rows' in metadata
        assert 'num_cols' in metadata


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
