#!/usr/bin/env python3
"""
Enterprise IT Service Desk & End-User Support Operations Lab
Data Integrity & Quality Assurance Validator
Validates all CSV dataset files in incidents/ and asset-management/
"""

import csv
import os
import sys

def validate_csv(filepath, required_cols, id_col):
    errors = []
    warnings = []
    
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"], []
        
    seen_ids = set()
    row_count = 0
    
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        
        # Check required columns
        for col in required_cols:
            if col not in headers:
                errors.append(f"Missing required column '{col}'")
                
        for idx, row in enumerate(reader, start=2):
            row_count += 1
            record_id = row.get(id_col, '').strip()
            
            if not record_id:
                errors.append(f"Row {idx}: Empty identifier in column '{id_col}'")
            elif record_id in seen_ids:
                errors.append(f"Row {idx}: Duplicate identifier '{record_id}'")
            else:
                seen_ids.add(record_id)
                
            # Check for empty fields in required columns
            for col in required_cols:
                val = row.get(col, '').strip()
                if not val and col not in ['ResolvedDate', 'ResolutionTime_Hours', 'EscalatedTo', 'ImplementedDate', 'FulfilledDate', 'Notes']:
                    warnings.append(f"Row {idx} ({record_id}): Blank value in column '{col}'")
                    
    return errors, warnings, row_count

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    files_to_check = [
        ('incidents/incident-register.csv', ['IncidentID', 'Title', 'Category', 'Priority', 'Status'], 'IncidentID'),
        ('incidents/service-requests.csv', ['RequestID', 'Title', 'RequestType', 'Priority', 'Status'], 'RequestID'),
        ('incidents/problem-records.csv', ['ProblemID', 'Title', 'Category', 'Status'], 'ProblemID'),
        ('incidents/change-records.csv', ['ChangeID', 'Title', 'Type', 'Priority', 'Status'], 'ChangeID'),
        ('asset-management/asset-inventory.csv', ['AssetID', 'DeviceType', 'Manufacturer', 'Model', 'Status'], 'AssetID')
    ]
    
    total_errors = 0
    total_warnings = 0
    
    print("=" * 70)
    print("   NEXORA TECHNOLOGIES - DATA INTEGRITY & AUDIT REPORT")
    print("=" * 70)
    
    for rel_path, required_cols, id_col in files_to_check:
        full_path = os.path.join(base_dir, rel_path)
        errors, warnings, count = validate_csv(full_path, required_cols, id_col)
        
        status_str = "PASS" if not errors else "FAIL"
        print(f"[{status_str}] {rel_path} ({count} records)")
        
        if errors:
            for e in errors:
                print(f"   [ERROR] {e}")
            total_errors += len(errors)
            
        if warnings:
            for w in warnings[:3]:  # print first 3 warnings
                print(f"   [WARN] {w}")
            if len(warnings) > 3:
                print(f"   [WARN] ... and {len(warnings) - 3} more warnings")
            total_warnings += len(warnings)
            
    print("-" * 70)
    print(f"Validation Summary: {total_errors} Errors, {total_warnings} Warnings")
    print("=" * 70)
    
    if total_errors > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
