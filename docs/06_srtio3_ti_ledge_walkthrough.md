# SrTiO3 Ti L-edge 실습

Ti L-edge는 Ti 2p 코어 상태에서 Ti 3d 성분의 비점유 상태로의 전이를 봅니다. Ti L2,3 white-line 모양과 splitting은 원자가와 crystal field에 민감하므로 TEM/EELS 사용자에게 익숙한 edge입니다.

## 실행

```bash
cd SrTiO3/Ti_Ledge
bash run.sh
cd ../..
```

클러스터에서는 다음 방식이 더 좋습니다.

```bash
sbatch scheduler/slurm_srtio3_tiledge.sbatch
```

## 중요한 입력 선택

Ti 흡수 원자는 `Tih`로 레이블링되어 있습니다.

```fortran
ATOMIC_SPECIES
Sr   ...
Tih  ...   ! 흡수 원자
O    ...
```

따라서 다음처럼 설정합니다.

```fortran
ntyp = 3
xiabs = 2
edge = 'L2'
```

## 해석할 때 주의할 점

- 실험 EELS에서는 보통 L3와 L2 edge가 모두 보입니다.
- 이 예제는 `edge='L2'`를 사용합니다. 완전한 정량적 L2,3 simulation이 아니라 튜토리얼 계산으로 보세요.
- Energy alignment 후 정성적인 peak 위치와 상대적인 모양을 비교하세요.
