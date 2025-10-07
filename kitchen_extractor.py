#!/usr/bin/env python3
"""
Kitchen BOM Extractor
Extracts Bill of Materials from kitchen specifications
"""

import json
import csv
from typing import Dict, List, Any
from collections import defaultdict


class KitchenBOMExtractor:
    """Extract and generate Bill of Materials from kitchen specifications"""
    
    def __init__(self):
        self.bom_items = defaultdict(lambda: {
            'quantity': 0,
            'unit': '',
            'category': '',
            'description': ''
        })
    
    def load_from_json(self, filepath: str) -> None:
        """Load kitchen specification from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self._process_specification(data)
    
    def load_from_csv(self, filepath: str) -> None:
        """Load kitchen specification from CSV file"""
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)
            self._process_csv_items(items)
    
    def _process_specification(self, spec: Dict[str, Any]) -> None:
        """Process kitchen specification and extract BOM items"""
        if 'items' in spec:
            for item in spec['items']:
                self._add_item(
                    name=item.get('name'),
                    quantity=item.get('quantity', 1),
                    unit=item.get('unit', 'piece'),
                    category=item.get('category', 'general'),
                    description=item.get('description', '')
                )
    
    def _process_csv_items(self, items: List[Dict[str, str]]) -> None:
        """Process CSV items into BOM"""
        for item in items:
            self._add_item(
                name=item.get('name'),
                quantity=int(item.get('quantity', 1)),
                unit=item.get('unit', 'piece'),
                category=item.get('category', 'general'),
                description=item.get('description', '')
            )
    
    def _add_item(self, name: str, quantity: int, unit: str, 
                  category: str, description: str) -> None:
        """Add or update an item in the BOM"""
        if name:
            self.bom_items[name]['quantity'] += quantity
            self.bom_items[name]['unit'] = unit
            self.bom_items[name]['category'] = category
            self.bom_items[name]['description'] = description
    
    def generate_bom_report(self) -> str:
        """Generate a formatted BOM report"""
        report = "=" * 80 + "\n"
        report += "KITCHEN BILL OF MATERIALS (BOM)\n"
        report += "=" * 80 + "\n\n"
        
        # Group items by category
        categories = defaultdict(list)
        for name, details in sorted(self.bom_items.items()):
            categories[details['category']].append((name, details))
        
        for category in sorted(categories.keys()):
            report += f"\n{category.upper()}\n"
            report += "-" * 80 + "\n"
            
            for name, details in categories[category]:
                report += f"  {name:<40} {details['quantity']:>8} {details['unit']:<10}\n"
                if details['description']:
                    report += f"    Description: {details['description']}\n"
        
        report += "\n" + "=" * 80 + "\n"
        report += f"Total unique items: {len(self.bom_items)}\n"
        report += "=" * 80 + "\n"
        
        return report
    
    def export_to_json(self, filepath: str) -> None:
        """Export BOM to JSON file"""
        bom_dict = dict(self.bom_items)
        with open(filepath, 'w') as f:
            json.dump(bom_dict, f, indent=2)
    
    def export_to_csv(self, filepath: str) -> None:
        """Export BOM to CSV file"""
        with open(filepath, 'w', newline='') as f:
            fieldnames = ['name', 'quantity', 'unit', 'category', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for name, details in sorted(self.bom_items.items()):
                writer.writerow({
                    'name': name,
                    'quantity': details['quantity'],
                    'unit': details['unit'],
                    'category': details['category'],
                    'description': details['description']
                })
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary statistics of the BOM"""
        summary = {
            'total_items': len(self.bom_items),
            'categories': len(set(item['category'] for item in self.bom_items.values()))
        }
        return summary


def main():
    """CLI interface for kitchen BOM extractor"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Kitchen BOM Extractor - Extract Bill of Materials from kitchen specifications'
    )
    parser.add_argument('input', help='Input specification file (JSON or CSV)')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], 
                       help='Input format (auto-detected if not specified)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--output-format', choices=['json', 'csv', 'report'],
                       default='report', help='Output format (default: report)')
    
    args = parser.parse_args()
    
    # Create extractor
    extractor = KitchenBOMExtractor()
    
    # Determine input format
    input_format = args.format
    if not input_format:
        if args.input.endswith('.json'):
            input_format = 'json'
        elif args.input.endswith('.csv'):
            input_format = 'csv'
        else:
            print("Error: Could not determine input format. Please specify with -f/--format")
            return 1
    
    # Load input
    try:
        if input_format == 'json':
            extractor.load_from_json(args.input)
        else:
            extractor.load_from_csv(args.input)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        return 1
    except Exception as e:
        print(f"Error loading input: {e}")
        return 1
    
    # Generate output
    if args.output_format == 'report':
        report = extractor.generate_bom_report()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"BOM report written to {args.output}")
        else:
            print(report)
    elif args.output_format == 'json':
        output_file = args.output or 'bom_output.json'
        extractor.export_to_json(output_file)
        print(f"BOM exported to {output_file}")
    elif args.output_format == 'csv':
        output_file = args.output or 'bom_output.csv'
        extractor.export_to_csv(output_file)
        print(f"BOM exported to {output_file}")
    
    # Print summary
    summary = extractor.get_summary()
    print(f"\nSummary: {summary['total_items']} items in {summary['categories']} categories")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
