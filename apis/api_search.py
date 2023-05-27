from bottle import post, request, response
import json
import x


@post("/search")
def _():
    try:
        response.set_header("Content-type", "application/json")

        data = request.json
        query = data["query"]

        db =x.db()
        tweets = db.execute(
            "SELECT * FROM tweets_fts WHERE tweets_fts MATCH ?", (query,)).fetchall()
        
        return json.dumps( [dict(i) for i in tweets] )
    except Exception as ex:
        return json.dumps([{}])
    finally:
        pass
