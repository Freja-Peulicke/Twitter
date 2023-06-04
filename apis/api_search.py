from bottle import post, request, response
import json
import x


@post("/api-search")
def _():
    try:
        response.set_header("Content-type", "application/json")

        data = request.json
        query = data["query"]

        db =x.db()
        cur = db.cursor()
        tweets = cur.execute(
            "SELECT * FROM tweets_fts WHERE tweets_fts MATCH ?", (query,)).fetchall()
        
        return json.dumps( [dict(i) for i in tweets] )
    except Exception as ex:
        if 'db' in locals(): db.rollback()
        return json.dumps([{}])
    finally:
        pass
