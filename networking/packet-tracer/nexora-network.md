# Nexora Technologies Office Network Topology (Cisco Packet Tracer Specification)
**Document ID:** NET-PKT-001  
**Simulator:** Cisco Packet Tracer (v8.2+)  
**Scope:** Bengaluru Office LAN, VLAN Segmentation, Inter-VLAN Routing, DHCP Services

---

## 1. Network Topology Overview

The Nexora Technologies office network supports ~25 employees across 4 departments with separated user and server subnets:

```
                                [INTERNET]
                                    │
                                [ISP WAN] (203.0.113.1/30)
                                    │ GigabitEthernet 0/0/0
                        +───────────────────────────+
                        |   R1: Cisco 2911 Router   |  (Default Gateway & Inter-VLAN Routing)
                        |   "NEX-RTR01"             |
                        +───────────────────────────+
                                    │ GigabitEthernet 0/0/1 (802.1Q Trunk)
                                    │
                        +───────────────────────────+
                        |  SW1: Cisco 2960 Switch   |  (Core / Distribution Switch)
                        |  "SW-CORE-01"             |
                        +───────────────────────────+
                         │ FastEthernet 0/1          │ FastEthernet 0/2
                         │ (VLAN 10 Access)          │ (VLAN 20 Access)
                         ▼                           ▼
            +─────────────────────────+  +─────────────────────────+
            |  VLAN 10: Corporate LAN |  |  VLAN 20: Server Farm    |
            |  Subnet: 192.168.10.0/24|  |  Subnet: 192.168.20.0/24|
            +─────────────────────────+  +─────────────────────────+
             │           │           │    │           │           │
             ▼           ▼           ▼    ▼           ▼           ▼
          [PC-HR01]  [PC-FIN01]  [PRN01] [NEX-DC01]  [NEX-FS01]  [NEX-APP01]
          .11        .12         .25     .10         .15         .50
```

---

## 2. IP Subnet Plan & VLAN Table

| VLAN ID | VLAN Name | Subnet Range | Gateway IP | Description & Assigned Devices |
|---|---|---|---|---|
| **VLAN 10** | `Corp_Users` | `192.168.10.0/24` | `192.168.10.1` | Employee workstations, laptops, network MFD printers. Dynamic DHCP pool (`.100` to `.200`). |
| **VLAN 20** | `Server_Farm` | `192.168.20.0/24` | `192.168.20.1` | Corporate infrastructure: Domain Controller (DNS/DHCP), File Server, Application Server. Static IPs. |
| **VLAN 99** | `Management` | `192.168.99.0/24` | `192.168.99.1` | Switch and router in-band SSH/SNMP management interface. |

---

## 3. Cisco IOS Configuration Snippets

### Router: Router-on-a-Stick Subinterfaces (NEX-RTR01)
```cisco
hostname NEX-RTR01

! Subinterface for VLAN 10 (Corporate Users)
interface GigabitEthernet0/0/1.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip helper-address 192.168.20.10
!
! Subinterface for VLAN 20 (Server Subnet)
interface GigabitEthernet0/0/1.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
!
! Subinterface for VLAN 99 (Management)
interface GigabitEthernet0/0/1.99
 encapsulation dot1Q 99
 ip address 192.168.99.1 255.255.255.0
```

### Switch: Trunk and Access Port Configuration (SW-CORE-01)
```cisco
hostname SW-CORE-01

! Define VLANs in database
vlan 10
 name Corp_Users
vlan 20
 name Server_Farm
vlan 99
 name Management

! Trunk uplink port to Router
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,99

! Access ports for Corporate Users (VLAN 10)
interface range FastEthernet0/1 - 18
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast

! Access ports for Server Farm (VLAN 20)
interface range FastEthernet0/19 - 24
 switchport mode access
 switchport access vlan 20
```

---

## 4. Connectivity Verification Plan in Packet Tracer
1. **Host-to-Gateway Test:** From `PC-HR01`, ping default gateway `192.168.10.1` (ICMP success rate 100%).
2. **Inter-VLAN Routing Test:** From `PC-HR01` (VLAN 10), ping Domain Controller `192.168.20.10` (VLAN 20).
3. **DHCP DORA Verification:** Toggle desktop PC IP configuration to "DHCP"; verify successful lease from pool `192.168.10.100-200` with correct DNS option (`192.168.20.10`).
4. **Simulation Mode Inspection:** Switch Packet Tracer to Simulation Mode, filter by `ICMP`, `ARP`, and `DNS`, and step through frame encapsulation across switch and router.
