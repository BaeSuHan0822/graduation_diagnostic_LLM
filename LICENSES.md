# 📜 Open Source Licenses

이 프로젝트는 다음 오픈소스 소프트웨어, 프레임워크, 및 AI 모델을 사용하고 있습니다.  
모든 구성요소는 각자의 라이선스 조건에 따라 합법적으로 사용되었습니다.

---

## 🧩 라이브러리 및 툴 요약

| Component | Version | License Type | Notes |
|------------|----------|---------------|--------|
| **fastapi** | 0.120.4 | MIT | Lightweight Python web framework |
| **pdfminer.six** | 20250506 | MIT | PDF text extraction backend |
| **pdfplumber** | 0.11.7 | MIT | High-level PDF parsing library |
| **pypdfium2** | 5.0.0 | BSD-3-Clause / Apache-2.0 | PDF rendering engine (Google PDFium bindings) |
| **langchain** | 1.0.3 | MIT | Core framework for LLM applications |
| **langchain-classic** | 1.0.0 | MIT | Legacy compatibility module |
| **langchain-community** | 0.4.1 | MIT | Community extensions and integrations |
| **langchain-core** | 1.0.2 | MIT | Core building blocks for LangChain |
| **langchain-huggingface** | 1.0.0 | MIT | Hugging Face integration for embeddings |
| **langchain-ollama** | 1.0.0 | MIT | Ollama local model interface |
| **langchain-text-splitters** | 1.0.0 | MIT | Text chunking utilities for LLM pipelines |
| **chromadb** | 1.3.0 | Apache License 2.0 | Vector database for embeddings |
| **sentence-transformers** | 5.1.2 | Apache License 2.0 | Sentence embeddings via Transformers |
| **transformers** | 4.57.1 | Apache License 2.0 | Hugging Face Transformers library |
| **datasets** | 4.4.1 | Apache License 2.0 | Dataset loading & preprocessing library |
| **Docker** | 27.x | Apache License 2.0 | Container engine for application orchestration |
| **Poetry** | 1.8.x | MIT | Dependency and virtual environment manager |
| **kakaocorp/kanana-nano-2.1b-embedding** | — | Apache License 2.0 | Korean embedding model by KakaoBrain on Hugging Face Hub |
| **pip-licenses** | 5.5.0 | MIT | Generate dependency license reports |

---

## 🤖 사용된 AI 모델

이 프로젝트는 **KakaoBrain**이 공개한 한국어 임베딩 모델을 사용합니다.

### 🔹 Model Information
- **Model Name:** `kakaocorp/kanana-nano-2.1b-embedding`  
- **Publisher:** [KakaoBrain](https://huggingface.co/kakaocorp)  
- **Platform:** [Hugging Face Hub](https://huggingface.co/kakaocorp/kanana-nano-2.1b-embedding)  
- **License:** Apache License 2.0  
- **Description:**  
  경량 한국어 문장 임베딩 모델로, `SentenceTransformer` 기반의 다국어 임베딩 구조를 지원합니다.  
  본 프로젝트에서는 문서 임베딩 및 질의 유사도 계산을 위해 사용되었습니다.

> © KakaoBrain Corp. Licensed under the Apache License 2.0.

---

## 📈 License Distribution Summary

| License Type | Components |
|---------------|-------------|
| **MIT License** | fastapi, pdfminer.six, pdfplumber, langchain, langchain-classic, langchain-community, langchain-core, langchain-huggingface, langchain-ollama, langchain-text-splitters, Poetry, pip-licenses |
| **Apache License 2.0** | chromadb, sentence-transformers, transformers, datasets, Docker, pypdfium2 (partial), kakaocorp/kanana-nano-2.1b-embedding |
| **BSD-3-Clause** | pypdfium2 (dual licensed) |

---

## 📚 참고

- 본 라이선스 목록은 `pip-licenses` 명령어를 통해  
  `poetry` 가상환경(`micro-service-programming-py3.11`)에서 자동으로 수집되었습니다.
- 명령어 예시:
  ```bash
  pip-licenses --from=poetry --format=markdown > LICENSES.md
  ```
- Docker 및 Poetry, 그리고 Hugging Face 모델은 pip 기반 패키지가 아니므로 수동으로 포함되었습니다.
- 최신 상태 유지를 위해, 라이브러리 또는 모델 업데이트 시 해당 문서를 갱신하시기 바랍니다.

---

# 📘 License Texts

## MIT License
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
```

---

## Apache License 2.0
```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
See the License for the specific language governing permissions and 
limitations under the License.
```

---

## BSD 3-Clause License
```
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright 
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in 
   the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its 
   contributors may be used to endorse or promote products derived 
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY 
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

© 2025 **micro_service_programming Project**  
All rights reserved.
