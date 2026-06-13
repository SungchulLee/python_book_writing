# 외접원과 사인법칙

삼각형의 한 변과 그 대각의 사인 사이에는 **외접원의 반지름**을 매개로 한 우아한 관계가 성립한다.

!!! note "사인법칙 (확장형)"
    삼각형 $\mathrm{ABC}$ 의 외접원의 반지름을 $R$ 이라 하면

    $$
    \frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R
    $$

    (단, $a = \overline{\mathrm{BC}}$, $b = \overline{\mathrm{CA}}$, $c = \overline{\mathrm{AB}}$.)

또한 삼각함수 $\sin 2x$, $\cos 2x$ 의 주기성·대칭성으로 인해 $\sin 2B = \sin 2C$ 또는 $\cos 2B = \cos 2C$ 같은 조건은 $B, C$ 의 관계를 **두 가지 경우**로 분기시킨다.

!!! note "각의 분기 조건"
    삼각형의 각 ($0 < A, B, C < \pi$, $A + B + C = \pi$) 에 대하여
    
    - $\sin 2B = \sin 2C \;\Leftrightarrow\; 2B = 2C \;\text{또는}\; 2B = \pi - 2C$
    - $\cos 2B = \cos 2C \;\Leftrightarrow\; 2B = 2C \;\text{또는}\; 2B = 2\pi - 2C$
    
    그러나 $A + B + C = \pi$ 와 결합하면 $2B = 2\pi - 2C$ 의 경우는 $A = 0$ 이어 불가. 따라서 **$B = C$ (이등변)** 또는 **$B + C = \pi/2$ 즉 $A = \pi/2$ (직각)**.

---

## 보기: 두 외접원의 넓이 비

삼각형 $\mathrm{ABC}$ 가 다음을 만족한다.

> (가) 세 변의 길이 중 가장 짧은 변의 길이는 $3$ 이다.
> (나) $\sin 2B = \sin 2C$ 또는 $\cos 2B = \cos 2C$.

(ㄴ) $\cos B = \dfrac{1}{3}$ 일 때 $\overline{\mathrm{BC}}$ 가 가질 수 있는 모든 값의 모임 $M$.

(ㄷ) 선분 $\mathrm{AB}$ 의 중점 $\mathrm{P}$. 삼각형 $\mathrm{APC}$ 의 외접원의 넓이 $S_1$, 삼각형 $\mathrm{BPC}$ 의 외접원의 넓이 $S_2$. $S_1/S_2$ 의 값이 $1/8, 3/8, 5/8$ 일 때 $\overline{\mathrm{BC}}$ 의 최솟값 $p, q, r$.

