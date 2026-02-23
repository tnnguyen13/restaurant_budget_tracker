import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

# Request total spending for user_id=1
socket.send_json({"user_id": 1})
response = socket.recv_json()

print("Summary:", response)