# 슈퍼컴퓨터 빠른 시작

이 튜토리얼은 공용 슈퍼컴퓨터 또는 클러스터 환경을 기준으로 작성되었습니다. 실제 모듈 이름과 큐/파티션 이름은 기관마다 다르므로, 아래 예시와 다른 경우에는 강사가 제공한 명령을 우선 사용하세요.

## 1. 로그인하기

```bash
ssh username@cluster.example.edu
```

## 2. 튜토리얼 파일 받기

PBS/Nurion처럼 home 디렉터리에서 `qsub`가 막힌 시스템에서는 `/scratch/$USER` 아래에서 clone하거나, 이미 home에 받은 복사본을 scratch로 복사한 뒤 그곳에서 작업합니다.

```bash
cd /scratch/$USER
```

```bash
git clone https://github.com/material-JH/xspectra-tutorial.git
cd xspectra-tutorial
```

강사가 공용 복사본 경로를 제공했다면, 위의 clone 대신 그 경로를 사용하세요.

## 3. 환경 설정하기

먼저 템플릿을 복사합니다.

```bash
cp env.sh.example env.sh
vim env.sh
git clone --depth 1 --branch develop https://github.com/QEF/q-e.git ~/q-e
source env.sh       # 감지된 QE 실행 파일과 TOOLS_DIR가 화면에 출력됩니다.
```

`/path/to/q-e` 같은 문구를 그대로 입력하지 마세요. 초보자는 보통 QE가 어디 설치되어 있는지 모르기 때문에, 먼저 클러스터 module이 제공하는 실행 파일 위치를 확인합니다.

```bash
module avail quantum
module avail qe
module avail espresso
```

강사 또는 클러스터 문서가 알려준 module을 로드합니다. 이름은 사이트마다 다릅니다.

```bash
module purge
module load quantum-espresso/7.3   # 예시입니다. 실제 module 이름으로 바꾸세요.
module load python/3.10             # 필요할 때만 사용하세요.
```

그 다음 QE 실행 파일이 보이는지 확인합니다.

```bash
command -v pw.x
command -v xspectra.x
command -v ld1.x
```

예를 들어 첫 번째 명령이 다음처럼 출력되면,

```text
/apps/qe/7.3/bin/pw.x
```

`BIN_DIR`는 `/apps/qe/7.3/bin`, `QE_ROOT`는 `/apps/qe/7.3`입니다. 새 `env.sh.example`은 module을 제대로 로드하면 이 값을 자동으로 찾도록 되어 있습니다. 따라서 대부분의 학생은 `env.sh`에서 module 이름만 자기 클러스터에 맞게 고치면 됩니다.

```bash
# env.sh 안에서 보통 고칠 부분
module purge
module load quantum-espresso/7.3
module load python/3.10
```

Slurm 작업 안에서는 MPI 실행 명령을 다음처럼 쓰는 경우가 많습니다.

```bash
export MPI_RUN="srun -n $NPROCS"
```

Slurm이 아니라 `mpirun`을 쓰는 시스템이라면 다음처럼 설정하세요.

```bash
export MPI_RUN="mpirun -np $NPROCS"
```

주의: 새 학생 계정에는 보통 QE source tree가 없으므로 [QE source tree와 유사퍼텐셜 준비](00_qe_source_and_pseudopotentials.md)를 참고해서 `$HOME/q-e`에 한 번 내려받으세요. 실행 파일은 module에서 쓰고, source tree는 `XSpectra/tools/upf2plotcore.sh` 같은 보조 파일을 찾는 데 사용합니다.

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

PBS/Nurion 예시:

```bash
cd /scratch/$USER/xspectra-tutorial
qsub scheduler/pbs_diamond.pbs
qstat -u "$USER"
```

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
