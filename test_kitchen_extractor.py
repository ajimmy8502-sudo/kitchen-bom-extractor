#!/usr/bin/env python3
"""
Unit tests for Kitchen BOM Extractor
"""

import unittest
import json
import csv
import tempfile
import os
from kitchen_extractor import KitchenBOMExtractor


class TestKitchenBOMExtractor(unittest.TestCase):
    """Test cases for KitchenBOMExtractor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = KitchenBOMExtractor()
    
    def test_add_single_item(self):
        """Test adding a single item to BOM"""
        self.extractor._add_item(
            name="Test Cabinet",
            quantity=2,
            unit="piece",
            category="cabinetry",
            description="Test description"
        )
        
        self.assertEqual(len(self.extractor.bom_items), 1)
        self.assertEqual(self.extractor.bom_items["Test Cabinet"]["quantity"], 2)
        self.assertEqual(self.extractor.bom_items["Test Cabinet"]["unit"], "piece")
    
    def test_add_duplicate_items(self):
        """Test that duplicate items accumulate quantities"""
        self.extractor._add_item(
            name="Cabinet",
            quantity=2,
            unit="piece",
            category="cabinetry",
            description="Base cabinet"
        )
        self.extractor._add_item(
            name="Cabinet",
            quantity=3,
            unit="piece",
            category="cabinetry",
            description="Base cabinet"
        )
        
        self.assertEqual(len(self.extractor.bom_items), 1)
        self.assertEqual(self.extractor.bom_items["Cabinet"]["quantity"], 5)
    
    def test_load_from_json(self):
        """Test loading from JSON file"""
        # Create temporary JSON file
        test_data = {
            "items": [
                {
                    "name": "Test Item",
                    "quantity": 5,
                    "unit": "piece",
                    "category": "test",
                    "description": "Test item"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            self.extractor.load_from_json(temp_file)
            self.assertEqual(len(self.extractor.bom_items), 1)
            self.assertEqual(self.extractor.bom_items["Test Item"]["quantity"], 5)
        finally:
            os.unlink(temp_file)
    
    def test_load_from_csv(self):
        """Test loading from CSV file"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'quantity', 'unit', 'category', 'description'])
            writer.writeheader()
            writer.writerow({
                'name': 'CSV Item',
                'quantity': '3',
                'unit': 'piece',
                'category': 'test',
                'description': 'CSV test item'
            })
            temp_file = f.name
        
        try:
            self.extractor.load_from_csv(temp_file)
            self.assertEqual(len(self.extractor.bom_items), 1)
            self.assertEqual(self.extractor.bom_items["CSV Item"]["quantity"], 3)
        finally:
            os.unlink(temp_file)
    
    def test_generate_bom_report(self):
        """Test BOM report generation"""
        self.extractor._add_item(
            name="Test Item",
            quantity=1,
            unit="piece",
            category="test",
            description="Test"
        )
        
        report = self.extractor.generate_bom_report()
        
        self.assertIn("KITCHEN BILL OF MATERIALS", report)
        self.assertIn("Test Item", report)
        self.assertIn("TEST", report)
        self.assertIn("Total unique items: 1", report)
    
    def test_export_to_json(self):
        """Test JSON export"""
        self.extractor._add_item(
            name="Export Test",
            quantity=2,
            unit="piece",
            category="test",
            description="Export test item"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.extractor.export_to_json(temp_file)
            
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn("Export Test", data)
            self.assertEqual(data["Export Test"]["quantity"], 2)
        finally:
            os.unlink(temp_file)
    
    def test_export_to_csv(self):
        """Test CSV export"""
        self.extractor._add_item(
            name="CSV Export",
            quantity=4,
            unit="piece",
            category="test",
            description="CSV export test"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            self.extractor.export_to_csv(temp_file)
            
            with open(temp_file, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['name'], 'CSV Export')
            self.assertEqual(rows[0]['quantity'], '4')
        finally:
            os.unlink(temp_file)
    
    def test_get_summary(self):
        """Test summary statistics"""
        self.extractor._add_item("Item 1", 1, "piece", "category1", "Desc1")
        self.extractor._add_item("Item 2", 2, "piece", "category1", "Desc2")
        self.extractor._add_item("Item 3", 3, "piece", "category2", "Desc3")
        
        summary = self.extractor.get_summary()
        
        self.assertEqual(summary['total_items'], 3)
        self.assertEqual(summary['categories'], 2)
    
    def test_empty_bom(self):
        """Test handling of empty BOM"""
        report = self.extractor.generate_bom_report()
        self.assertIn("Total unique items: 0", report)
        
        summary = self.extractor.get_summary()
        self.assertEqual(summary['total_items'], 0)
    
    def test_multiple_categories(self):
        """Test items from multiple categories"""
        self.extractor._add_item("Cabinet", 1, "piece", "cabinetry", "")
        self.extractor._add_item("Countertop", 1, "sq ft", "countertops", "")
        self.extractor._add_item("Sink", 1, "piece", "fixtures", "")
        
        report = self.extractor.generate_bom_report()
        
        self.assertIn("CABINETRY", report)
        self.assertIn("COUNTERTOPS", report)
        self.assertIn("FIXTURES", report)


if __name__ == '__main__':
    unittest.main()
