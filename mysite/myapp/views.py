from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .GetCandidates import GetCandidates

import requests


@api_view(['GET'])
def get_league_data(request, league_id):
    try:
        r1 = requests.get(url='https://draft.premierleague.com/api/league/' + league_id + '/details')
        r1.raise_for_status()
        result = r1.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return Response(result)


@api_view(['GET'])
def get_element_status(request, league_id):
    try:
        r1 = requests.get(url='https://draft.premierleague.com/api/league/' + league_id + '/element-status')
        r1.raise_for_status()
        result = r1.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return Response(result)


@api_view(['GET'])
def get_boostrap(request):
    try:
        r1 = requests.get(url='https://draft.premierleague.com/api/bootstrap-static')
        r1.raise_for_status()
        players = r1.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return Response(players)


@api_view(['GET'])
def get_candidates(request, league_id, team_name):
    getCandidates = GetCandidates(league_id, team_name)
    response_dict = [{k: v for k, v in d.items() if k in ('id', '6GW Candidates', 'NGW Candidates',
                    '6GW Pts Projection', 'NGW Pts Projection')} for d in getCandidates.team.playersInTeam]
    return JsonResponse(response_dict, safe=False)
