"""This module implements the request handlers for the endpoints of the Asset
Inventory API related to team operations."""

from flask import jsonify

from graph_asset_inventory_api.context import get_inventory_client
from graph_asset_inventory_api.inventory import NotFoundError
from graph_asset_inventory_api.api import TeamResp


def get_teams(page=None, size=None):
    """Request handler for the API endpoint ``/v1/teams``."""
    cli = get_inventory_client()

    teams = None
    if not page or not size:
        teams = cli.teams()
    else:
        teams = cli.teams_page(page, size)

    resp = [TeamResp.from_dbteam(t).__dict__ for t in teams]
    return jsonify(resp), 200


def get_teams_id(id):  # pylint: disable=redefined-builtin
    """Request handler for the API endpoint ``/v1/teams/{id}``."""
    cli = get_inventory_client()

    team = None
    try:
        team = cli.team(id)
    except NotFoundError:
        return jsonify(error='id not found'), 404

    resp = TeamResp.from_dbteam(team).__dict__
    return jsonify(resp), 200
