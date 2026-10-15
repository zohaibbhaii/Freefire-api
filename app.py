# LEGEND FF API
# Powered by LEGEND

import os
import asyncio
from flask import Flask, request, jsonify
from get_jwt import create_jwt
from count_likes import GetAccountInformation
from encrypt_like_body import create_like_payload
import httpx
import json

app = Flask(__name__)

SUPPORTED_REGIONS = ["IND", "BR", "SG", "RU", "ID", "TW", "US", "VN", "TH", "ME", "PK", "CIS"]


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "ok",
        "service": "LEGEND FF API",
        "powered_by": "LEGEND"
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})


@app.route('/info', methods=['GET'])
def info_endpoint():
    uid = request.args.get("uid")
    region = request.args.get("region", "IND").upper()

    if not uid or not uid.isdigit():
        return jsonify({"error": "uid required"}), 400
    if region not in SUPPORTED_REGIONS:
        return jsonify({"error": f"invalid region. use: {SUPPORTED_REGIONS}"}), 400

    try:
        info = asyncio.run(GetAccountInformation(uid, "0", region, "/GetPlayerPersonalShow"))
        basic = info.get("basicInfo", {})
        return jsonify({
            "status": "ok",
            "region": region,
            "uid": uid,
            "player_name": basic.get("nickname", "unknown"),
            "likes": basic.get("liked", 0),
            "level": basic.get("level", "?"),
            "powered_by": "LEGEND"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/jwt', methods=['GET'])
def jwt_endpoint():
    region = request.args.get("region", "IND").upper()
    if region not in SUPPORTED_REGIONS:
        return jsonify({"error": "invalid region"}), 400
    return jsonify({
        "status": "ok",
        "region": region,
        "note": "JWT generation requires guest account. See /info and /like endpoints.",
        "powered_by": "LEGEND"
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"LEGEND FF API running on {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
