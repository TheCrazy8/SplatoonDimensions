#!/usr/bin/env python3
"""
GitHub Device Flow server.

Endpoints:
  GET  /device/start    -> start device flow (returns device_code, user_code, verification_uri, interval, expires_in)
  POST /device/poll     -> body { "device_code": "...", "max_wait": 300 } -> polls GitHub until token or error
  GET  /health
Environment variables:
  GITHUB_CLIENT_ID      - required
  GITHUB_CLIENT_SECRET  - optional (not required to get token, but may be used server-side)
  FRONTEND_URL          - allowed origin for CORS (e.g. https://your-frontend.example.com)
  SECRET_KEY            - optional, used for Flask sessions (defaults to random)
"""
import os
import time
from typing import Tuple

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

GITHUB_DEVICE_CODE_URL = "https://github.com/login/device/code"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(24)

# Configure CORS: allow exactly your frontend origin (don't use "*"
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
CORS(app, origins=[FRONTEND_URL])

CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
DEFAULT_SCOPE = os.environ.get("GITHUB_OAUTH_SCOPE", "read:user user:email")

if not CLIENT_ID:
    app.logger.warning("GITHUB_CLIENT_ID not set; device flow will fail until configured.")


@app.route("/device/start", methods=["GET"])
def device_start():
    """
    Start the device flow by asking GitHub for device & user codes.
    Returns JSON containing:
      device_code, user_code, verification_uri, expires_in, interval
    """
    if not CLIENT_ID:
        return jsonify({"error": "server_misconfigured", "message": "GITHUB_CLIENT_ID not set on server"}), 500

    data = {"client_id": CLIENT_ID, "scope": DEFAULT_SCOPE}
    headers = {"Accept": "application/json"}

    try:
        resp = requests.post(GITHUB_DEVICE_CODE_URL, data=data, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        app.logger.exception("Error requesting device code from GitHub")
        return jsonify({"error": "fetch_failed", "message": "Failed to start device flow", "detail": str(exc)}), 502

    return jsonify(resp.json())


def github_poll_for_token(device_code: str, max_wait: int = 600) -> Tuple[dict, int]:
    """
    Poll GitHub for an access token. Returns (result_json, status_code).
    This will block while polling; for production use a background worker or short-poll style.
    """
    params = {
        "client_id": CLIENT_ID,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    headers = {"Accept": "application/json"}

    interval = 5
    waited = 0
    start = time.time()

    while waited < max_wait:
        try:
            resp = requests.post(GITHUB_ACCESS_TOKEN_URL, data=params, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as exc:
            app.logger.exception("Error polling GitHub for access token")
            return {"error": "fetch_failed", "message": str(exc)}, 502

        j = resp.json()

        if "access_token" in j:
            token = {
                "access_token": j.get("access_token"),
                "token_type": j.get("token_type"),
                "scope": j.get("scope"),
            }
            return {"success": True, "token": token}, 200

        error = j.get("error")
        if error == "authorization_pending":
            time.sleep(interval)
            waited = int(time.time() - start)
            continue
        if error == "slow_down":
            interval += 5
            time.sleep(interval)
            waited = int(time.time() - start)
            continue
        if error == "access_denied":
            return {"error": "access_denied", "message": "User denied the request"}, 403
        if error == "expired_token":
            return {"error": "expired_token", "message": "Device code expired"}, 410

        # unknown
        return {"error": "github_error", "detail": j}, 400

    return {"error": "timeout", "message": "Timed out waiting for user authorization"}, 408


@app.route("/device/poll", methods=["POST"])
def device_poll():
    """
    Poll for token server-side. Expects JSON body:
      { "device_code": "<device_code_from_start>", "max_wait": 300 }
    On success returns { token: {access_token, token_type, scope}, user: { ... } }
    """
    body = request.get_json(silent=True) or {}
    device_code = body.get("device_code")
    max_wait = int(body.get("max_wait", 300))

    if not device_code:
        return jsonify({"error": "missing_parameter", "message": "device_code is required"}), 400
    if not CLIENT_ID:
        return jsonify({"error": "server_misconfigured", "message": "GITHUB_CLIENT_ID not set on server"}), 500

    result, status = github_poll_for_token(device_code=device_code, max_wait=max_wait)
    if status != 200:
        return jsonify(result), status

    token = result["token"]["access_token"]
    user = {}
    try:
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        user_resp = requests.get(GITHUB_USER_API, headers=headers, timeout=10)
        user_resp.raise_for_status()
        user = user_resp.json()
    except Exception:
        user = {}

    return jsonify({"token": result["token"], "user": user}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "frontend": FRONTEND_URL})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)