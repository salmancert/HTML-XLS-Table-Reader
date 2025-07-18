# Examples

## Example 1: Simple Table Extraction

### Scenario
Extract a single table from an HTML file saved as .xls

### Input File (report.xls)
```html
<html>
<table>
  <tr><th>Product</th><th>Sales</th><th>Date</th></tr>
  <tr><td>Widget A</td><td>1,234</td><td>2024-01-15</td></tr>
  <tr><td>Widget B</td><td>5,678</td><td>2024-01-16</td></tr>
</table>
</html>
```

### Configuration
```yaml
File Path: /data/report.xls
Table Index: 0
Parse Dates: true
Thousands Separator: ,
```

### Output
| Product  | Sales | Date       |
|----------|-------|------------|
| Widget A | 1234  | 2024-01-15 |
| Widget B | 5678  | 2024-01-16 |

## Example 2: Batch Processing Multiple Reports

### Scenario
Process all monthly reports in a directory

### Directory Structure
```
/reports/
  ├── january_2024.xls
  ├── february_2024.xls
  └── march_2024.xls
```

### Configuration
```yaml
Batch Processing Mode: true
Folder Path: /reports/
File Pattern: *_2024.xls
Include Metadata: true
```

### Output
| source_file      | table_index | Month    | Revenue |
|------------------|-------------|----------|---------|
| january_2024.xls | 0           | January  | 50000   |
| february_2024.xls| 0           | February | 55000   |
| march_2024.xls   | 0           | March    | 60000   |

## Example 3: Multi-Table Extraction

### Scenario
Extract all tables from a complex report

### Input File (complex_report.xls)
```html
<html>
<h2>Sales Summary</h2>
<table>
  <tr><th>Region</th><th>Sales</th></tr>
  <tr><td>North</td><td>100K</td></tr>
  <tr><td>South</td><td>150K</td></tr>
</table>

<h2>Product Details</h2>
<table>
  <tr><th>Product</th><th>Stock</th></tr>
  <tr><td>A</td><td>500</td></tr>
  <tr><td>B</td><td>300</td></tr>
</table>
</html>
```

### Configuration
```yaml
Table Index: -1  # All tables
Include Metadata: true
```

### Output
| source_file        | table_index | Region | Sales | Product | Stock |
|--------------------|-------------|--------|-------|---------|-------|
| complex_report.xls | 0           | North  | 100K  | NULL    | NULL  |
| complex_report.xls | 0           | South  | 150K  | NULL    | NULL  |
| complex_report.xls | 1           | NULL   | NULL  | A       | 500   |
| complex_report.xls | 1           | NULL   | NULL  | B       | 300   |

## Example 4: Handling Special Characters

### Scenario
Process files with special characters and different encodings

### Configuration
```yaml
Encoding: auto
Clean Column Names: true
NA Values: "N/A, NULL, -, #N/A"
```

### Input Column Names
```
"Sales ($)", "Profit %", "Date (MM/DD/YYYY)", "Status!!!"
```

### Output Column Names
```
"Sales", "Profit", "Date_MM_DD_YYYY", "Status"
```

## Example 5: Flow Variable Integration

### Workflow Setup
```
[Table Creator] --> [Java Edit Variable] --> [HTML-XLS Reader] --> [Excel Writer]
      |                    |                         |                    |
      v                    v                         v                    v
  Create list         Set file_path            Read tables          Save results
```

### Java Edit Variable Code
```java
// Generate dynamic file path
String date = new SimpleDateFormat("yyyyMMdd").format(new Date());
out_file_path = "/reports/daily_report_" + date + ".xls";
```

## Example 6: Error Handling in Batch Mode

### Scenario
Process directory with mixed file types and handle errors

### Configuration
```yaml
Batch Processing Mode: true
File Pattern: *.xls
Error Handling: Continue on error
```

### Input Directory
```
/mixed_files/
  ├── valid_report.xls     ✓
  ├── corrupt_file.xls     ✗ (corrupted)
  ├── empty_file.xls       ✗ (no tables)
  └── good_report.xls      ✓
```

### Result
- 2 files successfully processed
- 2 files failed (logged as warnings)
- Output contains data from valid files only

## Example 7: Custom Parsing Options

### Scenario
Handle European number format and skip header rows

### Configuration
```yaml
Skip Rows: 5              # Skip company header
Header Rows: 2            # Multi-line headers
Thousands Separator: .    # European format
Decimal Separator: ,      # European format
Parse Dates: true
```

### Input (after skipping 5 rows)
```
| Product Category |        Sales        |
| Name            | Q1      | Q2       |
|-----------------|---------|----------|
| Electronics     | 1.234,56| 2.345,67 |
```

### Output
| Product_Category_Name | Sales_Q1 | Sales_Q2 |
|----------------------|----------|----------|
| Electronics          | 1234.56  | 2345.67  |
