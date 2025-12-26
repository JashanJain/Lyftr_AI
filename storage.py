from app.models import get_conn
from datetime import datetime

def insert_message(msg):
    conn=get_conn(); cur=conn.cursor()
    try:
        cur.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",(
            msg["message_id"],msg["from"],msg["to"],msg["ts"],msg.get("text"),datetime.utcnow().isoformat()
        )); conn.commit()
    except: pass
    finally: conn.close()

def list_messages(limit, offset):
    conn=get_conn(); cur=conn.cursor()
    rows=cur.execute("SELECT message_id,from_msisdn,to_msisdn,ts,text FROM messages ORDER BY ts,message_id LIMIT ? OFFSET ?",(limit,offset)).fetchall()
    total=cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    conn.close()
    return {"data":[{"message_id":r[0],"from":r[1],"to":r[2],"ts":r[3],"text":r[4]} for r in rows],"total":total,"limit":limit,"offset":offset}

def get_stats():
    conn=get_conn(); cur=conn.cursor()
    total=cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    first=cur.execute("SELECT MIN(ts) FROM messages").fetchone()[0]
    last=cur.execute("SELECT MAX(ts) FROM messages").fetchone()[0]
    conn.close()
    return {"total_messages":total,"first_message_ts":first,"last_message_ts":last}
