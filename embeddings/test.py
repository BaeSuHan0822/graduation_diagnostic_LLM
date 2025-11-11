import os
# from Kanana import Custom_Kanana

# model = Custom_Kanana()

file_path = "../curriculum_db/"
output_path = "../chroma_db"
if os.path.exists(output_path) :
    print("이미 존재합니다.")
else :
    os.makedirs(output_path)
files = os.listdir(file_path)
print(files)