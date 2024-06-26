message = """PING localhost (127.0.0.1) 56(84) bytes of data.
    64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.014 ms

    --- localhost ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.014/0.014/0.014/0.000 ms"""

second_message = """PING localhost (192.168.54.16) 56(84) bytes of data.
    64 bytes from localhost (192.168.54.16): icmp_seq=1 ttl=64 time=0.014 ms

    --- localhost ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.014/0.014/0.014/0.000 ms"""

action_logs = [
  {
    "id": 1,
    "action_id": 1,
    "target": "localhost",
    "action_messages": [
      message
    ]
  },
  {
    "id": 2,
    "action_id": 2,
    "target": "localhost",
    "action_messages": [
      message,
      message,
    ]
  },
  {
    "id": 3,
    "action_id": 2,
    "target": "192.168.54.16",
    "action_messages": [
      second_message,
      second_message
    ]
  },
]
