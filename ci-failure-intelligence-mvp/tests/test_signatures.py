from app.analyzer import detect_signatures

def test_oom():
 assert detect_signatures("OOMKilled")[0]["category"]=="OOM"
