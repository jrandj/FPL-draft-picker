from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests


@api_view(['GET'])
def get_league_data(request, league_id):
    try:
        r1 = requests.get(url='https://draft.premierleague.com/api/league/' + league_id +
                              '/details')
        r1.raise_for_status()
        result = r1.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return Response(result)


@api_view(['GET'])
def get_element_status(request, league_id):
    try:
        r1 = requests.get(url='https://draft.premierleague.com/api/league/' + league_id +
                              '/element-status')
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
