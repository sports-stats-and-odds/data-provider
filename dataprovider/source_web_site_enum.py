from enum import Enum

SourceWebSite = Enum(
            'SourceWebSite', 
            [
                'FBREF',
                'FOOTBALLIA',
                'MATCHENDIRECT',
                'WIKIPEDIA',
                'LEQUIPE'
            ]
        )