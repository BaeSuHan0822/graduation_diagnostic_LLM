import torch
from Kanana import Custom_Kanana  # ✅ 클래스 import

if __name__ == "__main__":
    # 1️⃣ 모델 로드
    model = Custom_Kanana(
        instruction="질문이 주어졌을 때 학과 졸업 요건을 찾아라",
        device="cpu",
        normalize=True
    )

    # 2️⃣ 테스트용 문서
    docs = [
        "컴퓨터공학과 졸업 요건은 전공필수 48학점 이상 이수이다.",
        "졸업을 위해 영어 인증시험을 통과해야 한다.",
        "졸업논문 또는 캡스톤디자인 과목을 이수해야 한다.",
    ]

    # 3️⃣ 문서 임베딩
    print("📘 문서 임베딩 중...")
    doc_embeddings = model.embed_documents(docs)
    print(f"문서 벡터 개수: {len(doc_embeddings)}")
    print(f"한 벡터 길이: {len(doc_embeddings[0])}")

    # 4️⃣ 질의문 임베딩
    query = "컴퓨터공학과 졸업 조건이 뭐야?"
    print("\n💬 질의 임베딩 중...")
    query_embedding = model.embed_query(query)
    print(f"질의 벡터 길이: {len(query_embedding)}")

    # 5️⃣ 질의-문서 유사도 계산
    print("\n📈 유사도 계산 결과:")
    query_tensor = torch.tensor(query_embedding).unsqueeze(0)
    doc_tensor = torch.tensor(doc_embeddings)
    scores = (query_tensor @ doc_tensor.T) * 100

    for i, score in enumerate(scores[0]):
        print(f"문서 {i+1} ({docs[i][:20]}...): {score.item():.2f}")

    best_idx = torch.argmax(scores)
    print(f"\n✅ 가장 관련 있는 문서: {docs[best_idx]}")
