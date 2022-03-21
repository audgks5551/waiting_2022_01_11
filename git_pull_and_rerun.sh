#!/bin/bash

# git_pull_and_rerun.sh 파일내용

# 테스트 환경에서 테스트 먼저
{
  docker start python__2__test
  docker exec python__2__test bash -ce "cd /data/site_projects/python__2__test/src ; git pull origin master"
  docker exec python__2__test bash -ce "cd /data/site_projects/python__2__test/src ; pip install -r requirements/prod.txt"
  docker exec python__2__test bash -ce "cd /data/site_projects/python__2__test/src ; python manage.py test -v 2 --settings=config.settings.prod 2>&1"
} || {
  docker stop python__2__test
  exit 1
}

# 테스트장고 종료
docker stop python__2__test

# 기존장고 종료
docker exec python__2 pkill "gunicorn"

# 폴더에 깃에 있는 최신소스코드 가져오기
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; git pull origin master"

# 의존성 설치
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; pip install -r requirements/prod.txt"

# 마이그레이트
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py migrate --settings=config.settings.prod"

# 샘플 데이터 추가
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py createsu --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_users --number 10 --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_amenities --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_foodTypes --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_menus --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_storeTypes --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_tastes --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_themes --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_stores 'example_csv.csv' --settings=config.settings.prod"
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; python manage.py seed_waiting --settings=config.settings.prod"

# 장고를 운영모드로 실행
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; nohup gunicorn --bind=0.0.0.0:8000 config.wsgi &"

# static collect 다시 수행
docker exec python__2 bash -ce "cd /data/site_projects/python__2/src ; echo yes | python manage.py collectstatic --settings=config.settings.prod"

exit 0

## 테스트1
## 테스트2
## 테스트3
## 테스트4
## 테스트5
## 테스트6 - 샘플데이터추가
## 테스트7 - db날리고 재시작
## 테스트8 - db날리고 재시작