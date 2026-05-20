# 슈퍼컴퓨터 빠른 시작

이 튜토리얼은 공용 슈퍼컴퓨터 또는 클러스터 환경을 기준으로 작성되었습니다. 실제 모듈 이름과 큐/파티션 이름은 기관마다 다르므로, 아래 예시와 다른 경우에는 강사가 제공한 명령을 우선 사용하세요.

## 1. 로그인하기

```bash
ssh username@cluster.example.edu
```

## 2. 튜토리얼 파일 받기

```bash
git clone https://github.com/material-JH/xspectra-tutorial.git
cd xspectra-tutorial
```

강사가 공용 복사본 경로를 제공했다면, 위의 clone 대신 그 경로를 사용하세요.

## 3. 환경 설정하기

```bash
cp env.sh.example env.sh
vim env.sh
```

`env.sh`에 들어가는 일반적인 클러스터 설정 예시는 다음과 같습니다.

```bash
module purge
module load quantum-espresso
module load openmpi
module load python
export QE_ROOT=/path/to/q-e
export BIN_DIR=$QE_ROOT/bin
export TOOLS_DIR=$QE_ROOT/XSpectra/tools
export EXAMPLE_PSEUDO_DIR=$QE_ROOT/XSpectra/examples/pseudo
export NPROCS=4
export MPI_RUN="srun -n $NPROCS"      # Slurm 작업 내부에서 사용
```

사용하는 시스템이 `mpirun`을 쓴다면 다음처럼 설정하세요.

```bash
export MPI_RUN="mpirun -np $NPROCS"
```

## 4. 설정 확인 실행하기

```bash
bash check_setup.sh
```

설정 확인 스크립트는 가볍고 로그인 노드에서 실행해도 안전합니다. QE 계산을 실제로 실행하지는 않습니다.

## 5. 작업 제출하기

Slurm을 사용하는 경우:

```bash
sbatch scheduler/slurm_diamond.sbatch
squeue -u "$USER"
```

필요하면 작업을 취소할 수 있습니다.

```bash
scancel <jobid>
```

PBS/Torque를 사용하는 경우에는 `scheduler/pbs_examples.md`를 참고하세요.

## 6. 로그인 노드와 계산 노드

비싼 MPI 계산을 로그인 노드에서 직접 실행하지 마세요. 다음 중 하나를 사용합니다.

- 배치 작업에는 `sbatch`를 사용합니다.
- 대화형 Slurm 세션에는 `salloc` + `srun`을 사용합니다.
- PBS/Torque 작업에는 `qsub`를 사용합니다.

작은 파일 편집, 그림 그리기, `git`, `bash check_setup.sh` 실행은 보통 로그인 노드에서 해도 괜찮습니다.

## 7. 출력 파일이 저장되는 위치

각 계산 디렉터리에는 다음 파일이 만들어집니다.

- `pw.x`가 사용하는 `scf.in`, `scf.out`.
- `xspectra.x`가 사용하는 `xspectra.in`, `xspectra.out`.
- 유사퍼텐셜에서 추출한 `*.wfc` 코어 파동함수.
- 최종 스펙트럼인 `*.dat` 파일.
- QE 임시 파일이 저장되는 `tmp/` 디렉터리.

작업이 실패하면 먼저 다음 파일 끝부분을 확인하세요.

```bash
tail -80 scf.out
tail -80 xspectra.out
```
