# restaurant_budget_tracker
A microservice that tracks restaurant spending based upon where you've eaten.

In order to send data:

1. Create and bind a ZMQ socket.
2. Send a JSON file that incorporates the following:
    - user_id
    - restaurant_id
    - restaurant_name
    - amount (amount spent)
An example call would be:
````
event = {
    "user_id": 1,
    "restaurant_id": 123123,
    "restaurant_name": "Happi House,
    "amount": 30.54
}

socket.send_string("expense_created " + json.dumps(event))
````

In order to request data:
1. Create and bind a ZMQ socket.
2. Request a specific user's total amount spent!
    Ex:
    ````
    socket.send_json({"user_id": 1})
    response = socket.recv_json()
    ````

```mermaid
    sequenceDiagram
        title Restaurant Budget Tracker Microservice

        participant A as Expense Publishing
        participant ZMQ as ZeroMQ Pipe
        participant Service as Restaurant Budget Tracker Microservice
        participant B as Request Total

        %% Publish Expense
        A->>ZMQ: restaurant_id\nrestaurant_name\nuser_id\namount_spent
        ZMQ->>Service: Forward Expense Data
        Service->>Service: Store Expense\nUpdate Total

        %% Request Total
        B->>ZMQ: user_id
        ZMQ->>Service: Request Total for user_id
        Service->>Service: Calculate / Retrieve Total
        Service-->>ZMQ: total_amount
        ZMQ-->>B: Display total_amount
```