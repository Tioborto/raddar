import binascii
import hmac
import json
import urllib.parse

from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import APIKeyHeader

from raddar.core.settings import settings

GithubSignatureHeader = APIKeyHeader(name="X-Hub-Signature-256")


async def valid_github_webhook(
    *, github_signature: str = Security(GithubSignatureHeader), request: Request
):
    body = await request.body()

    signature = hmac.new(
        settings.API_KEY.get_secret_value().encode(),
        msg=body,
        digestmod="sha256",
    )
    digest = f"sha256={signature.hexdigest()}"
    if not hmac.compare_digest(digest, github_signature):
        raise HTTPException(status_code=401, detail="Bad webhook secret")
