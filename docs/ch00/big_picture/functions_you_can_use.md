# 🛠 사용 가능한 4가지 함수 — User Manual

본 프로젝트는 **4개의 명령어**로 모든 일상 작업을 처리한다. 기존 페이지의 품질 진단/개선과, 외부 PDF로부터 신규 페이지 생성이 분리되어 있어 한 명령이 한 가지 일만 한다.

| 명령어 | 무엇을 하나 | 언제 쓰나 |
|---|---|---|
| **`review <file\|folder\|all>`** | `_vN.md` 스냅샷을 동결하고 두 reviewer (수학·글쓰기) 로 점검 → stdout 보고 | 쓰기 전에 페이지 품질을 진단하고 싶을 때 |
| **`write <file\|folder\|all>`** *(옵션 `if score < N`)* | 직전 review 의 피드백을 반영해 `<n>.md` 를 새로 쓰고 점수 갱신 | review 결과를 보고 페이지를 개선할 때 |
| **`update <file\|folder\|all>`** *(옵션 `if score < N`)* | `review` + `write` 를 한 명령으로 실행 | 평상시 페이지 정기 갱신 |
| **`fetch-pdf <pdf-path> [<target>]`** | 한국어 수학 PDF에서 문제를 추출해 새 절(들) 의 `.md` + figures `.py` + PNG 일괄 생성, `mkdocs.yml` nav 자동 등록 | 시험지·교재 PDF에서 새 교재 페이지를 만들 때 |

네 함수는 **두 갈래의 작업 흐름**으로 분리되어 있다.

```
[기존 페이지] ──→ review ──→ [_vN.md 동결 + reviewer report]
                  ↓
                write  ──→ [_score.md 점수 갱신 + <n>.md 개선판]
                  ↑
                update = review + write 통합

[외부 PDF] ──→ fetch-pdf ──→ [신규 <name>.md + figures/<name>_figures.py + *.png]
                              + mkdocs.yml nav 자동 등록
                              + mkdocs build --strict 자동 검증
```

> Reviewer agents (`MATH_REVIEWER`, `WRITING_REVIEWER`) 와 작성 agent (`WRITER`) 의 내부 prompt 는 사용자가 직접 호출하지 않는다. 본 매뉴얼은 **사용자 명령어** 만 다룬다.

---

## 1. `review` — 페이지 품질 진단 (쓰기 없음)

### 1.1 기본 사용

```
review ch01/integration_by_parts/integration_by_parts.md     # 단일 파일
review ch01/integration_by_parts                              # 폴더 (재귀)
review ch01                                                    # 챕터 전체
review all                                                     # docs/ 전체
```

- **무엇을 하나**:
    1. 기존 `_vN.md` 개수 확인 → 다음 버전 $N$ = (개수 + 1)
    2. `<n>.md` 를 `<n>_vN.md` 로 **복사** (이동 X — 원본은 그대로)
    3. `MATH_REVIEWER` 실행 → 수학 정확성 점검 보고 (in memory)
    4. `WRITING_REVIEWER` 실행 → 글쓰기 점검 보고 (in memory)
    5. 두 보고를 stdout 으로 출력 — **파일에 쓰지 않음**
- **하지 않는 것**: `<n>.md` 수정 X · `_score.md` 갱신 X · `mkdocs.yml` 변경 X
- **소요 시간**: 파일당 ~1–2분 (LLM 두 번 호출)
- **경로 형식**: `docs/` 접두사 생략 가능 · `.md` 확장자 생략 가능 · 디렉토리 지정 시 재귀 처리

### 1.2 결과 (디스크에 남는 것)

- **`<n>_vN.md`** : 동결된 vN 스냅샷 (`.gitignore` 처리되어 커밋되지 않음)
- **stdout 의 두 보고** : 🔴 Critical / 🟡 Major / 🟢 Minor 분류된 issue 목록

### 1.3 언제 쓰나

- 페이지를 수정하기 전 현재 상태의 약점 파악
- 분기 자기 검토 (`review all`) — 어느 페이지가 점수가 낮은지 일괄 확인
- `write` 전 단계 (수동 분리하고 싶을 때)
- 외부 PR 리뷰 보조

---

## 2. `write` — 리뷰 결과를 반영해 페이지 개선

### 2.1 기본 사용

```
write ch01/integration_by_parts/integration_by_parts.md
write ch01/integration_by_parts
write ch01
write all
```

