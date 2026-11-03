import json,pathlib
from app.analyzer import detect_signatures

def run(path="sample_logs/oom.log"):
 txt=pathlib.Path(path).read_text()
 rep={"findings":detect_signatures(txt)}
 pathlib.Path("reports").mkdir(exist_ok=True)
 open("reports/report.json","w").write(json.dumps(rep,indent=2))
 print(json.dumps(rep,indent=2))

if __name__=="__main__":
 run()
