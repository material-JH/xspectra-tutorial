# Core-hole 방법

Core-hole 근사는 여기된 전자와 뒤에 남은 core hole 사이의 상호작용을 모사합니다.

## 접근법

| 방법 | 유사퍼텐셜 | `tot_charge` | 용도 |
|---|---|---:|---|
| Core hole 없음 | 표준 유사퍼텐셜 | 0 | 가장 빠른 시작점 |
| Full core hole (FCH) | 코어 전자 하나 제거 | +1.0 | 최종 상태 효과가 큼 |
| Half core hole (HCH) | 코어 전자 반 개 제거 | +0.5 | 자주 쓰는 절충안 |

## 중요한 규칙

1. 흡수 원자는 반드시 독립적인 species label을 가져야 합니다.
2. Core-hole 유사퍼텐셜은 흡수 원자에만 사용합니다.
3. `tot_charge`는 core hole 하나에 대응하며 supercell 크기에 따라 바꾸지 않습니다.
4. `filecore`는 원래의 non-core-hole 유사퍼텐셜에서 추출해야 합니다.
5. XSpectra에 사용할 core-hole 유사퍼텐셜에는 GIPAW reconstruction이 필요합니다.

## 유사퍼텐셜 생성

`ld1.x` 입력 파일은 다음 위치에 있습니다.

```text
SrTiO3/pseudo/gen_*.in
```

강사가 유사퍼텐셜 생성을 시연하려는 경우에만 직접 실행하세요. 대부분의 튜토리얼 세션에서는 시간을 절약하기 위해 제공된 유사퍼텐셜을 사용합니다.
