# XSpectra 튜토리얼

TEM/EELS 학생과 포닥을 위한 Quantum ESPRESSO + XSpectra 한국어 실습 자료입니다. 리눅스와 QE가 처음인 학습자를 기준으로, 슈퍼컴퓨터 접속부터 Diamond/SrTiO3 XSpectra 예제 실행과 스펙트럼 비교까지 순서대로 안내합니다.

## 빠른 시작

PBS/Nurion처럼 home 디렉터리에서 `qsub`가 막힌 시스템에서는 먼저 자기 scratch 디렉터리에서 저장소를 받으세요.

```bash
cd /scratch/$USER
```

```bash
git clone https://github.com/material-JH/xspectra-tutorial.git
cd xspectra-tutorial
cp env.sh.example env.sh
vim env.sh        # Nurion 기본 module 줄은 설정되어 있습니다. 다른 클러스터면 수정하세요.
git clone --depth 1 --branch develop https://github.com/QEF/q-e.git ~/q-e
source env.sh     # 감지된 실행 파일과 $HOME/q-e/XSpectra/tools 경로가 출력됩니다.
./check_setup.sh
```

QE source tree는 이 튜토리얼 repo 안에 넣지 않습니다. 새 계정에서는 각자 `$HOME/q-e` 같은 별도 위치에 내려받고, `env.sh`는 그 안의 `XSpectra/tools`를 `TOOLS_DIR`로 사용합니다.

Slurm 클러스터에서는 첫 예제를 작업으로 제출합니다.

```bash
sbatch scheduler/slurm_diamond.sbatch
squeue -u "$USER"
```

큰 QE/XSpectra 계산은 로그인 노드에서 직접 실행하지 말고, 계산 노드나 스케줄러 작업 안에서 실행하세요.

## 목차

### 본편

1. [슈퍼컴퓨터 빠른 시작](docs/00_supercomputer_quickstart.md)
2. [QE source tree와 유사퍼텐셜 준비](docs/00_qe_source_and_pseudopotentials.md)
3. [이 튜토리얼에 필요한 리눅스 기초](docs/01_linux_basics_for_tutorial.md)
4. [Quantum ESPRESSO 입력 파일 기초](docs/02_quantum_espresso_input_basics.md)
5. [XSpectra 계산 흐름](docs/03_xspectra_pipeline.md)
6. [Diamond C K-edge 예제](docs/04_diamond_walkthrough.md)
7. [SrTiO3 O K-edge 예제](docs/05_srtio3_o_kedge_walkthrough.md)
8. [Core-hole 근사 비교](docs/07_core_hole_methods.md)
9. [계산 스펙트럼과 EELS 비교](docs/08_compare_with_eels.md)
10. [Supercell과 MPI 참고](docs/09_supercell_and_mpi.md)
11. [문제 해결](docs/10_troubleshooting.md)

### 자료

- [학생용 HTML 발표 자료](https://material-jh.github.io/xspectra-tutorial/xspectra_tutorial_presentation.html)
- [Oh My QE 플러그인 가이드](https://material-jh.github.io/xspectra-tutorial/oh-my-qe.html) ([PDF](https://material-jh.github.io/xspectra-tutorial/oh-my-qe.pdf))
- [강사용 체크리스트](docs/instructor_checklist.md)
- [계산/데이터 출처](data_provenance.md)
- [참고문헌](CITATION.md)
- [Slurm 작업 예시](scheduler/slurm_diamond.sbatch)
- [PBS 작업 예시 설명](scheduler/pbs_examples.md)

## 저장소에서 자주 쓰는 파일

- `env.sh.example` → `env.sh`로 복사해서 클러스터 경로, module, MPI 설정을 적습니다.
- `check_setup.sh` — QE/XSpectra 실행 파일, pseudopotential, Python 환경을 확인합니다.
- `reference_output/` — 계산이 오래 걸리거나 실패했을 때 비교할 수 있는 기준 출력입니다.
- `diamond/` — 짧은 Diamond C K-edge 연습 예제입니다. 필요한 Carbon 유사퍼텐셜은 `diamond/pseudo/`에 포함되어 있습니다.
- `SrTiO3/` — O K-edge, core-hole, supercell, EELS 비교 예제가 들어 있습니다.
