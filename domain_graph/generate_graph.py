import yaml, pandas as pd

with open("seeds.yaml") as f:
    data=yaml.safe_load(f)

rows=[]

for domain,skills in data.items():
    for skill,block in skills.items():
        rows.append([domain,"HAS_SKILL",skill])

        for c in block.get("concepts",[]):
            rows.append([skill,"HAS_CONCEPT",c])

        for r in block.get("relations",[]):
            rows.append(r)

df=pd.DataFrame(rows,columns=["source","relation","target"])
df.to_csv("domain_graph.csv",index=False)
print("domain_graph.csv regenerated")
