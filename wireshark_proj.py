import openpyxl
import pyshark
import pandas as pd
import numpy as np

cap = pyshark.FileCapture(r"C:\Users\hp\Documents\newcapture.pcapng")

packet_data=[]

for i, packet in enumerate(cap):
    if i >= 1000:
        break

    src_ip = dst_ip = proto = None

    if 'IP' in packet:
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        proto = packet.highest_layer

    elif 'IPv6' in packet:
        src_ip = packet.ipv6.src
        dst_ip = packet.ipv6.dst
        proto = packet.highest_layer

    else:
        proto = packet.highest_layer  # For ARP, etc.

    packet_data.append({
        "No": i + 1,
        "Source IP": src_ip,
        "Destination IP": dst_ip,
        "Protocol": proto,
    })


df = pd.DataFrame(packet_data)
print(f"\nPacket #{i + 1}",df)

total_packets=df.shape[0]
print("The total no. of packets are:",total_packets)

unique_protocols=np.unique(df['Protocol'])
print("The total no. of unique protocols are:",unique_protocols)

nan_src_count = np.sum(pd.isna(df['Source IP']))
nan_dst_count = np.sum(pd.isna(df['Destination IP']))

print("Packets with missing Source IP:", nan_src_count)
print("Packets with missing Destination IP:", nan_dst_count)

missing_source_indices = np.where(pd.isna(df['Source IP']))[0]
missing_destination_indices = np.where(pd.isna(df['Destination IP']))[0]

print("Packet indices with missing Source IP:", missing_source_indices)
print("Packet indices with missing Destination IP:", missing_destination_indices)

protocol_counts = df['Protocol'].value_counts().to_numpy()
protocol_names = df['Protocol'].value_counts().index.to_numpy()

print("Most common protocols:")
for name, count in zip(protocol_names, protocol_counts):
    print(f"{name}: {count} packets")

structured = df[['Protocol', 'No']].to_records(index=False)

protocols = np.unique(structured['Protocol'])

print("\nAverage packet number by protocol:")
for proto in protocols:
    avg_no = np.mean(structured['No'][structured['Protocol'] == proto])
    print(f"{proto}: {avg_no:.2f}")

df.to_excel(r"C:\Users\hp\Documents\packet_analysis.xlsx", index=False)
print("\nData exported to C:\\Users\\hp\\Documents\\packet_analysis.xlsx")

