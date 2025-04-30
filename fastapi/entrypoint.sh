#!/bin/bash
set -e
echo "Entrypoint received arguments: $@"
# コンテナ内の/shared配下を作成
mkdir -p /shared/bcrlapi/request
mkdir -p /shared/bcrlapi/response
if [ ! -f /shared/bcrlapi/request/status.json ]; then
    cp /fastapi/init-status.json /shared/bcrlapi/request/status.json
    # MOCK用の初期データをコピー
    cp /fastapi/response.json /shared/bcrlapi/response/00000000-0000-0000-0000-000000000000.json
fi
exec "$@"
