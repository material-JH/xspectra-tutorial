# 이 튜토리얼에 필요한 Linux 기초

이 튜토리얼에서는 많지 않은 Linux 명령만 사용합니다. 명령 앞에 보이는 프롬프트 기호(`$`)가 있다면 직접 입력하지 않습니다.

## 디렉터리 이동

```bash
pwd                 # 현재 디렉터리 보기
ls                  # 파일 목록 보기
ls -lh              # 파일 크기와 함께 목록 보기
cd xspectra-tutorial    # 디렉터리 안으로 들어가기
cd ..               # 한 단계 위 디렉터리로 이동
```

## 파일 다루기

```bash
cp env.sh.example env.sh
vim env.sh          # 텍스트 파일 편집
more xspectra.out   # 긴 파일 보기; q를 누르면 종료
tail -40 xspectra.out
mkdir -p tmp
rm -rf tmp          # 주의: 하위 내용까지 재귀적으로 삭제
```

## 출력에서 문자열 찾기

```bash
grep "WALL" scf.out
grep "error" xspectra.out
```

## 클러스터 명령

Slurm 사용:

```bash
module list
module avail quantum
sbatch scheduler/slurm_diamond.sbatch
squeue -u "$USER"
scancel <jobid>
```

PBS/Torque 사용:

```bash
qsub job.pbs
qstat -u "$USER"
qdel <jobid>
```

## 좋은 습관

- 터미널 하나는 항상 프로젝트 최상위 디렉터리에 두세요.
- 문제가 생기면 먼저 `*.out` 파일을 읽어 보세요.
- 큰 계산은 로그인 노드에서 실행하지 마세요.
- 공용 파일을 삭제하기 전에는 반드시 강사에게 확인하세요.
