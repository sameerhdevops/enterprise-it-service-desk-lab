#!/usr/bin/env python3
"""
Enterprise IT Service Desk & End-User Support Operations Lab
Service Desk Reporting and MIS Generator
Author: Sameer Kulkarni (L1 Support Engineer)
Platform: Python 3 Standard Library Only (No external dependencies)
"""

import csv
import sys
import os
from datetime import datetime
from collections import Counter, defaultdict

# SLA Resolution Targets in Hours
SLA_TARGETS_HOURS = {
    'P1': 4.0,     # Critical: 4 hours
    'P2': 8.0,     # High: 8 business hours
    'P3': 72.0,    # Medium: 3 business days (72 hours)
    'P4': 120.0    # Low: 5 business days (120 hours)
}

def resolve_path(relative_path):
    """Resolve path relative to repo root."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

def load_incidents(filepath=None):
    """Load and parse incidents CSV file."""
    if filepath is None:
        filepath = resolve_path('incidents/incident-register.csv')
    
    if not os.path.exists(filepath):
        print(f"Error: Incident register not found at {filepath}", file=sys.stderr)
        return []
    
    incidents = []
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean string values
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            incidents.append(clean_row)
    return incidents

def load_service_requests(filepath=None):
    """Load and parse service requests CSV file."""
    if filepath is None:
        filepath = resolve_path('incidents/service-requests.csv')
    
    if not os.path.exists(filepath):
        return []
    
    requests = []
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            requests.append(clean_row)
    return requests

def generate_daily_summary(incidents):
    """Generate Daily Service Desk Summary Report."""
    total = len(incidents)
    status_counts = Counter(inc['Status'] for inc in incidents)
    priority_counts = Counter(inc['Priority'] for inc in incidents)
    
    open_tickets = sum(status_counts[s] for s in ['New', 'InProgress', 'Escalated'])
    resolved_tickets = status_counts.get('Resolved', 0)
    closed_tickets = status_counts.get('Closed', 0)
    
    lines = [
        "=" * 65,
        "   NEXORA TECHNOLOGIES - IT SERVICE DESK DAILY SUMMARY",
        f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST",
        "=" * 65,
        f"Total Logged Incidents:       {total}",
        f"Active Open / In-Progress:    {open_tickets}",
        f"Resolved Incidents:           {resolved_tickets}",
        f"Closed Incidents:             {closed_tickets}",
        "-" * 65,
        "INCIDENTS BY PRIORITY:",
    ]
    for p in ['P1', 'P2', 'P3', 'P4']:
        count = priority_counts.get(p, 0)
        pct = (count / total * 100) if total else 0
        lines.append(f"  {p} - {count:2d} ({pct:5.1f}%)")
    
    lines.append("-" * 65)
    lines.append("INCIDENTS BY STATUS:")
    for st, count in status_counts.items():
        lines.append(f"  {st:15s}: {count:2d}")
    lines.append("=" * 65)
    return "\n".join(lines)

def generate_priority_report(incidents):
    """Generate Incident Priority Distribution Report."""
    total = len(incidents)
    priority_counts = Counter(inc['Priority'] for inc in incidents)
    
    lines = [
        "=" * 65,
        "   NEXORA TECHNOLOGIES - TICKET PRIORITY BREAKDOWN",
        "=" * 65,
        f"{'Priority':<10}{'Severity':<15}{'Target Resolution':<22}{'Count':<8}{'Share':<8}",
        "-" * 65
    ]
    labels = {
        'P1': ('Critical', '4 Hours'),
        'P2': ('High', '8 Business Hours'),
        'P3': ('Medium', '3 Business Days'),
        'P4': ('Low', '5 Business Days')
    }
    for p in ['P1', 'P2', 'P3', 'P4']:
        count = priority_counts.get(p, 0)
        pct = (count / total * 100) if total else 0
        sev, target = labels.get(p, ('Unknown', 'N/A'))
        lines.append(f"{p:<10}{sev:<15}{target:<22}{count:<8}{pct:>5.1f}%")
    lines.append("-" * 65)
    lines.append(f"Total Evaluated Incidents: {total}")
    lines.append("=" * 65)
    return "\n".join(lines)

def generate_sla_report(incidents):
    """Generate SLA Compliance Report."""
    sla_data = defaultdict(lambda: {'total': 0, 'met': 0, 'breached': 0})
    
    for inc in incidents:
        p = inc.get('Priority', 'Unknown')
        sla_data[p]['total'] += 1
        
        # Check SLA status
        slam = inc.get('SLAMet', '').strip().lower()
        if slam in ['yes', 'true', '1']:
            sla_data[p]['met'] += 1
        elif slam in ['no', 'false', '0']:
            sla_data[p]['breached'] += 1
        else:
            # Check numerically if ResolutionTime_Hours exists
            res_str = inc.get('ResolutionTime_Hours', '').strip()
            if res_str:
                try:
                    res_time = float(res_str)
                    target = SLA_TARGETS_HOURS.get(p, 72.0)
                    if res_time <= target:
                        sla_data[p]['met'] += 1
                    else:
                        sla_data[p]['breached'] += 1
                except ValueError:
                    sla_data[p]['met'] += 1
            else:
                # If unresolved but past SLA
                sla_data[p]['met'] += 1

    lines = [
        "=" * 70,
        "   NEXORA TECHNOLOGIES - SLA COMPLIANCE REPORT",
        "=" * 70,
        f"{'Priority':<10}{'Target':<12}{'Total':<8}{'SLA Met':<10}{'Breached':<10}{'Compliance %':<12}",
        "-" * 70
    ]
    tot_inc = 0
    tot_met = 0
    tot_brk = 0
    
    for p in ['P1', 'P2', 'P3', 'P4']:
        t = sla_data[p]['total']
        m = sla_data[p]['met']
        b = sla_data[p]['breached']
        tot_inc += t
        tot_met += m
        tot_brk += b
        target_str = f"{int(SLA_TARGETS_HOURS[p])}h"
        pct = (m / t * 100) if t else 100.0
        lines.append(f"{p:<10}{target_str:<12}{t:<8}{m:<10}{b:<10}{pct:>10.1f}%")
        
    lines.append("-" * 70)
    overall_pct = (tot_met / tot_inc * 100) if tot_inc else 100.0
    lines.append(f"{'OVERALL':<22}{tot_inc:<8}{tot_met:<10}{tot_brk:<10}{overall_pct:>10.1f}%")
    lines.append("=" * 70)
    return "\n".join(lines)

def generate_category_report(incidents):
    """Generate Category and Subcategory Analysis Report."""
    cat_counts = Counter(inc['Category'] for inc in incidents)
    cat_resolved = defaultdict(int)
    cat_times = defaultdict(list)
    
    for inc in incidents:
        c = inc['Category']
        if inc['Status'] in ['Resolved', 'Closed']:
            cat_resolved[c] += 1
        res_str = inc.get('ResolutionTime_Hours', '').strip()
        if res_str:
            try:
                cat_times[c].append(float(res_str))
            except ValueError:
                pass

    lines = [
        "=" * 72,
        "   NEXORA TECHNOLOGIES - INCIDENT CATEGORY ANALYSIS",
        "=" * 72,
        f"{'Category':<18}{'Total':<8}{'Resolved':<10}{'Resolve Rate':<15}{'Avg Resolution':<15}",
        "-" * 72
    ]
    for c, total in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        res = cat_resolved[c]
        rate = (res / total * 100) if total else 0
        times = cat_times[c]
        avg_time = (sum(times) / len(times)) if times else 0.0
        lines.append(f"{c:<18}{total:<8}{res:<10}{rate:>11.1f}%   {avg_time:>9.2f} hrs")
        
    lines.append("=" * 72)
    return "\n".join(lines)

def generate_weekly_mis(incidents, service_requests=None):
    """Generate Weekly Management Information System (MIS) Report."""
    if service_requests is None:
        service_requests = []
        
    total_inc = len(incidents)
    total_sr = len(service_requests)
    
    # Calculate group distribution
    group_counts = Counter(inc.get('AssignmentGroup', 'Unassigned') for inc in incidents)
    dept_counts = Counter(inc.get('Department', 'General') for inc in incidents)
    
    # Average resolution time across all resolved incidents
    res_times = []
    for inc in incidents:
        val = inc.get('ResolutionTime_Hours', '').strip()
        if val:
            try:
                res_times.append(float(val))
            except ValueError:
                pass
    avg_res_time = sum(res_times) / len(res_times) if res_times else 0.0
    
    # Escalation metrics
    escalated_count = sum(1 for inc in incidents if inc.get('Status') == 'Escalated' or inc.get('EscalatedTo', '').strip() not in ['', '—', '-'])
    
    lines = [
        "=" * 75,
        "   NEXORA TECHNOLOGIES - WEEKLY IT SERVICE DESK MIS REPORT",
        f"   Reporting Period: November 2024 (Consolidated)",
        "=" * 75,
        f"EXECUTIVE SUMMARY:",
        f"  Total IT Interactions Logged:      {total_inc + total_sr}",
        f"  Total Incident Tickets:            {total_inc}",
        f"  Total Service Requests:            {total_sr}",
        f"  Mean Time to Resolve (MTTR):       {avg_res_time:.2f} hours",
        f"  Total Escalated to L2/L3:          {escalated_count} ({(escalated_count/total_inc*100 if total_inc else 0):.1f}%)",
        "-" * 75,
        "TICKETS BY ASSIGNMENT GROUP:",
    ]
    for grp, cnt in group_counts.most_common():
        lines.append(f"  {grp:<30}: {cnt:2d} ({(cnt/total_inc*100):.1f}%)")
        
    lines.append("-" * 75)
    lines.append("INCIDENTS BY IMPACTED DEPARTMENT:")
    for dept, cnt in dept_counts.most_common():
        lines.append(f"  {dept:<30}: {cnt:2d} ({(cnt/total_inc*100):.1f}%)")
        
    lines.append("=" * 75)
    return "\n".join(lines)

def main():
    args = sys.argv[1:]
    command = "all"
    save_reports = False
    
    if "--save" in args:
        save_reports = True
        args.remove("--save")
        
    if args:
        command = args[0].lower()
        
    incidents = load_incidents()
    service_requests = load_service_requests()
    
    if not incidents:
        print("No incident data found to analyze.")
        sys.exit(1)
        
    reports = {
        'daily': ("daily-report.txt", generate_daily_summary(incidents)),
        'priority': ("priority-report.txt", generate_priority_report(incidents)),
        'sla': ("sla-report.txt", generate_sla_report(incidents)),
        'category': ("category-report.txt", generate_category_report(incidents)),
        'weekly': ("weekly-report.txt", generate_weekly_mis(incidents, service_requests))
    }
    
    if command == "all":
        for name, (filename, content) in reports.items():
            print(content)
            print("\n")
            if save_reports:
                out_path = resolve_path(os.path.join('reporting/reports', filename))
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[Saved] {out_path}")
    elif command in reports:
        filename, content = reports[command]
        print(content)
        if save_reports:
            out_path = resolve_path(os.path.join('reporting/reports', filename))
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n[Saved] {out_path}")
    else:
        print(f"Unknown command: '{command}'. Valid options: daily, priority, sla, category, weekly, all")
        sys.exit(1)

if __name__ == '__main__':
    main()
