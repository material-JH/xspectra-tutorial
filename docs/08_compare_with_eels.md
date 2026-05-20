# XSpectra와 EELS 비교

XSpectra 계산 결과와 실험 EELS 스펙트럼은 자동으로 같은 에너지 축이나 intensity scale 위에 놓이지 않습니다.

## 에너지 정렬(Energy alignment)

계산 스펙트럼은 보통 전자 구조 기준에 대한 상대 에너지를 사용합니다. 실험 스펙트럼은 절대 에너지 손실을 사용합니다. 첫 튜토리얼 비교에서는 다음 절차를 사용하세요.

1. Intensity를 normalize합니다.
2. 실험 스펙트럼에서 큰 peak 하나를 찾습니다.
3. 그에 대응하는 계산 peak를 찾습니다.
4. 전체 에너지 축에 rigid shift를 적용합니다.

## 이 튜토리얼에서 의미 있게 볼 수 있는 것

- 대략적인 peak 순서.
- No-core-hole, FCH, HCH 사이의 정성적 변화.
- O K-edge의 hybridization feature.
- 정성적 수준의 Ti L-edge white-line 모양.

## 이 튜토리얼에서 완전히 모델링하지 않는 것

- 다중 산란(plural scattering).
- 자세한 background subtraction.
- collection/convergence angle 의존성.
- 시편 두께.
- 절대 cross-section intensity.
- 완전한 장비 broadening.

이 비교는 최종 정량 EELS simulation이 아니라 해석을 돕는 가이드로 사용하세요.