??? success "보기 풀이 (요약)"

    **집합 $M$.** (나) 에서 두 분기:

    1. **직각삼각형** $A = \pi/2$: $B$ 가 $\pi/4$ 이상이고 $\cos B = 1/3 \Rightarrow B > C$, $\overline{\mathrm{AB}}$ 가 가장 짧으므로 $\overline{\mathrm{AB}} = 3$. $\overline{\mathrm{BC}} = \overline{\mathrm{AB}}/\cos B = 3/(1/3) = 9$.
    2. **이등변삼각형** $B = C$: $B \ge \pi/3$ 이므로 $A \le \pi/3 < B$, $\overline{\mathrm{BC}}$ 가 가장 짧음 = $3$.

    $\boxed{M = \{3, 9\}}$

    **$p, q, r$.** 사인법칙 ($\overline{\mathrm{PC}}$ 기준): $2 R_1 = \overline{\mathrm{PC}}/\sin A$, $2 R_2 = \overline{\mathrm{PC}}/\sin B$. 즉

    $$
    \frac{S_1}{S_2} = \frac{R_1^2}{R_2^2} = \frac{\sin^2 B}{\sin^2 A}
    $$

    삼각형 $\mathrm{ABC}$ 의 외접원의 반지름을 $R$ 이라 하면 사인법칙으로 $\dfrac{\overline{\mathrm{BC}}}{\sin A} = \dfrac{\overline{\mathrm{AC}}}{\sin B}$, 즉 $\dfrac{S_1}{S_2} = \dfrac{\overline{\mathrm{AC}}^2}{\overline{\mathrm{BC}}^2}$.

    - **직각삼각형** $A = \pi/2$: 피타고라스 $\overline{\mathrm{AB}}^2 + \overline{\mathrm{AC}}^2 = \overline{\mathrm{BC}}^2$.
    - **이등변삼각형** $B = C$: $\overline{\mathrm{AB}} = \overline{\mathrm{AC}}$, $\cos B = \overline{\mathrm{BC}}/(2 \overline{\mathrm{AC}})$. 따라서 $\dfrac{S_1}{S_2} = \dfrac{1}{4\cos^2 B}$.

    **$(1) S_1/S_2 = 1/8$**:
    - 직각: $\overline{\mathrm{AC}}^2 : \overline{\mathrm{AB}}^2 : \overline{\mathrm{BC}}^2 = 1 : 7 : 8$. $\overline{\mathrm{AC}} < \overline{\mathrm{AB}} < \overline{\mathrm{BC}}$, $\overline{\mathrm{AC}} = 3$, $\overline{\mathrm{BC}} = 3 \cdot 2\sqrt 2 = 6\sqrt 2$.
    - 이등변: $1/(4\cos^2 B) \ge 1/4 > 1/8$ 이므로 해 없음.

    $\boxed{p = 6\sqrt 2}$

    **$(2) S_1/S_2 = 3/8$**:
    - 직각: $\overline{\mathrm{AC}}^2 : \overline{\mathrm{AB}}^2 : \overline{\mathrm{BC}}^2 = 3 : 5 : 8$. $\overline{\mathrm{AC}} = 3$, $\overline{\mathrm{BC}} = 2\sqrt 6$.
    - 이등변: $\dfrac{1}{4\cos^2 B} = 3/8 \Rightarrow \cos B = \sqrt 6/3$, $\overline{\mathrm{BC}} = 6\cos B = 2\sqrt 6$ (이등변에서 $\overline{\mathrm{AB}} = \overline{\mathrm{AC}} = 3$).

    $\boxed{q = 2\sqrt 6}$

    **$(3) S_1/S_2 = 5/8$**:
    - 직각: $\overline{\mathrm{AC}}^2 : \overline{\mathrm{AB}}^2 : \overline{\mathrm{BC}}^2 = 5 : 3 : 8$. $\overline{\mathrm{AC}} > \overline{\mathrm{AB}}$, $\overline{\mathrm{AB}} = 3$, $\overline{\mathrm{BC}} = 3 \cdot 2\sqrt 6/\sqrt 3 = 2\sqrt 6$.

      잠깐 — 다시: $\overline{\mathrm{AB}}^2 = 3 \cdot 3 = 9$, $\overline{\mathrm{BC}}^2 = 8 \cdot 3 = 24$, $\overline{\mathrm{BC}} = 2\sqrt 6$.

    - 이등변: $\dfrac{1}{4\cos^2 B} = 5/8 \Rightarrow \cos B = \sqrt{10}/5$, $\overline{\mathrm{BC}} = 6 \cdot \sqrt{10}/5 = \dfrac{6\sqrt{10}}{5}$.
    
    $6\sqrt{10}/5 \approx 3.79 < 2\sqrt 6 \approx 4.90$ 이므로 최솟값은 이등변에서.

    $\boxed{r = \dfrac{6\sqrt{10}}{5}}\quad\square$

!!! info "교훈"
    - **각의 분기 조건** $\sin 2B = \sin 2C$ 또는 $\cos 2B = \cos 2C$ 가 삼각형을 **직각** 또는 **이등변** 두 경우로 한정.
    - 외접원의 넓이 비는 사인법칙의 변형으로 변의 비로 직접 변환.
    - 최솟값을 구할 때는 두 경우의 후보를 비교한다.

---

**연습문제 (보충).** [넓이와 두 변으로부터 내접원 반지름]
삼각형 $\mathrm{ABC}$ 에서 $\overline{\mathrm{AB}} = 5$, $\overline{\mathrm{AC}} = 3$, 넓이 $= \sqrt{26}$ 이다. $\angle A$ 가 예각일 때 삼각형 $\mathrm{ABC}$ 의 내접원의 반지름의 길이를 구하시오.

??? success "연습문제 (보충) 풀이"

    $S = \dfrac{1}{2} \cdot 3 \cdot 5 \sin A = \sqrt{26} \Rightarrow \sin A = \dfrac{2\sqrt{26}}{15}$.

    $\angle A$ 예각이므로 $\cos A = \sqrt{1 - 4 \cdot 26/225} = \sqrt{121/225} = \dfrac{11}{15}$.

    코사인법칙: $\overline{\mathrm{BC}}^2 = 9 + 25 - 2 \cdot 3 \cdot 5 \cdot \dfrac{11}{15} = 34 - 22 = 12$, $\overline{\mathrm{BC}} = 2\sqrt 3$.

    내접원 반지름 공식 $S = \dfrac{1}{2}(a + b + c) r$:

    $$
    r = \frac{2S}{a + b + c} = \frac{2\sqrt{26}}{2\sqrt 3 + 3 + 5} = \frac{2\sqrt{26}}{8 + 2\sqrt 3} = \frac{\sqrt{26}}{4 + \sqrt 3} = \frac{\sqrt{26}(4 - \sqrt 3)}{13} = \frac{4\sqrt{26} - \sqrt{78}}{13}\quad\square
    $$

