# SrTiO3 O K-edge 실습

O K-edge는 O 1s 상태에서 비점유 O 2p 성분 상태로의 전이를 봅니다. SrTiO3에서는 이러한 O 2p 상태가 Ti 3d 상태와 강하게 hybridization하므로, 이 edge는 Ti-O 결합과 팔면체 전자 구조에 민감합니다.

## 실행

```bash
cd SrTiO3/O_Kedge
bash run.sh
cd ../..
```

클러스터에서는 다음 방식이 더 좋습니다.

```bash
sbatch scheduler/slurm_srtio3_okedge.sbatch
```

## 중요한 입력 선택

SCF 입력에서 산소 하나는 `Oh`로 레이블링되어 있습니다.

```fortran
ATOMIC_SPECIES
Sr  ...
Ti  ...
Oh  ...   ! 흡수 원자
O   ...   ! 나머지 산소
```

따라서 다음처럼 설정합니다.

```fortran
ntyp = 4
xiabs = 3
```

## TEM/EELS 해석

- O K-edge: O 1s에서 O 2p 성분의 비점유 상태로 가는 전이입니다.
- SrTiO3에서 초기 O K-edge feature는 Ti t2g/eg 성분의 전도 상태와의 hybridization을 반영합니다.
- 계산 스펙트럼은 상대 에너지 축을 사용하므로, 실험 에너지 손실과 비교하기 전에 energy alignment가 필요합니다.
- Broadening은 `xgamma`로 정합니다. 이는 완전한 장비 응답 함수 모델은 아닙니다.

## 출력

```text
SrTiO3/O_Kedge/O_Kedge.dat
```

그림은 다음처럼 그립니다.

```bash
cd SrTiO3
python3 plot_spectra.py
```
