"""
Blueprint API — routes extraites de app.py.
D'autres routes peuvent être déplacées ici progressivement.
"""

from flask import Blueprint, current_app, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/ping", methods=["GET"])
def ping():
    """Endpoint léger pour vérifier que l'API répond."""
    return jsonify({"ok": True, "service": "arkalia-quest"})


@api_bp.route("/luna-emotions", methods=["GET"])
def luna_emotions():
    """API pour les émotions de LUNA."""
    engine = current_app.config.get("LUNA_EMOTIONS_ENGINE")
    if not engine:
        return jsonify({"success": False, "error": "Moteur non disponible"}), 503
    try:
        emotions_data = engine.get_current_state()
        return jsonify({"success": True, "emotion": emotions_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/mission-handler/available", methods=["GET"])
def mission_handler_available():
    """API pour les missions disponibles via le gestionnaire unifié."""
    mission_unified = current_app.config.get("MISSION_UNIFIED")
    if not mission_unified:
        return jsonify({"success": False, "error": "Gestionnaire non disponible"}), 503
    try:
        available_missions = mission_unified.get_all_missions()
        return jsonify({"success": True, "missions": available_missions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
