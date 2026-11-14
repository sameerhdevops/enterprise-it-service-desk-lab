# Cisco Packet Tracer Lab Verification & Troubleshooting Exercise
**Document ID:** NET-PKT-002  
**Simulator Target:** Cisco Packet Tracer 8.0+  
**Target Devices:** Cisco 2911 Router (`NEX-RTR01`), Cisco Catalyst 2960 Switch (`SW-CORE-01`)  
**Configuration Files:** [`nexora-rtr01-running-config.ios`](nexora-rtr01-running-config.ios) | [`nexora-sw01-running-config.ios`](nexora-sw01-running-config.ios)  

---

## 1. Laboratory Verification Runbook

### Test 1: Verify 802.1Q Trunk Status on Switch
```cisco
SW-CORE-01# show interfaces trunk

Port        Mode             Encapsulation  Status        Native vlan
Gi0/1       on               802.1q         trunking      1

Port        Vlans allowed on trunk
Gi0/1       10,20,99

Port        Vlans in spanning tree forwarding state and not pruned
Gi0/1       10,20,99
```
*Interpretation:* Port `Gi0/1` is actively trunking and forwarding traffic for user VLAN 10 and server VLAN 20 to the router.

### Test 2: Verify Router-on-a-Stick Subinterfaces & IP Routing
```cisco
NEX-RTR01# show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0/0       203.0.113.2     YES manual up                    up      
GigabitEthernet0/0/1       unassigned      YES unset  up                    up      
GigabitEthernet0/0/1.10    192.168.10.1    YES manual up                    up      
GigabitEthernet0/0/1.20    192.168.20.1    YES manual up                    up      
GigabitEthernet0/0/1.99    192.168.99.1    YES manual up                    up      
```
*Interpretation:* All three 802.1Q subinterfaces are UP/UP and bound to their respective default gateway IP addresses.

### Test 3: DHCP Pool Lease Verification
```cisco
NEX-RTR01# show ip dhcp binding
IP address       Client-ID/Hardware address   Lease expiration        Type
192.168.10.21    0050.7966.6801               --                      Automatic
192.168.10.22    0050.7966.6802               --                      Automatic
```
*Interpretation:* Workstations `PC-HR01` and `PC-FIN01` successfully completed the DORA handshake and leased addresses in the `.21`+ range.

---

## 2. Practical L1 Troubleshooting Scenario: "Workstation Isolated with APIPA Address"

### Reported Incident:
Workstation `PC-FIN01` plugged into switch port `Fa0/5` cannot browse the intranet or reach any shared folders. Running `ipconfig` returns an APIPA address: `169.254.120.44`.

### Triage Sequence:
1. **Physical Layer Check:**
   `show interfaces fastethernet 0/5` $\rightarrow$ Port is `up/up`. Link lights are green.
2. **VLAN Assignment Check on Switch:**
   ```cisco
   SW-CORE-01# show mac address-table interface fastethernet 0/5
             Mac Address Table
   -------------------------------------------
   Vlan    Mac Address       Type        Ports
   ----    -----------       --------    -----
      1    0050.7966.6802    DYNAMIC     Fa0/5
   ```
   **Root Cause Identified:** Port `Fa0/5` was left on the default unconfigured `VLAN 1`, which has no DHCP server, no default gateway, and no routing!
3. **Corrective Command Sequence:**
   ```cisco
   SW-CORE-01# configure terminal
   SW-CORE-01(config)# interface FastEthernet0/5
   SW-CORE-01(config-if)# switchport mode access
   SW-CORE-01(config-if)# switchport access vlan 10
   SW-CORE-01(config-if)# spanning-tree portfast
   SW-CORE-01(config-if)# end
   SW-CORE-01# write memory
   ```
4. **Client-Side Verification:**
   On `PC-FIN01`, run:
   ```cmd
   ipconfig /renew
   ```
   *Result:* Acquired `192.168.10.22`, Default Gateway `192.168.10.1`, DNS `192.168.20.10`.
   Ping to `192.168.10.1` and `192.168.20.10` replies in <1ms. Issue resolved.
