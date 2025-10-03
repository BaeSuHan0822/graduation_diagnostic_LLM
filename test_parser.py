import re
import pandas as pd

with open("data/noname.txt", encoding="cp949") as f:
    lines = f.readlines()

courses = []
for line in lines:
    # 학수번호(영문+숫자), 과목명(한글/영문), 학점(숫자), 학기(YYYY / N) 잡기
    match = re.search(r"([A-Z]{2,}\d{3,})\s+([가-힣a-zA-Z0-9+/().:#]+)\s+(\d+)\s+(\d{4}\s*/\s*\d+)", line)
    if match:
        code, name, credit, semester = match.groups()
        courses.append({
            "code": code.strip(),
            "name": name.strip(),
            "credit": int(credit),   # 숫자로 변환
            "semester": semester.strip()
        })

df = pd.DataFrame(courses)
df.to_csv("noname.csv")
print(df.head(50))