- **사전 조건**: `<n>_vN.md` 가 존재해야 함 (즉 이 파일에 대해 `review` 가 먼저 실행됐어야 함)
- **무엇을 하나**:
    1. `WRITER` 가 `<n>_vN.md` + 두 reviewer 보고 (in-memory 재실행) 를 읽음
    2. **🔴 → 🟡 → 🟢** 순으로 수정 적용 (math 우선)
    3. `<n>.md` 를 새 버전으로 **덮어쓰기**
    4. `<n>_score.md` 에 새 버전 열을 추가 (Math/Writing 점수)
    5. (관행) 커밋 메시지 `write: <n>` 으로 stage

### 2.2 조건부 — `write … if score < N`

```
write ch01 if score < 9.0
write all if score < 8.5
```

- 파일별로 분기:
    1. **`_score.md` 없음** → 먼저 `review` 자동 실행, 임계값 적용 후 트리거 시 write
    2. **`_score.md` 존재** → 최우측(가장 최신) Math/Writing 점수 중 하나라도 $N$ 미만이면 write, 둘 다 $\geq N$ 이면 skip + stdout 로그
    3. **점수 stale** (사용자가 stale 로 판단) → `review` 를 in-memory 로 재실행 후 임계값 적용
- **배치**: batch size = 1 (한 파일씩) · 실제로 write 된 파일마다 커밋

### 2.3 산출물

| 파일 | 처리 |
|---|---|
| **`<n>.md`** | ✅ 덮어쓰기 (새 버전) |
| **`<n>_score.md`** | ✅ 새 vN 열 append |
| **`<n>_vN.md`** | (변경 없음 — `review` 가 만든 스냅샷 유지) |

### 2.4 언제 쓰나

- `review` 보고를 읽고 수정 방향이 마음에 들 때
- 임계값 기반 일괄 개선 (`write all if score < 9`)
- 수동으로 page 별 개선을 분리해서 통제하고 싶을 때

---

## 3. `update` — `review` + `write` 일괄 처리

### 3.1 기본 사용

```
update ch01/integration_by_parts/integration_by_parts.md
update ch01/integration_by_parts
update ch01
update all
```

- **무엇을 하나**:
    1. `_vN.md` 카운트 → 다음 $N$
    2. `<n>.md` → `<n>_vN.md` 복사 (동결)
    3. MATH/WRITING reviewer 실행 → 보고 stdout 출력 (파일에 쓰지 않음)
    4. `WRITER` 가 보고 + `<n>_vN.md` 를 입력으로 `<n>.md` 덮어쓰기
    5. `<n>_score.md` 에 vN 점수 append
    6. 커밋: `update: <n> → v(N)`
- 즉 사용자가 stdout 의 보고를 읽지 않고도 자동으로 다음 단계까지 흘러간다.

### 3.2 조건부 — `update … if score < N`

```
update ch01 if score < 9.0
update all if score < 8.5
```

- 파일별로 분기:
    1. **`_score.md` 없음** → `review` 실행 (stdout 만), 임계값 적용 후 트리거 시 full update
    2. **`_score.md` 존재** → 최신 점수 확인 후 임계값 미달 시 full update, 충족 시 skip
- 가장 자주 쓰는 형태. **분기 정기 점검** 에 적합.

### 3.3 일상 흐름

```
update ch01/absolute_value_integral if score < 9.0
update all if score < 9.0
```

- 첫 호출에서는 `_score.md` 가 없으므로 review 부터 수행 → write 진행
- 다음 호출부터는 `_score.md` 의 최신 점수 기준으로 자동 skip / write 분기

> **`update` vs `write`**: `write` 는 사용자가 review 를 먼저 명시적으로 실행했다는 것을 가정한다. `update` 는 review 를 내부적으로 실행하므로 사전 조건이 없다.

---

## 4. `fetch-pdf` — PDF 에서 신규 절(들) 일괄 생성

### 4.1 기본 사용

```
fetch-pdf /Users/me/Downloads/exam.pdf ch04/limits/limits.md
fetch-pdf /Users/me/Downloads/exam.pdf
fetch-pdf /Users/me/Downloads/exam.pdf ch01/integration_by_parts/integration_by_parts.md
```

- **무엇을 하나**:
    1. PDF 의 페이지를 읽어 한국어 수학 문제·풀이·도형을 추출 (행정·인문 페이지는 skip)
    2. 문제별로 어느 챕터·절에 들어갈지 매핑 → 사용자에게 layout 제안
    3. 절 (target) 별로:
        - `docs/<chapter>/<section>/figures/` 디렉토리 생성
        - `<section>_figures.py` 작성 → 실행 → 6–8 개 PNG 생성
        - `<section>.md` 작성 (한국어 본문, ~250–320 줄)
        - `mkdocs.yml` nav 항목 자동 등록
        - `mkdocs build --strict` 로 검증
    4. 2개 이상의 신규 파일/챕터 생성이 예상되면 **먼저 사용자에게 확인** 후 진행