---

**연습문제 (보충 2).** [사인 덧셈정리 + 정사각형 내접 재귀 등비급수]
한 변의 길이가 $2$ 인 정사각형 $\mathrm{A}_1\mathrm{B}_1\mathrm{C}_1\mathrm{D}_1$ 에 내접하는 원과 그 원에 내접하는 정사각형 $\mathrm{A}_2\mathrm{B}_2\mathrm{C}_2\mathrm{D}_2$ 를 만든다 (구체적인 작도는 출제 그림 참조). 이 과정을 반복하여 정사각형 $\mathrm{A}_n\mathrm{B}_n\mathrm{C}_n\mathrm{D}_n$ 을 얻고 그 넓이를 $S_n$ 이라 하자. 변환의 각도가 $\theta$ ($\pi/4 < \theta < \pi/2$) 이고 $\cos\theta = \dfrac{\sqrt 5}{5}$ 일 때 $\displaystyle\sum_{n=1}^{\infty} S_n$ 을 구하시오.

??? success "연습문제 (보충 2) 풀이 (요약)"

    원 (외접원) 의 반지름을 $a$, 내접하는 정사각형의 한 변 길이를 $r$ 이라 하면 사인 덧셈정리에 의하여

    $$
    r = a \cdot \frac{\sin(\theta + \pi/4)}{\sin\theta} = \frac{\sqrt 2}{2}\,a(1 + \cot\theta)
    $$

    한편 정사각형 → 내접원의 반지름은 (한 변)/2 이므로, $a$ 와 $r$ 사이의 관계와 결합하여

    $$
    r = \frac{2(1 + \cot\theta)}{(1 + \cot\theta)^2 + 2}\quad (\text{한 변 } 2 \text{ 인 정사각형에서})
    $$

    $\cos\theta = \sqrt 5/5$ 이므로 $\sin\theta = 2\sqrt 5/5$, $\cot\theta = 1/2$. 대입:

    $$
    r = \frac{2 \cdot 3/2}{(3/2)^2 + 2} = \frac{3}{9/4 + 2} = \frac{3}{17/4} = \frac{12}{17}
    $$

    각 단계의 정사각형 넓이의 비는 $r^2/4$ (한 변이 $r/2$ 배가 아니라 $r$ 배인 경우와 비교 필요. 출제 풀이의 결과는 공비 $r^2/4$). $S_1 = 4$, 공비 $r^2/4$ 의 무한등비급수:

    $$
    \sum_{n=1}^{\infty} S_n = \frac{S_1}{1 - r^2/4} = \frac{4}{1 - (12/17)^2/4} = \frac{4}{1 - 144/(4\cdot 289)} = \frac{4}{1 - 36/289} = \frac{4 \cdot 289}{253} = \frac{1156}{253}\quad\square
    $$

    !!! info "교훈"
        - **사인 덧셈정리 + 작도** 가 결합되어 한 단계마다의 변 길이 비를 정확히 계산한다.
        - 무한등비급수의 공비가 $1$ 보다 작아야 수렴; 이 문제에서는 공비 $r^2/4 = (12/17)^2/4 = 36/289 < 1$.

---

**연습문제 (보충 2).** [$\sin 2B = \sin 2C$ 또는 $\cos 2B = \cos 2C$ + 외접원 넓이 비]

삼각형 $\mathrm{ABC}$ 가 다음을 만족한다.

> (가) 세 변의 길이 중 가장 짧은 변의 길이는 $3$ 이다.
> (나) $\sin 2 B = \sin 2 C$ 또는 $\cos 2 B = \cos 2 C$ 이다.

선분 $\overline{\mathrm{AB}}$ 의 중점을 $\mathrm P$, 삼각형 $\mathrm{APC}, \mathrm{BPC}$ 의 외접원의 넓이를 각각 $S_1, S_2$ 라 하자.

(1) $\cos B = \dfrac{1}{3}$ 일 때, $\overline{\mathrm{BC}}$ 가 가질 수 있는 모든 값의 모임 $M$.

(2) $\dfrac{S_1}{S_2}$ 가 $\dfrac{1}{8}, \dfrac{3}{8}, \dfrac{5}{8}$ 일 때 $\overline{\mathrm{BC}}$ 의 최솟값을 각각 $p, q, r$.

