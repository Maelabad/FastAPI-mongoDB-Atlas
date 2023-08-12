

def movieEntity(item) -> dict:
    return {
        "_id": str(item['_id']),
        "Rank": int(item['Rank']),
        "Movie Title": str(item['Movie Title']),
        "Year": int(item['Year']),
        "Score": int(item['Score']),
        "Director": str(item['Director']),
        "Cast": str(item['Cast']),
        "critics": str(item['Critics Consensus'])
    }


def moviesEntity(entity) -> list:
    return [movieEntity(item) for item in entity]
#Best way













def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]