- **하지 않는 것**: `_score.md` / `_vN.md` 생성 X (그건 review-write 루프의 영역) · 기존 `index.md` 수정 X (legacy stub 보존)
- **소요 시간**: 절당 ~3–5분 (figures 스크립트 작성·실행 + MD 작성 + 빌드)

### 4.2 입력 분기 (3가지 모드)

| 호출 형태 | 동작 |
|---|---|
| `fetch-pdf <pdf> <target.md>` *(target 존재)* | target 을 **benchmark** 로 삼아 (i) 동일 파일에 새 연습문제를 extend 하거나, (ii) 같은 챕터 내 sibling 절들로 새 파일을 만든다. 2개 이상 생성 예상 시 사용자 확인. |
| `fetch-pdf <pdf> <target.md>` *(target 없음)* | 새 파일을 그 경로에 생성. 스타일은 프로젝트 benchmark (`ch01/integration_by_parts/integration_by_parts.md`) 를 따른다. |
| `fetch-pdf <pdf>` *(target 생략)* | PDF 를 읽고 chapter/section 분할안을 제안 → 사용자 확인 후 진행. 신규 챕터 (`ch04/`, `ch05/` 등) 가 필요하면 함께 제안. |

### 4.3 산출물 (절당)

```
docs/<chapter>/<section>/
├── <section>.md                          ← 한국어 본문 (250–320 줄)
└── figures/
    ├── <section>_figures.py              ← matplotlib 스크립트
    ├── example1_*.png                    ← 6–8 개 PNG
    ├── example2_*.png
    ├── exercise1_*.png
    └── ...
```

추가로:

- `mkdocs.yml` 의 nav 에 `<section>` 항목 자동 등록 (필요 시 새 챕터 블록 생성)
- `mkdocs build --strict` 통과 확인

### 4.4 스타일 표준 — benchmark 파일

**`docs/ch01/integration_by_parts/integration_by_parts.md`** 가 모든 새 절의 스타일 기준이다. 구조 (순서 고정):

1. `# <한국어 주제명>` (heading 에 LaTeX 금지 — TOC anchor 가 깨짐)
2. 동기 부여 단락 (2–4 문장, 구체에서 추상으로)
3. `!!! note "사용 도구"` — 사용할 공식/도구를 미리 정리
4. `## 보기 N: <부제목>` 블록들 — 각각:
    - 설정 단락 + 동기
    - 최소 1개의 figure (`<figure markdown>` + `<figcaption>`)
    - `??? success "보기 N 풀이"` 접힌 풀이
    - `!!! info "핵심 아이디어"` 마무리
5. `---`
6. `## 연습문제` 헤딩
7. `**연습문제 N.**` 각각 바로 아래 `??? success "연습문제 N 풀이"` 로 풀이 첨부 · `---` 로 구분
8. 마지막 연습문제의 풀이는 `!!! tip "큰 그림"` 으로 마무리

> **한국어 + 인라인 수식 공백 규칙**: 닫는 `$` 다음에 한글이 오면 공백 한 칸. 예: `$ab = 1$ 일 때` (O), `$ab = 1$일 때` (X). 다음 문자가 영문/기호/구두점/공백/다른 수식이면 공백 불필요.

### 4.5 figures 자동 생성 규칙

- **한 절당 한 개의 Python 스크립트**: `figures/<section>_figures.py`
- **6–8개 PNG**. 사용자 지침: "그림은 많을수록 좋다"
- **스크립트 형식**:
    - module docstring 에 PNG 목록 + 1줄 설명
    - `# ===` 로 함수 사이 구분
    - 각 함수 시그니처: `def make_X(out_path: Path) -> None:`
    - `plt.savefig(out_path, dpi=120, bbox_inches="tight")` + `plt.close(fig)`
    - 말미에 `if __name__ == "__main__":` 가드, 모든 함수 호출 후 `print(f"Wrote figures to {out_dir}")`
- **plot 안의 텍스트**: **English / LaTeX 만**. matplotlib 의 기본 폰트는 한글을 깔끔히 렌더하지 못한다. 한국어 설명은 MD 의 `<figcaption>` 에만 둔다.

### 4.6 matplotlib mathtext 의 LaTeX 제약 (gotchas)

MathJax (MD 본문) 에서는 동작하지만 matplotlib 의 `mathtext` 가 **지원하지 않는** LaTeX 명령어 — 발견 시 즉시 치환:

| 동작 안 함 | 대체 |
|---|---|
| `\dfrac`, `\tfrac` | `\frac` |
| `\displaystyle` | 제거하거나 식 재구성 |
| `\!` (negative thin space) | 제거 |
| `\boldsymbol` | `\mathbf` |
| `\square` (QED) | `\Box` 또는 plot 안에서는 생략 |
| `\bigl`, `\bigr` | 일반 `(`, `)` |

`python <section>_figures.py` 실행 시 `Unknown symbol: \X` 에러가 나면 그 명령어를 위 표대로 치환. 다른 렌더링 백엔드로 바꾸지 말 것.

### 4.7 무엇을 하지 않는가

- **`index.md` 수정 안 함** — 기존 챕터 overview 는 이전 프로젝트 구조의 잔재일 수 있다 (예: ch01/index.md 가 "Python Basics" 시절 내용). 명시적 요청 없이는 손대지 않는다.
- **커밋 안 함** — 사용자가 결과를 확인한 후 직접 커밋한다.
- **`mkdocs build --strict` 생략 안 함** — strict 모드만 깨진 링크·누락 nav 를 잡아준다.
- **문제 창작 안 함** — 모든 `보기` 와 `연습문제` 는 PDF 의 원 문제·풀이로 트레이스 가능해야 한다. 단, intro 의 `!!! note "사용 도구"` 와 첫 warm-up `보기` 는 scaffolding 을 위해 추가할 수 있다.
- **figure 안에 한글 안 씀** — 배포된 사이트에서 박스로 렌더된다.

### 4.8 언제 쓰나

- 대학별고사·수능 기출 PDF 가 손에 들어왔을 때
- 교과서 한 단원의 문제·풀이를 발췌해 옮기고 싶을 때
- 기존 절을 benchmark 로 삼아 sibling 절들을 일괄 생성하고 싶을 때
- 새 챕터 (ch04, ch05 …) 의 초고를 빠르게 만들고 싶을 때

> `fetch-pdf` 가 생성한 절은 review-write 루프에 자연스럽게 합류한다. 사용자가 나중에 `review <new-section>` 또는 `update <new-section>` 을 호출하면 v1 스냅샷이 만들어지고 점수 추적이 시작된다.

---

## 5. 파일 관리 규칙

| 파일 패턴 | Git | GitHub Pages |
|---|---|---|
| `<n>.md` | ✅ committed | ✅ published |
| `<n>_score.md` | ✅ committed | ❌ excluded via `mkdocs.yml` |
| `<n>_v[0-9]*.md` | ❌ gitignored | ❌ excluded via `mkdocs.yml` |
| `figures/<n>_figures.py` | ✅ committed | (스크립트 — published 안 됨) |
| `figures/*.png` | ✅ committed | ✅ published (그림으로 표시) |

`.gitignore` 핵심 라인:

```
docs/**/*_v[0-9]*.md
```

`mkdocs.yml` 의 `exclude_docs`:

```yaml
exclude_docs: |
  *_score.md
  *_v[0-9]*.md
```

`update` · `write` 후 commit 시 stage 대상은 `<n>.md` 와 `<n>_score.md` 두 개만:

```bash
git add docs/path/to/<n>.md docs/path/to/<n>_score.md
git commit -m "update: <n>"
```

`_vN.md` 가 실수로 stage 되지 않도록 주의.

---

## 6. 점수 파일 형식

`<n>_score.md` 는 단일 growing table — 매 `write`/`update` 마다 새 vN 열이 추가된다.

```
┌───────────────┬──────────┬──────────┬──────────┐
│               │    v1    │    v2    │    v3    │
├───────────────┼──────────┼──────────┼──────────┤
│ Math score    │ 8.5 / 10 │ 9.5 / 10 │ 9.7 / 10 │
├───────────────┼──────────┼──────────┼──────────┤
│ Writing score │ 7.5 / 10 │ 9.0 / 10 │ 9.3 / 10 │
└───────────────┴──────────┴──────────┴──────────┘
```

- `v1` = 첫 `review` 패스의 원본 점수
- 각 `vN` = WRITER 가 vN 의 수정 적용 후 추정한 점수
- 빈 셀 = 그 버전은 아직 작성되지 않음

테이블 아래에는 매 update 마다 한 블록이 append:

```
vN → v(N+1)  YYYY-MM-DD
Math fixes: N (🔴 X, 🟡 Y, 🟢 Z)
Writing fixes: N (🔴 X, 🟡 Y, 🟢 Z)
Skipped: <의도적으로 skip 한 minor 이슈와 그 이유>
```

이 형식은 `agents/WRITER.md` 의 명세를 따른다 (repo 루트의 파일).

---

