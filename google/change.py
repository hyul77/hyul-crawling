import os
import re
import pandas as pd
from shutil import copyfile

# 이미지가 저장된 폴더 경로
img_folder_path = 'img/'
new_img_folder_path = 'data/'

# DataFrame을 저장할 빈 리스트 생성
data = []

# img 폴더 내의 파일 목록 가져오기
files = os.listdir(img_folder_path)
number1 = 0
# 파일 이름을 순회하며 데이터 추출
for file_name in files:
    file_name = file_name.strip()
    if file_name.endswith('.jpg'):  # jpg 파일만 고려
        # 파일 이름에서 음식명, 순번 추출
        match = re.match(r'([a-zA-Z가-힣\s_]+?)(\(\w*\))?(\d*)\.jpg', file_name)
        if match:
            food_name = match.group(1)
            number = int(match.group(3)) if match.group(3) else 0
            
            # 새로운 파일명 생성 (image숫자.jpg)
            new_file_name = f'image{number1}.jpg'
            
            # 새로운 경로에 파일 복사
            copyfile(os.path.join(img_folder_path, file_name), os.path.join(new_img_folder_path, new_file_name))
            
            # 데이터 리스트에 추가
            data.append({'Food_name': food_name, 'number': int(number), 'img_file_name': new_file_name})
            number1 += 1
        
        else:
            print(f'파일 형식이 일치하지 않아 데이터프레임에 추가하지 않습니다: {file_name}')

# 리스트를 DataFrame으로 변환
df = pd.DataFrame(data)

# Food_name별로 등장 횟수를 세어 'count' 열 추가
df['count'] = df.groupby('Food_name')['Food_name'].transform('count')

# DataFrame을 원하는 형식으로 정렬 (Food_name과 number 순으로)
df = df.sort_values(by=['Food_name', 'number'])

# 결과를 CSV 파일로 저장
df.to_csv('image_data.csv', index=False, encoding='utf-8')

print("image_data가 정상적으로 저장되었습니다.")
