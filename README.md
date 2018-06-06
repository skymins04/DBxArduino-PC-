# DBxArduino-PC-
DB x Arduino 그래프 뷰어 v.1.0.3

[@] UI 개선
[@] 코드 최적화
[@] 가독성 향상

# How to Use it?
```sh
pip install pil
-pil을 설치해
```
```sh
1. DBgraphVeiwer를 다운받는다
2. https://github.com/skymins04/DBxArduino-server- 에서 dynamicGraph.php, exportCSV.php, veiwList.php 를 다운받아
  자신의 서버에 (/var/www/html/DBxArduino) 풀어놓는다.
3. dynamicGraph.php 를 열어 5번째 줄에서 mysql 유저와 패스워드를 입력한다.
4. 나머지 exportCSV.php 와 veiwList.php 에도 mysql 정보를 수정한다
5. 처음에 다운받은 DBgraphVeiwer 안에 DBgraphVeiwer.lnk 를 실행한다.
6. 서버주소, DB명, 테이블명을 입력하고 원하는 옵션을 준뒤 "그래프 보기" 를 클릭한다

*주의!!: 데이블 구조는 다음 형식을 준수해주어야 합니다.   id int not null auto_increment,
        스키마는 아무렇게나 지어도 상관업지만 데이터형과  time timestamp default current_timestamp,
        기본값은 준수해주어야 합니다.                   각종 정수형 데이터들
                                                      .
                                                      .
                                                      .
```

  
제작자: BetaMan(강민수,skymin0417@gmail.com)
