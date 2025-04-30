```mermaid
sequenceDiagram
    autonumber
    participant cli as Client
    participant api as APIServer
    participant req as reqest/[uuid].json
    participant sat as status.json
    participant res as respons/[uuid].json
    participant app as APPServer


    par monitor/1min
        app -->> sat: cron monitor {status:pending}
    end

    rect rgb(191, 255, 241)
        par async
            cli ->> api: POST /submit, {SocRequest}
            api ->> req: new
            note over req : xxx.json
            api ->> sat: add ★FileLock
            note over sat : {uuid:xxx, api:soc, status:pending}
        end
    end

    par async
        cli ->>+ api: GET /jobs/{uuid}/status
        api ->> sat: read
        api ->>- cli: {JobStatusResponse}
    end

    app -->> sat: cron monitor {status:pending}
    app -->> sat: cron update ★FileLock
    note over sat : {uuid:xxx, api:soc, status:processing}
    app ->> app: main.py
    activate app
    
    par async
        cli ->>+ api: GET /jobs/{uuid}/status
        api ->> sat: read
        api ->>- cli: {JobStatusResponse}
    end

    rect rgb(191, 255, 241)
        par async
            cli ->> api: POST /submit, {SocRequest}
            api ->> req: new
            note over req : xxx.json
            api ->> sat: add ★FileLock
            note over sat : {uuid:xxx, api:soc, status:pending}
        end
    end

    app ->> res: new
    note over res : xxx.json
    app ->> sat: update ★FileLock
    deactivate app
    note over sat : {uuid:xxx, api:soc, status:done}

    par async
        cli ->>+ api: /jobs/{uuid}/status
        api ->> sat: read
        api ->>- cli: {JobStatusResponse}
    end

    cli ->>+ api: GET jobs/{uuid}/results
    api ->> res: read xxx.json
    api ->>- cli: {SocResponse}