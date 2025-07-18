# Usage Guide

## Quick Start

### Basic Usage

1. **Add the Node**: Drag the "HTML-XLS Table Reader" from the Node Repository to your workflow

2. **Configure File Path**: 
   - Double-click the node to open configuration
   - Enter the path to your HTML-XLS file
   - Or use a flow variable for dynamic paths

3. **Execute**: Run the node to extract tables

### Example Workflow

```
[File Path Variable] --> [HTML-XLS Table Reader] --> [Data Processing]
```

## Configuration Options

### File Selection Tab

#### Single File Mode
- **File Path**: Direct path to the HTML-XLS file
- Can use flow variables for dynamic file selection

#### Batch Processing Mode
- **Enable Batch Processing**: Process multiple files
- **Folder Path**: Directory containing files
- **File Pattern**: Wildcards to match files (e.g., `*.xls`, `report_2024_*.xls`)
- **Recursive Search**: Include subdirectories

### Table Parsing Tab

- **Encoding**: Character encoding (auto-detect or specify)
- **Table Index**: 
  - `0` = First table
  - `1` = Second table
  - `-1` = All tables
- **Header Rows**: Number of rows to use as headers
- **Skip Rows**: Rows to skip from the beginning
- **Parse Dates**: Automatically detect and parse date columns
- **Separators**: Configure thousand and decimal separators

### Output Options Tab

- **Include Metadata**: Add columns with source file information
- **Clean Column Names**: Remove special characters from headers
- **Drop Empty Rows**: Remove completely empty rows
- **Drop Empty Columns**: Remove completely empty columns

## Advanced Usage

### Using Flow Variables

```python
# Set file path via flow variable
flow_variables['file_path'] = '/data/reports/monthly_report.xls'
```

### Batch Processing Example

Process all Excel files in a directory:
```
Configuration:
- Batch Processing Mode: ✓
- Folder Path: /data/reports/2024/
- File Pattern: *.xls
- Recursive: ✓
```

### Handling Multiple Tables

Extract all tables and add source information:
```
Configuration:
- Table Index: -1
- Include Metadata: ✓
```

## Output Structure

### Standard Output
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |

### With Metadata
| source_file | table_index | Column 1 | Column 2 |
|-------------|-------------|----------|----------|
| report.xls  | 0           | Data     | Data     |

## Common Use Cases

### 1. Web Application Exports
Many web applications export HTML tables with .xls extension:
```python
# Process weekly reports from web app
File Pattern: weekly_export_*.xls
Parse Dates: ✓
```

### 2. Legacy System Integration
Handle outputs from older systems:
```python
# Legacy system exports
Encoding: latin-1
Skip Rows: 3  # Skip header info
```

### 3. Data Aggregation
Combine multiple report files:
```python
# Aggregate monthly reports
Batch Mode: ✓
File Pattern: report_2024_*.xls
Include Metadata: ✓
```

## Tips and Best Practices

1. **Preview Tables First**: Use the preview feature to understand table structure
2. **Test with Single File**: Before batch processing, test with one file
3. **Use Metadata**: Include metadata when processing multiple files for tracking
4. **Handle Errors**: Enable error handling in batch mode to continue on failures
5. **Check Encoding**: If you see garbled text, try different encoding options

## Troubleshooting

### Common Issues

#### No Tables Found
- Verify the file contains HTML content
- Check if tables use non-standard HTML tags
- Try adjusting the parser settings

#### Encoding Errors
- Use encoding auto-detection
- Try common encodings: utf-8, latin-1, cp1252
- Check the original file source for encoding hints

#### Memory Issues with Large Files
- Process files individually instead of batch mode
- Extract specific tables instead of all tables
- Increase KNIME's memory allocation

### Error Messages

| Error | Solution |
|-------|----------|
| "No tables found" | Check HTML structure, verify file content |
| "Encoding error" | Try different encoding options |
| "Table index out of range" | Check available tables with preview |
| "File not found" | Verify file path and permissions |
