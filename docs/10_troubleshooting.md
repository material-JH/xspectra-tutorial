# 문제 해결

## `env.sh not found`

템플릿에서 새로 만드세요.

```bash
cp env.sh.example env.sh
vim env.sh
```

## `pw.x: command not found` 또는 `pw.x`가 없음

가능한 원인: QE module이 잘못되었거나 `BIN_DIR` 설정이 틀렸습니다.

```bash
module avail quantum
module load quantum-espresso
which pw.x
```

그 다음 `env.sh`를 수정하세요.

## `xspectra.x`가 없음

로드한 QE build에 XSpectra가 포함되어 있지 않을 수 있습니다. 강사에게 XSpectra가 활성화된 QE module을 문의하세요.

## `upf2plotcore.sh`가 없음

`TOOLS_DIR`를 확인하세요.

```bash
find "$QE_ROOT" -name upf2plotcore.sh
```

`env.sh`에서 `TOOLS_DIR`를 해당 script가 들어 있는 디렉터리로 설정하세요.

## 유사퍼텐셜 파일을 열 수 없음

생성된 `scf.in`의 `pseudo_dir`를 확인하고, 파일이 실제로 있는지 확인하세요.

```bash
ls SrTiO3/pseudo/
ls "$EXAMPLE_PSEUDO_DIR"
```

## `O.wfc` 또는 `Ti.wfc`가 없음

수정된 스크립트는 이 파일들을 자동으로 생성합니다. 필요하면 다음처럼 수동으로 다시 생성하세요.

```bash
$TOOLS_DIR/upf2plotcore.sh SrTiO3/pseudo/O.pbe-n-kjpaw_psl.0.1.UPF > O.wfc
$TOOLS_DIR/upf2plotcore.sh SrTiO3/pseudo/Ti.pbe-spn-kjpaw_psl.1.0.0.UPF > Ti.wfc
```

## `xspectra.x did not produce xanes.dat`

출력 파일의 마지막 부분을 읽어 보세요.

```bash
tail -80 xspectra.out
```

흔한 원인은 잘못된 `xiabs`, 없는 `filecore`, `outdir` 안의 SCF 데이터 누락, 또는 호환되지 않는 유사퍼텐셜입니다.

## MPI launcher 실패

Slurm 클러스터에서는 작업 안에서 다음 설정을 권장합니다.

```bash
export MPI_RUN="srun -n $NPROCS"
```

다른 시스템에서는 다음처럼 설정합니다.

```bash
export MPI_RUN="mpirun -np $NPROCS"
```

로그인 노드 정책 오류가 보이면, 대화형 실행 대신 스케줄러로 작업을 제출하세요.

## 작업이 wall time을 초과함

튜토리얼 중에는 reference output을 사용하거나, 강사에게 scheduler script의 wall time을 늘려 달라고 요청하세요.
