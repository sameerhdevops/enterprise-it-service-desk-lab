# Nexora Technologies Office Network Topology (Cisco Packet Tracer Specification)
**Document ID:** NET-PKT-001
**Simulator:** Cisco Packet Tracer (v8.2+)
**Scope:** Bengaluru Office LAN, VLAN Segmentation, Inter-VLAN Routing, DHCP Services
**Classification:** Reference Configuration Draft (Educational Lab Design)

> ⚠️ **Reference Configuration Note:** The Cisco IOS running configurations and network designs in this folder are reference implementation drafts. The repository does not include a compiled `.pkt` binary simulator file, and these configurations have not been deployed on physical Cisco hardware.

---

## 1. Network Topology Overview

The Nexora Technologies office network supports ~25 employees across 4 departments with separated user and server subnets:

```
                                [INTERNET]
                                    │
                                [ISP WAN] (203.0.113.1/30)
                                    │ GigabitEthernet0/0
                        +───────────────────────────+
                        |   R1: Cisco 2911 Router   |  (Default Gateway & Inter-VLAN Routing)
                        |   "NEX-RTR01"             |
                        +───────────────────────────+
                                    │ GigabitEthernet0/1 (802.1Q Trunk)
                                    │
                        +───────────────────────────+
                        |  SW1: Cisco 2960 Switch   |  (Core / Distribution Switch)
                        |  "SW-CORE-01"             |
                        +───────────────────────────+
                         │ FastEthernet0/1           │ FastEthernet0/2
                         │ (VLAN 10 Access)          │ (VLAN 20 Access)
                         ▼                           ▼
            +─────────────────────────+  +─────────────────────────+
            |  VLAN 10: Corporate LAN |  |  VLAN 20: Server Farm    |
            |  Subnet: 192.168.10.0/24|  |  Subnet: 192.168.20.0/24|
            +─────────────────────────+  +─────────────────────────+
             │           │           │    │           │           │
             ▼           ▼           ▼    ▼           ▼           ▼
          [PC-HR01]  [PC-FIN01]  [PRN01] [NEX-DC01]  [NEX-FS01]  [NEX-APP01]
          .21        .22         .25     .10         .15         .50
```

---

## 2. IP Subnet Plan & VLAN Table

| VLAN ID | VLAN Name | Subnet Range | Gateway IP | Description & Assigned Devices |
|---|---|---|---|---|
| **VLAN 10** | `Corp_Users` | `192.168.10.0/24` | `192.168.10.1` | Workstations, laptops, network printers. Router DHCP pool (`.21` to `.254`). Static exclusions: `.1` to `.20`. |
| **VLAN 20** | `Server_Farm` | `192.168.20.0/24` | `192.168.20.1` | Corporate infrastructure: Domain Controller (`.10`), File Server (`.15`), App Server (`.50`). Static IPs exclusively. |
| **VLAN 99** | `Management` | `192.168.99.0/24` | `192.168.99.1` | Switch and router in-band SSH/management SVI (`.2`). |

---

## 3. Cisco IOS Configuration Snippets

### Router: Router-on-a-Stick Subinterfaces (NEX-RTR01)
```cisco
hostname NEX-RTR01

! WAN Uplink
interface GigabitEthernet0/0
 description WAN Uplink to ISP
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
!
! Physical Trunk Port to Switch
interface GigabitEthernet0/1
 description Trunk Link to SW-CORE-01
 no ip address
!
! Subinterface for VLAN 10 (Corporate Users)
interface GigabitEthernet0/1.10
 description Corporate Users LAN
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
!
! Subinterface for VLAN 20 (Server Subnet)
interface GigabitEthernet0/1.20
 description Corporate Server Farm
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 ip nat inside
!
! Subinterface for VLAN 99 (Management)
interface GigabitEthernet0/1.99
 description Management SVI
 encapsulation dot1Q 99
 ip address 192.168.99.1 255.255.255.0
```

### Router-Managed DHCP Pool (VLAN 10)
```cisco
! Exclude static IPs (.1 to .20 for gateway, switches, and printers)
ip dhcp excluded-address 192.168.10.1 192.168.10.20

! Pool for corporate users (leases .21 to .254)
ip dhcp pool VLAN10_CORP_USERS
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 192.168.20.10 8.8.8.8
 domain-name nexora.test
 lease 7
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
3. **DHCP Lease Verification:** Configure desktop PC to "DHCP"; verify successful lease from pool `192.168.10.21-254` with correct default gateway (`192.168.10.1`) and DNS options (`192.168.20.10`).
4. **Simulation Mode Inspection:** Switch Packet Tracer to Simulation Mode, filter by `ICMP`, `ARP`, and `DNS`, and step through frame encapsulation across switch and router.
