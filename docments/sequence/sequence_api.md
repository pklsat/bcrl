```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant api as APIServer
    participant app as APP+APIServer
    Client->>+api: Request
    api ->>+app: Request
    app->>app: main.py
    app->>-api: Response
    api->>-Client: Response
```