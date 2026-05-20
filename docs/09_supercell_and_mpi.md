# Supercell과 MPI 참고사항

## 왜 supercell을 사용할까요?

주기적 경계 조건에서는 core hole이 모든 단위격자에서 반복됩니다. Supercell을 사용하면 core-hole image 사이의 거리가 늘어나고 인공적인 상호작용이 줄어듭니다.

SrTiO3의 경우:

- 단위격자: 원자 5개.
- 2x2x2 supercell: 원자 40개.
- 흡수 원자 하나는 HCH 유사퍼텐셜을 사용합니다.
- 나머지 원자는 표준 유사퍼텐셜을 사용합니다.
- half core hole 하나에 대해서는 `tot_charge=+0.5`를 그대로 유지합니다.

## MPI와 k-point pool

XSpectra는 k-point pool 병렬화의 이점을 크게 받을 수 있습니다.

```bash
xspectra.x -nk N
```

2x2x2 SrTiO3 supercell 예제에서는 다음처럼 작은 수의 k-point pool을 사용하세요.

```bash
-nk 4
```

Supercell SCF 예제에서는 다음 옵션을 사용합니다.

```bash
-nd 1
```

이는 이 튜토리얼 시스템에서 관찰된 ScaLAPACK diagonalization 실패를 피하기 위한 설정입니다.

## 클러스터 권장사항

Supercell 작업은 반드시 스케줄러를 통해 실행하세요. 예시:

```bash
sbatch scheduler/slurm_srtio3_okedge.sbatch
```

Wall time과 partition은 강사의 클러스터 환경에 맞게 조정하세요.
