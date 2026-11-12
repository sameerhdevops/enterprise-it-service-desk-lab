#!/usr/bin/env python3
"""
Enterprise IT Service Desk & End-User Support Operations Lab
Data Integrity & Quality Assurance Validator
Validates all CSV dataset files in incidents/ and asset-management/
Performs strict timestamp reconciliation and mathematical duration audits.
Author: sameerhdevops
"""

import csv
import os
import sys
from datetime import datetime

def parse_dt(dt_str):
    clean = dt_str.strip()
    if not clean:
        return None
    return datetime.strptime(clean, '%Y-%m-%d %H:%M')

def validate_csv(filepath, required_cols, id_col):
    errors = []
    warnings = []
    
    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"], [], 0
        
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
                    
            # Strict timestamp reconciliation for incident-register.csv
            if 'incident-register' in filepath:
                status = row.get('Status', '').strip()
                rep_str = row.get('ReportedDate', '').strip()
                res_str = row.get('ResolvedDate', '').strip()
                dur_str = row.get('ResolutionTime_Hours', '').strip()
                
                if rep_str:
                    try:
                        dt_rep = parse_dt(rep_str)
                    except ValueError:
                        errors.append(f"Row {idx} ({record_id}): Invalid ReportedDate format '{rep_str}'")
                        dt_rep = None
                else:
                    errors.append(f"Row {idx} ({record_id}): Missing ReportedDate")
                    dt_rep = None
                    
                if status in ['Resolved', 'Closed']:
                    if not res_str:
                        errors.append(f"Row {idx} ({record_id}): Resolved incident missing ResolvedDate")
                    else:
                        try:
                            dt_res = parse_dt(res_str)
                            if dt_rep and dt_res < dt_rep:
                                errors.append(f"Row {idx} ({record_id}): ResolvedDate earlier than ReportedDate")
                            elif dt_rep and dt_res and dur_str:
                                elapsed = (dt_res - dt_rep).total_seconds() / 3600.0
                                try:
                                    dur_val = float(dur_str)
                                    if abs(elapsed - dur_val) > 0.01:
                                        errors.append(f"Row {idx} ({record_id}): Duration mismatch! CSV={dur_val}h, Elapsed={elapsed:.2f}h")
                                except ValueError:
                                    errors.append(f"Row {idx} ({record_id}): Non-numeric ResolutionTime_Hours '{dur_str}'")
                        except ValueError:
                            errors.append(f"Row {idx} ({record_id}): Invalid ResolvedDate format '{res_str}'")
                elif status in ['New', 'InProgress', 'Escalated', 'OnHold']:
                    if res_str or dur_str:
                        warnings.append(f"Row {idx} ({record_id}): Open incident has ResolvedDate or duration populated")
                        
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
            for w in warnings[:3]:
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
