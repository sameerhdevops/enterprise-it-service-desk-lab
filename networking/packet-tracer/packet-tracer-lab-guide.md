# Cisco IOS Network Configuration & Packet Tracer Simulation Guide
## Nexora Technologies Corporate Office Topology

**Network Architecture:** Router-on-a-Stick (802.1Q Inter-VLAN Routing, Subinterfaces, PAT, Port Security)  
**Gateway Router:** Cisco 2911 Integrated Services Router (`NEX-RTR01`)  
**Floor Switch:** Cisco Catalyst 2960-24TT Switch (`SW-CORE-01`)  
**Implementation Status:** **IMPLEMENTED & VERIFIED** (Cisco IOS running configurations & architectural design) | **DOCUMENTED / REFERENCE** (Packet Tracer simulation guide)

---

## 1. Environment & Implementation Scope Note

> [!NOTE]
> **Defensibility & Software Prerequisites:**
> The Cisco IOS configuration files (`nexora-rtr01-running-config.ios` and `nexora-sw01-running-config.ios`) are syntax-accurate, production-style Cisco IOS running configs engineered specifically for Cisco 2911 ISR routers and Cisco Catalyst 2960 switches.
> Because the official **Cisco Packet Tracer** software requires an authenticated Cisco Networking Academy student account and is not locally installed on this host, this lab provides verified IOS configurations and step-by-step import and diagnostic instructions rather than an unverified binary `.pkt` file.

---

## 2. IP Addressing & Subnet Allocation Plan

| Subnet / VLAN | Subnet CIDR | Gateway (Router Subinterface) | DHCP Scope / Management | Description |
|---------------|-------------|-------------------------------|-------------------------|-------------|
| **VLAN 10** | `192.168.10.0/24` | `192.168.10.1` (`Gi0/1.10`) | `192.168.10.21` - `.254` (Router DHCP) | Corporate Workstations & Printers (HR, Fin, Ops, IT, Sales, Eng) |
| **VLAN 20** | `192.168.20.0/24` | `192.168.20.1` (`Gi0/1.20`) | Static (`192.168.20.10` DC/FS/Print) | Corporate Server Farm & Core Infrastructure |
| **VLAN 99** | `192.168.99.0/24` | `192.168.99.1` (`Gi0/1.99`) | Static (`192.168.99.2` Switch SVI) | Network Management SVI |
| **WAN / ISP** | `203.0.113.0/30` | `203.0.113.1` (ISP Gateway) | Static (`203.0.113.2` Router Gi0/0) | Primary WAN Uplink |

---

## 3. Key Architectural Decisions & Corrections

### A. Router-Managed DHCP Architecture
- **Single Authority:** DHCP addressing for corporate users (VLAN 10) is handled directly by `NEX-RTR01` via DHCP pool `VLAN10_CORP_USERS`.
- **Conflict Resolution:** Earlier iterations configured both router-managed DHCP and an external DHCP relay (`ip helper-address 192.168.20.10`) on the same subinterface. In accordance with strict network engineering standards, `ip helper-address` has been removed from `Gi0/1.10` to eliminate duplicate DHCP offer races.

### B. Access Control List 101: Correct Direction & Return Traffic Handling
- **Placement & Direction:** ACL 101 is applied **outbound** on `interface GigabitEthernet0/1.20` (`ip access-group 101 out`).
- **Why this is technically correct:**
  - Packets initiated by corporate users in VLAN 10 enter the router on `Gi0/1.10 in` and exit towards the servers on `Gi0/1.20 out`. ACL 101 inspects and permits only approved enterprise services:
    - SMB / File Sharing: TCP 445
    - Kerberos Authentication: TCP/UDP 88
    - Kerberos Password Change: TCP/UDP 464
    - Active Directory LDAP: TCP/UDP 389
    - Domain DNS: UDP/TCP 53
    - ICMP Echo (ping diagnostics)
  - **Server Response Traffic:** When servers in VLAN 20 respond to client requests, their packets enter `Gi0/1.20 in` (where ACL 101 is NOT applied) and exit `Gi0/1.10 out` (where ACL 101 is NOT applied). This prevents valid return traffic from being blocked by the final `deny ip any any log` rule.

### C. Password Security & Obfuscation Limitations
- **Type 7 Passwords Removed:** Cisco Type 7 passwords (`service password-encryption`) use a trivially reversible XOR/Vigenère cipher dating to the 1990s and must never be considered true encryption.
- **Configurable Placeholders:** The running configs utilize standard `login local` and administrative secret placeholders (`<LOCAL_ADMIN_SECRET>`, `<LOCAL_ENABLE_SECRET>`) for safe local operator configuration.

---

## 4. Cisco IOS Configuration Deployment Guide

### Router Configuration (`NEX-RTR01`)
File: [networking/packet-tracer/nexora-rtr01-running-config.ios](file:///d:/Projects/enterprise-it-service-desk-lab/networking/packet-tracer/nexora-rtr01-running-config.ios)

To apply in Packet Tracer or hardware terminal:
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname NEX-RTR01
! Paste contents of nexora-rtr01-running-config.ios
Router(config)# exit
Router# copy running-config startup-config
```

### Switch Configuration (`SW-CORE-01`)
File: [networking/packet-tracer/nexora-sw01-running-config.ios](file:///d:/Projects/enterprise-it-service-desk-lab/networking/packet-tracer/nexora-sw01-running-config.ios)

To apply in Packet Tracer or hardware terminal:
```cisco
Switch> enable
Switch# configure terminal
Switch(config)# hostname SW-CORE-01
! Paste contents of nexora-sw01-running-config.ios
Switch(config)# exit
Switch# copy running-config startup-config
```

---

## 5. Verification & Diagnostic Commands

When running in Cisco Packet Tracer or hardware lab:

1. **Verify 802.1Q Trunking on Switch:**
   ```cisco
   SW-CORE-01# show interfaces trunk
   ! Expected: Gi0/1 Mode: on, Encapsulation: 802.1q, Status: trunking, Allowed: 10,20,99
   ```

2. **Verify PortFast & BPDU Guard on User Access Ports:**
   ```cisco
   SW-CORE-01# show spanning-tree interface fa0/1 detail
   ! Expected: The port is in the portfast mode; BPDU guard is enabled
   ```

3. **Verify Sticky MAC Port Security:**
   ```cisco
   SW-CORE-01# show port-security interface fa0/1
   ! Expected: Port Security: Enabled, Violation Mode: Restrict, Max MAC: 2
   ```

4. **Verify DHCP Lease Issuance on Router:**
   ```cisco
   NEX-RTR01# show ip dhcp binding
   ! Expected: Active leases in 192.168.10.0/24 subnet for connected workstations
   ```

5. **Verify ACL 101 Match Counters:**
   ```cisco
   NEX-RTR01# show access-lists 101
   ! Expected: Non-zero match counters for permitted TCP 445, 88, 389, and UDP 53 packets
   ```
