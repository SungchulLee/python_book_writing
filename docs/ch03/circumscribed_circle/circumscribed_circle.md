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
