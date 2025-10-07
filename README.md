# Kitchen BOM Extractor

A Python tool for extracting and generating Bill of Materials (BOM) from kitchen specifications.

## Features

- Load kitchen specifications from JSON or CSV files
- Automatically accumulate quantities for duplicate items
- Generate formatted BOM reports organized by category
- Export BOM to JSON or CSV formats
- CLI interface for easy integration into workflows
- No external dependencies (uses Python standard library only)

## Installation

No installation required! The tool uses only Python standard library modules.

```bash
git clone https://github.com/ajimmy8502-sudo/kitchen-bom-extractor.git
cd kitchen-bom-extractor
```

## Usage

### Basic Usage

Generate a BOM report from a JSON specification:

```bash
python3 kitchen_extractor.py examples/kitchen_spec.json
```

Generate a BOM report from a CSV specification:

```bash
python3 kitchen_extractor.py examples/kitchen_spec.csv
```

### Advanced Usage

Save report to a file:

```bash
python3 kitchen_extractor.py examples/kitchen_spec.json -o my_bom_report.txt
```

Export to JSON format:

```bash
python3 kitchen_extractor.py examples/kitchen_spec.json --output-format json -o bom.json
```

Export to CSV format:

```bash
python3 kitchen_extractor.py examples/kitchen_spec.csv --output-format csv -o bom.csv
```

Specify input format explicitly:

```bash
python3 kitchen_extractor.py my_kitchen.txt -f json --output-format report
```

### Command Line Options

```
positional arguments:
  input                 Input specification file (JSON or CSV)

optional arguments:
  -h, --help           Show help message and exit
  -f, --format         Input format (json or csv) - auto-detected if not specified
  -o, --output         Output file path
  --output-format      Output format: report (default), json, or csv
```

## Input File Formats

### JSON Format

```json
{
  "items": [
    {
      "name": "Cabinet - Base 24\"",
      "quantity": 4,
      "unit": "piece",
      "category": "cabinetry",
      "description": "24-inch base cabinet with soft-close doors"
    }
  ]
}
```

### CSV Format

```csv
name,quantity,unit,category,description
Cabinet - Base 36",3,piece,cabinetry,36-inch base cabinet with drawers
```

Required fields:
- `name`: Item name (string)
- `quantity`: Number of items (integer)
- `unit`: Unit of measurement (string, e.g., "piece", "sq ft", "ft")
- `category`: Item category (string, e.g., "cabinetry", "fixtures", "hardware")
- `description`: Item description (string, optional)

## Output Formats

### Report Format (Default)

A formatted text report organized by category:

```
================================================================================
KITCHEN BILL OF MATERIALS (BOM)
================================================================================

CABINETRY
--------------------------------------------------------------------------------
  Cabinet - Base 24"                              4 piece     
    Description: 24-inch base cabinet with soft-close doors
...
================================================================================
Total unique items: 12
================================================================================
```

### JSON Format

A structured JSON file with all BOM data:

```json
{
  "Cabinet - Base 24\"": {
    "quantity": 4,
    "unit": "piece",
    "category": "cabinetry",
    "description": "24-inch base cabinet with soft-close doors"
  }
}
```

### CSV Format

A CSV file that can be imported into spreadsheet applications:

```csv
name,quantity,unit,category,description
Cabinet - Base 24",4,piece,cabinetry,24-inch base cabinet with soft-close doors
```

## Examples

The `examples/` directory contains sample kitchen specifications:

- `examples/kitchen_spec.json` - Complete kitchen with appliances, cabinetry, and fixtures
- `examples/kitchen_spec.csv` - Simple kitchen specification in CSV format

Try them out:

```bash
python3 kitchen_extractor.py examples/kitchen_spec.json
python3 kitchen_extractor.py examples/kitchen_spec.csv
```

## Testing

Run the unit tests:

```bash
python3 -m unittest test_kitchen_extractor.py -v
```

## Use Cases

- **Kitchen Designers**: Generate material lists from design specifications
- **Contractors**: Create shopping lists and cost estimates
- **Project Managers**: Track materials across multiple kitchen projects
- **DIY Renovators**: Plan and organize kitchen renovation materials

## Features in Detail

### Automatic Quantity Accumulation

If the same item appears multiple times in the input, the tool automatically accumulates quantities:

```json
Input:
  {"name": "Cabinet Hinge", "quantity": 4, ...}
  {"name": "Cabinet Hinge", "quantity": 6, ...}

Output:
  Cabinet Hinge: 10 pieces
```

### Category Organization

Items are automatically grouped by category in the report, making it easy to:
- Plan purchases by vendor or store section
- Organize work by trade (cabinetry, plumbing, electrical, etc.)
- Track progress by category

### Multiple Export Formats

Choose the format that works best for your workflow:
- **Report**: Human-readable format for printing or review
- **JSON**: Machine-readable for integration with other tools
- **CSV**: Import into Excel, Google Sheets, or database systems

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