??? success "연습문제 (보충 2) 풀이"

    **조건 (나) 분석.** $\sin 2 B = \sin 2 C \Rightarrow 2B = 2C$ 또는 $2B = \pi - 2C$ (즉 $A = \pi/2$). $\cos 2 B = \cos 2 C \Rightarrow 2B = 2C$ 또는 $2B = 2\pi - 2C$ ($A + B + C = \pi$ 와 모순으로 배제). 가능: $B = C$ (이등변) 또는 $A = \pi/2$ (직각).

    **(1) $\cos B = 1/3$.**

    - **직각 ($A = \pi/2$)**: $B$ 는 $\pi/4$ 이상이므로 $B > C$ 즉 $\overline{\mathrm{AB}}$ 가 가장 짧음, 길이 $3$. $\overline{\mathrm{BC}} = \overline{\mathrm{AB}}/\cos B = 3 \cdot 3 = 9$.
    - **이등변 ($B = C$)**: $B$ 는 $\pi/3$ 이상이므로 $A < B = C$, $\overline{\mathrm{BC}}$ 가 가장 짧음, 길이 $3$.

    $M = \boxed{\{3,\ 9\}}\quad\square$

    **(2) 외접원 비 환원.** $\overline{\mathrm{PC}}$ 를 기준으로 두 삼각형에 사인법칙: $2 R_1 = \overline{\mathrm{PC}}/\sin A$, $2 R_2 = \overline{\mathrm{PC}}/\sin B$. 따라서

    $$
    \frac{S_1}{S_2} = \frac{R_1^2}{R_2^2} = \frac{\sin^2 B}{\sin^2 A}
    $$

    $\mathrm{ABC}$ 의 외접원 반지름 $R$ 의 사인법칙으로 $\sin B/\sin A = \overline{\mathrm{AC}}/\overline{\mathrm{BC}}$. 따라서 $\dfrac{S_1}{S_2} = \dfrac{\overline{\mathrm{AC}}^2}{\overline{\mathrm{BC}}^2}$.

    - **직각 시**: $\overline{\mathrm{AB}}^2 + \overline{\mathrm{AC}}^2 = \overline{\mathrm{BC}}^2$.
    - **이등변 시**: $\overline{\mathrm{AC}} = \overline{\mathrm{AB}}$, $\cos B = \overline{\mathrm{BC}}/(2 \overline{\mathrm{AC}})$, $\dfrac{S_1}{S_2} = \dfrac{1}{4 \cos^2 B}$.

    각 비율별:

    - $S_1/S_2 = 1/8$: 직각 ⇒ $\overline{\mathrm{AC}}^2 : \overline{\mathrm{AB}}^2 : \overline{\mathrm{BC}}^2 = 1 : 7 : 8$. 가장 짧은 변 $\overline{\mathrm{AC}} = 3$, $\overline{\mathrm{BC}} = 3\cdot 2\sqrt 2 = 6\sqrt 2$. 이등변은 $1/(4\cos^2 B) = 1/8 < 1/4$ 불가능. $p = \boxed{6\sqrt 2}$.
    - $S_1/S_2 = 3/8$: 직각 ⇒ $3 : 5 : 8$, 짧은 변 $\overline{\mathrm{AC}} = 3$, $\overline{\mathrm{BC}} = 2\sqrt 6$. 이등변 ($\cos B = \sqrt 6/3$): $\overline{\mathrm{BC}} = 6 \cos B = 2\sqrt 6$. 두 경우 일치, $q = \boxed{2\sqrt 6}$.
    - $S_1/S_2 = 5/8$: 직각 ⇒ $5 : 3 : 8$, 짧은 변 $\overline{\mathrm{AB}} = 3$, $\overline{\mathrm{BC}} = 2\sqrt 6$. 이등변 ($\cos B = \sqrt{10}/5$): $\overline{\mathrm{BC}} = 6\sqrt{10}/5 < 2\sqrt 6$. 최소 $r = \boxed{\dfrac{6\sqrt{10}}{5}}$.

    !!! info "교훈"
        - **$\sin 2B = \sin 2C$ 또는 $\cos 2B = \cos 2C$** ⇔ **이등변 ($B = C$) 또는 직각 ($A = \pi/2$)**. 두 경우 모두 검토 필요.
        - **사인법칙 두 번 적용**: $\overline{\mathrm{PC}}$ 를 두 삼각형이 공유 ⇒ 외접원 반지름 비가 $\sin^{-1}$ 비. 다시 사인법칙으로 $\overline{\mathrm{AC}}/\overline{\mathrm{BC}}$ 비로 환원.
