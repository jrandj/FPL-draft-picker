Returns available players in the selected league that have a higher projected score than your existing players.

Update the below values in app.py accordingly.

.. code-block:: python

    myLeague = 48188
    myTeamName = "wearetherunnersup"

Add credentials to http://members.fantasyfootballscout.co.uk/ config.py in your local copy of the repository.

.. code-block:: python

    login = {
        'username' : <VALUE>,
        'password' : <VALUE>
    }

Output shown below.

.. code-block:: python

    Sokratis 17.1 [('Jonny', 18.1)]
    Lacazette 18.9 []
    El Ghazi 15.7 [('Moutinho', 19.1), ('Pereyra', 18.9), ('Doucouré', 18.8), ('Kanté', 18.0), ('Westwood', 16.8), ('Almirón', 16.5), ('Xhaka', 16.2), ('Gudmundsson', 16.2), ('Neves', 16.1), ('Ndidi', 15.9)]
    King 20.4 []
    Sigurdsson 25.9 []
    Maddison 25.4 []
    Matip 15.3 [('Jonny', 18.1), ('Shaw', 17.1), ('Schär', 16.8), ('Tarkowski', 16.7), ('Vertonghen', 16.5)]
    Rose 10.9 [('Jonny', 18.1), ('Shaw', 17.1), ('Schär', 16.8), ('Tarkowski', 16.7), ('Vertonghen', 16.5), ('Mee', 15.0), ('Cathcart', 14.4), ('Fredericks', 13.9), ('Burn', 13.5), ('Steve Cook', 13.4), ('Lowton', 13.4), ('Montoya', 13.1), ('Lascelles', 13.1), ('Webster', 13.1), ('Sidibé', 13.0), ('Baldock', 12.8), ('Bertrand', 12.6), ('Bennett', 12.6), ("O'Connell", 12.5), ('Delph', 12.3), ('Egan', 12.2), ('Basham', 12.1), ('Ritchie', 12.0), ('Dawson', 11.7), ('Bednarek', 11.6), ('Aarons', 11.5), ('Engels', 11.5), ('Ogbonna', 11.4), ('Young', 11.3), ('Valery', 11.3), ('Zouma', 11.3), ('Lewis', 11.2)]
    Lamela 18.8 [('Moutinho', 19.1), ('Pereyra', 18.9)]
    Foster 21.3 []
    Hughes 12.4 [('Moutinho', 19.1), ('Pereyra', 18.9), ('Doucouré', 18.8), ('Kanté', 18.0), ('Westwood', 16.8), ('Almirón', 16.5), ('Xhaka', 16.2), ('Gudmundsson', 16.2), ('Neves', 16.1), ('Ndidi', 15.9), ('Wijnaldum', 15.4), ('Robinson', 15.4), ('McArthur', 15.1), ('Barnes', 14.7), ('Norwood', 14.7), ('Fleck', 14.6), ('Højbjerg', 14.5), ('Noble', 14.5), ('Hudson-Odoi', 14.2), ('Rice', 14.1), ('Dendoncker', 14.1), ('Stiepermann', 13.9), ('Pérez', 13.7), ('Schlupp', 13.6), ('Fabinho', 13.6), ('Trossard', 13.5), ('Pröpper', 13.4), ('Longstaff', 13.3), ('Cork', 13.2), ('Mata', 13.2), ('Capoue', 13.2), ('Cleverley', 13.0), ('Stephens', 12.8), ('Billing', 12.8)]
    Doherty 20.9 []
    Jota 20.4 []
    Adrián 8.9 [('Roberto', 19.8), ('Henderson', 19.7), ('Gazzaniga', 17.8), ('Krul', 10.6)]
    Tomori 15.4 [('Jonny', 18.1), ('Shaw', 17.1), ('Schär', 16.8), ('Tarkowski', 16.7), ('Vertonghen', 16.5)]

