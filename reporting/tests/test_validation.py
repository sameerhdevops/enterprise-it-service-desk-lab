#!/usr/bin/env python3
"""
Unit Test Suite for Service Desk Data Validation and Reporting
Author: Sameer Kulkarni (L1 Support Engineer)
Framework: unittest (Python 3 Standard Library)
"""

import unittest
import os
import sys
from datetime import datetime

# Dynamically import report-generator.py
import importlib.util
script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report-generator.py')
spec = importlib.util.spec_from_file_location("report_generator", script_path)
report_generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report_generator)

# Sample embedded test fixtures to test calculations independently of external files
SAMPLE_VALID_DATA = [
    {
        'IncidentID': 'INC9001',
        'Title': 'Test Laptop issue',
        'ReportedBy': 'Test User',
        'Department': 'HR',
        'Category': 'Hardware',
        'Subcategory': 'Laptop',
        'Priority': 'P1',
        'Impact': '1-High',
        'Urgency': '1-High',
        'Status': 'Resolved',
        'AssignedTo': 'Sameer K',
        'AssignmentGroup': 'L1 Service Desk',
        'ReportedDate': '2024-11-01 09:00',
        'ResolvedDate': '2024-11-01 11:30',
        'ResolutionTime_Hours': '2.5',
        'Description': 'Test issue description',
        'RootCause': 'Test hardware failure',
        'Resolution': 'Test part replacement',
        'EscalatedTo': '—',
        'SLAMet': 'Yes'
    },
    {
        'IncidentID': 'INC9002',
        'Title': 'Test Network slow',
        'ReportedBy': 'Test User 2',
        'Department': 'Finance',
        'Category': 'Network',
        'Subcategory': 'LAN',
        'Priority': 'P2',
        'Impact': '2-Medium',
        'Urgency': '1-High',
        'Status': 'Escalated',
        'AssignedTo': 'Sameer K',
        'AssignmentGroup': 'L1 Service Desk',
        'ReportedDate': '2024-11-01 10:00',
        'ResolvedDate': '',
        'ResolutionTime_Hours': '',
        'Description': 'Test slow connection',
        'RootCause': 'Under investigation',
        'Resolution': 'Escalated to L2',
        'EscalatedTo': 'Arvind Rao',
        'SLAMet': 'No'
    }
]

class TestServiceDeskValidation(unittest.TestCase):

    def test_01_csv_parsing_live(self):
        """Verify real incident-register.csv can be parsed and has expected columns."""
        incidents = report_generator.load_incidents()
        self.assertGreater(len(incidents), 0, "Incident register should contain rows")
        expected_cols = {'IncidentID', 'Title', 'Priority', 'Status', 'Category', 'ReportedDate'}
        first_row = incidents[0]
        for col in expected_cols:
            self.assertIn(col, first_row, f"Required column {col} missing from CSV")

    def test_02_no_duplicate_incident_ids(self):
        """Verify that all IncidentIDs in the live register are strictly unique."""
        incidents = report_generator.load_incidents()
        ids = [inc['IncidentID'] for inc in incidents]
        unique_ids = set(ids)
        self.assertEqual(len(ids), len(unique_ids), f"Duplicate IncidentIDs found in register: {len(ids) - len(unique_ids)}")

    def test_03_valid_priorities(self):
        """Verify all incidents have valid priority values (P1, P2, P3, P4)."""
        incidents = report_generator.load_incidents()
        valid_priorities = {'P1', 'P2', 'P3', 'P4'}
        for inc in incidents:
            self.assertIn(inc['Priority'], valid_priorities, f"Invalid priority '{inc['Priority']}' in {inc['IncidentID']}")

    def test_04_valid_statuses(self):
        """Verify incident statuses match defined ITIL lifecycle states."""
        incidents = report_generator.load_incidents()
        valid_statuses = {'New', 'InProgress', 'OnHold', 'Resolved', 'Closed', 'Escalated'}
        for inc in incidents:
            self.assertIn(inc['Status'], valid_statuses, f"Invalid status '{inc['Status']}' in {inc['IncidentID']}")

    def test_05_date_chronology(self):
        """Verify resolved date is strictly chronologically after reported date."""
        incidents = report_generator.load_incidents()
        for inc in incidents:
            rep_date = inc.get('ReportedDate', '').strip()
            res_date = inc.get('ResolvedDate', '').strip()
            if rep_date and res_date:
                dt_rep = datetime.strptime(rep_date, '%Y-%m-%d %H:%M')
                dt_res = datetime.strptime(res_date, '%Y-%m-%d %H:%M')
                self.assertGreaterEqual(dt_res, dt_rep, f"ResolvedDate {res_date} is earlier than ReportedDate {rep_date} in {inc['IncidentID']}")

    def test_06_report_calculations(self):
        """Test calculation functions using deterministic fixture data."""
        summary = report_generator.generate_daily_summary(SAMPLE_VALID_DATA)
        self.assertIn("Total Logged Incidents:       2", summary)
        self.assertIn("Active Open / In-Progress:    1", summary)
        self.assertIn("Resolved Incidents:           1", summary)
        
        sla_rep = report_generator.generate_sla_report(SAMPLE_VALID_DATA)
        self.assertIn("P1", sla_rep)
        self.assertIn("50.0%", sla_rep)  # 1 of 2 met overall

    def test_07_empty_data_handling(self):
        """Verify report generator handles empty dataset gracefully without raising exceptions."""
        empty_data = []
        try:
            summary = report_generator.generate_daily_summary(empty_data)
            priority = report_generator.generate_priority_report(empty_data)
            sla = report_generator.generate_sla_report(empty_data)
            cat = report_generator.generate_category_report(empty_data)
            weekly = report_generator.generate_weekly_mis(empty_data)
            self.assertIn("Total Logged Incidents:       0", summary)
            self.assertIn("Total Evaluated Incidents: 0", priority)
        except Exception as e:
            self.fail(f"Report generation on empty data crashed with exception: {e}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
