#!/usr/bin/env python3
"""Create test data files for unit tests"""

import os
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent

# Sample HTML table content
SIMPLE_TABLE = """<html>
<head><title>Test Report</title></head>
<body>
<h1>Sales Report</h1>
<table border="1">
    <tr>
        <th>Product</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Total</th>
    </tr>
    <tr>
        <td>Widget A</td>
        <td>100</td>
        <td>$10.50</td>
        <td>$1,050.00</td>
    </tr>
    <tr>
        <td>Widget B</td>
        <td>250</td>
        <td>$5.25</td>
        <td>$1,312.50</td>
    </tr>
    <tr>
        <td>Widget C</td>
        <td>75</td>
        <td>$15.00</td>
        <td>$1,125.00</td>
    </tr>
</table>
</body>
</html>"""

MULTI_TABLE = """<html>
<head><title>Complex Report</title></head>
<body>
<h1>Quarterly Report</h1>

<h2>Sales by Region</h2>
<table>
    <tr>
        <th>Region</th>
        <th>Q1 Sales</th>
        <th>Q2 Sales</th>
        <th>Growth %</th>
    </tr>
    <tr>
        <td>North</td>
        <td>$125,000</td>
        <td>$145,000</td>
        <td>16%</td>
    </tr>
    <tr>
        <td>South</td>
        <td>$98,000</td>
        <td>$112,000</td>
        <td>14.3%</td>
    </tr>
    <tr>
        <td>East</td>
        <td>$156,000</td>
        <td>$167,000</td>
        <td>7.1%</td>
    </tr>
    <tr>
        <td>West</td>
        <td>$203,000</td>
        <td>$235,000</td>
        <td>15.8%</td>
    </tr>
</table>

<h2>Product Performance</h2>
<table>
    <tr>
        <th>Product Line</th>
        <th>Units Sold</th>
        <th>Revenue</th>
        <th>Margin</th>
    </tr>
    <tr>
        <td>Premium</td>
        <td>1,250</td>
        <td>$625,000</td>
        <td>42%</td>
    </tr>
    <tr>
        <td>Standard</td>
        <td>3,800</td>
        <td>$456,000</td>
        <td>35%</td>
    </tr>
    <tr>
        <td>Economy</td>
        <td>5,200</td>
        <td>$312,000</td>
        <td>28%</td>
    </tr>
</table>

<h2>Top Customers</h2>
<table>
    <tr>
        <th>Customer</th>
        <th>Orders</th>
        <th>Total Value</th>
    </tr>
    <tr>
        <td>ABC Corp</td>
        <td>45</td>
        <td>$89,500</td>
    </tr>
    <tr>
        <td>XYZ Inc</td>
        <td>38</td>
        <td>$76,200</td>
    </tr>
</table>
</body>
</html>"""

# Create test files
def create_test_files():
    """Create test XLS files with HTML content"""
    
    # Simple table file
    with open(TEST_DATA_DIR / "sample_table.xls", "w", encoding="utf-8") as f:
        f.write(SIMPLE_TABLE)
    
    # Multi-table file
    with open(TEST_DATA_DIR / "sample_multi_table.xls", "w", encoding="utf-8") as f:
        f.write(MULTI_TABLE)
    
    print("Test files created successfully!")

if __name__ == "__main__":
    create_test_files()
