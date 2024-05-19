"""
This small program is used to calculate:
- throughput
- run time of the program
"""
amount_of_samples = int(input("Amount of samples?"))
sample_interval = float(input("sample interal: "))
average_latency = float(input("Average latency: "))

total_time = amount_of_samples * (sample_interval + average_latency)

cumulative_bytes = int(input("Cumulative bytes: "))
total_bits = cumulative_bytes * 8

bps = total_bits / total_time
print(f"bps: {bps:.0f}")
print(f"total time in seconds: {total_bits / bps}")
