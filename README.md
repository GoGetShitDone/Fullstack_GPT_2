# Fullstack-GPT(ver02)

이 프로젝트는 LangChain과 기타 관련 기술을 사용하여 다양한 자연어 처리 태스크를 수행하는 Fullstack GPT 애플리케이션의 두 번째 버전입니다.

## 프로젝트 구조

```
.
├── .vscode
│   └── settings.json
├── practice
│   ├── 01_practice.ipynb
│   ├── 02_practice.ipynb
│   ├── 03_practice.ipynb
│   ├── 04_LangPoet.ipynb
│   ├── 05_practice(ModelIO).ipynb
│   ├── 06_Movie_gpt.ipynb
│   ├── 07_practie(Memory).ipynb
│   ├── 08_practice(RAG).ipynb
│   ├── 09_assignment.ipynb
│   ├── 10_RAG_LCEL.ipynb
│   └── cache.db
├── .gitignore
├── main.py
├── prompt.json
├── prompt.yaml
└── requirements.txt
```

## 주요 컴포넌트

- `practice/`: 다양한 실습과 예제를 포함하는 Jupyter 노트북 파일들이 있는 디렉토리
- `main.py`: 메인 애플리케이션 파일
- `prompt.json` 및 `prompt.yaml`: 프롬프트 템플릿 정의 파일
- `requirements.txt`: 프로젝트 의존성 목록

## 설치 방법

1. 저장소를 클론합니다:
   ```
   git clone [저장소 URL]
   ```

2. 프로젝트 디렉토리로 이동합니다:
   ```
   cd Fullstack-GPT(ver02)
   ```

3. 가상 환경을 생성하고 활성화합니다:
   ```
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

4. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

## 사용 방법

1. Jupyter 노트북 실행:
   ```
   jupyter notebook
   ```
   그런 다음 `practice` 폴더 내의 노트북 파일들을 열어 실습을 진행할 수 있습니다.

2. 메인 애플리케이션 실행:
   ```
   python main.py
   ```

## 주요 기능

- LangPoet: AI를 이용한 시 생성 (04_LangPoet.ipynb)
- Movie GPT: 영화 추천 시스템 (06_Movie_gpt.ipynb)
- RAG (Retrieval-Augmented Generation) 시스템 구현 (08_practice(RAG).ipynb, 10_RAG_LCEL.ipynb)

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5. Pull Request를 생성합니다.

## 라이선스

이 프로젝트는 [MIT] 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
