## 🚢 sentence-transformers를 활용한 HSCODE 자동 추천
* HSCODE는 수출 물품의 품목 분류 코드
* 기업은 통관절차를 밟기 위해 관세사에 화물의 HSCODE를 전달 해야함.
* 하지만 11,000개가 넘는 HSCODE표를 일일이 확인하는 작업은 시간적 비용이 매우 큼
* sentence-transformers, cosine simirality를 활용해 HSCODE 자동 추천 시스템을 개발

## 추천 시스템 알고리즘
![algorithm](image/algorithm.png)

* HSCODE-품명쌍 데이터 수집후, sentence-transformers 모델을 통해 embedding 벡터 추출.
* 최종적으로 HSCODE-품명-embedding 파일 생성 후 User-input이 들어올 경우 embedding 파일내의 embedding vector와 Cosine-simirality 계산 후 추천
## HSCODE 데이터 수집 및 임베딩 추출

```bash
python3 craw_data.py
```
selenium 라이브러리를 활용 관세법령정보포털에서 약 51,000개의 HSCODE-품명 쌍 데이터 수집

```bash
python3 embedding.py
```
[sentence-transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)를 활용해 품목명 임베딩 벡터 추출 및 임베딩 파일 생성

## 추천 예시
```bash
python3 recommend.py
```
![recommend](image/recommend.png)

## Reference
```
@article{
  title={단어 임베딩을 활용한 빅데이터 기반의 지능형 HS코드 식별},
  author={Hyo-Chang Woo,Young-Koo Lee}
  journal={한국정보과학회 학술발표논문집}
  year = {2019} 
}
@article{
  title={언어모델 전이학습 기반 해외 직접 구매 상품군 분류},
  author={Kyo-Joong Oh,Ho-Jin Choi,Wonseok Cha,Ilgu Kim,Chankyun Woo}
  journal={한글 및 한국어 정보처리 학술대회 논문집}
  year = {2022} 
}
```
* [HS 오토팬](https://www.hs-tariff.com/main/hs_mti_ai_main/?device=pc)
* [Cello Square(첼로 스퀘어)](https://www.cello-square.com/kr-ko/index.do)
* https://huggingface.co/nreimers/MiniLM-L6-H384-uncased
* https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
* [관세법령정보포털](https://unipass.customs.go.kr/clip/index.do)