## 7. 일상 워크플로우 모범 예시

### 7.1 새 PDF 한 권을 흡수

```
fetch-pdf /Users/me/Downloads/2026_exam.pdf
# → Claude 가 PDF 를 읽고 layout 제안 (예: "ch04/limits 와 ch05/series 두 신규 챕터")
# → 사용자 승인
# → 절별로 figures + MD + nav 자동 생성, 마다 mkdocs build --strict 통과 확인
```

### 7.2 단일 절 추가 (target 지정)

```
fetch-pdf /Users/me/Downloads/2026_exam.pdf ch04/limits_of_sequences/limits_of_sequences.md
# → 그 PDF 의 관련 문제만 추출해서 새 절 1개 생성
```

### 7.3 기존 절에 PDF 의 새 문제 추가

```
fetch-pdf /Users/me/Downloads/2027_exam.pdf ch01/integration_by_parts/integration_by_parts.md
# → benchmark 인 이 파일에 새 연습문제 append 또는 sibling 절 제안
```

### 7.4 분기 자기 점검

```
update all if score < 9.0
# → 모든 페이지 review → 점수 9 미만인 것만 write → 커밋
```

소요: 페이지당 ~3–5분, 전체 사이트 ~수 시간 (다중 세션).

### 7.5 특정 페이지를 깊게 재작성

```
update ch01/functional_equation_tangent/functional_equation_tangent.md
# → review (stdout) + write 일괄 수행, 새 vN 스냅샷 자동
```

### 7.6 한 절의 리뷰만 따로 보고 싶을 때

```
review ch01/integration_by_substitution/integration_by_substitution.md
# → 두 reviewer 의 보고를 stdout 으로만 출력, 파일 변경 X
# → 보고를 읽고 마음에 들면:
write ch01/integration_by_substitution/integration_by_substitution.md
```

### 7.7 신규 챕터 통째로 추가 (수동)

`fetch-pdf` 가 자동으로 처리하지만, 수동으로 만들 때:

1. `docs/ch04/<topic>/<topic>.md` + `figures/` 디렉토리 생성
2. `mkdocs.yml` 에 새 챕터 블록 + 새 절 추가
3. (선택) `update ch04/<topic>/<topic>.md` 로 점수 추적 시작

> 자세한 신규 챕터 생성 절차는 repo 루트의 `CLAUDE.md` §"Add a new chapter" 참조.

---

## 8. 함수 사이의 의존 관계

```
[PDF 파일] ──→ fetch-pdf ──→ [docs/<ch>/<section>/<section>.md]
                              [docs/<ch>/<section>/figures/*.png]
                              [mkdocs.yml nav 항목]
                              + mkdocs build --strict 통과 확인
                                  │
                                  ▼
                            (이후 정기 점검은 review-write 루프로)


[기존 <n>.md] ──→ review ──→ [<n>_vN.md 동결, reviewer 보고 stdout]
                  │
                  ▼
                write ──→ [<n>.md 덮어쓰기 + <n>_score.md 점수 append]
                  ↑
                update = review + write 통합 (사용자 권장 형태)
```

**핵심 원칙**: `fetch-pdf` 는 **생성**, `update` 는 **개선**, `review` 와 `write` 는 두 단계를 명시적으로 분리하고 싶을 때 사용한다. `_vN.md` 와 `_score.md` 는 review-write 루프의 산물이며, `fetch-pdf` 가 직접 만들지 않는다.

---

## 9. Reviewer / Writer 명세 위치

사용자가 직접 호출하지 않지만, 동작 정책을 확인하고 싶다면:

모두 repo 루트 (이 사이트에 published 되지 않음, GitHub 에서만 확인 가능) 에 위치한다.

| 문서 | 다루는 내용 |
|---|---|
| `agents/SKILL.md` | review/write/update 명령의 상세 의미, 파일 컨벤션, 실행 규칙 |
| `agents/MATH_REVIEWER.md` | 수학 정확성 review 의 점검 항목 (정의·정리·증명·기호 일관성) |
| `agents/WRITING_REVIEWER.md` | 글쓰기 review 의 점검 항목 (구조·동기 부여·예시·MathJax 컨벤션) |
| `agents/WRITER.md` | 두 review 의 보고를 받아 `<n>.md` 를 재작성하는 WRITER agent. `## PDF Ingestion Mode` 절에 fetch-pdf 의 전체 workflow 명세 |
| `CLAUDE.md` | 프로젝트 최상위 가이드 — 빌드 명령, 디렉토리 구조, 컨벤션 요약 |

> 이 매뉴얼이 모순될 경우 위 문서의 명세가 우선한다.
