from app.signatures import SIGNATURES

def detect_signatures(log_text):
 r=[]

 for c,pats in SIGNATURES.items():
  for p in pats:
   if p.lower() in log_text.lower(): r.append({"category":c,"evidence":p})
 return r
