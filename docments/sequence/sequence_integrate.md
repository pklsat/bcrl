```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant api as API+APPServer
    Client->>+api: Request
    api->>api: main.py
    api->>-Client: Response
```