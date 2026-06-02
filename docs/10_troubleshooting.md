# 문제 해결

## `env.sh not found`

템플릿에서 새로 만드세요.

```bash
cp env.sh.example env.sh
vim env.sh
```

## `env.sh`를 실행했는데 아무것도 안 보임

설정 파일이 아무 메시지도 출력하지 않으면 초보자는 성공인지 실패인지 알기 어렵습니다. 최신 `env.sh.example`은 다음 명령을 실행했을 때 상태 요약을 출력합니다.

```bash
bash env.sh.example     # 빠른 확인용: 현재 shell 환경은 바꾸지 않습니다.
```

실제 튜토리얼에서는 복사한 `env.sh`를 수정한 뒤, 현재 shell에 적용해 봅니다.

```bash
cp env.sh.example env.sh
vim env.sh
source env.sh           # 감지된 pw.x, xspectra.x, QE_ROOT 등이 출력됩니다.
./check_setup.sh
```

`bash env.sh`처럼 실행하면 화면에는 상태가 보이지만, 그 안에서 설정한 환경변수는 명령이 끝난 뒤 현재 shell에 남지 않습니다. 그래서 직접 확인할 때는 `source env.sh`, 최종 검사는 `./check_setup.sh`를 사용하세요.

## `pw.x: command not found` 또는 `pw.x`가 없음

가능한 원인: QE module이 아직 로드되지 않았거나, `env.sh`의 module 이름이 현재 클러스터와 맞지 않습니다. `/path/to/q-e`를 그대로 쓰면 안 됩니다.

먼저 사용할 수 있는 module 이름을 찾아보세요.

```bash
module avail quantum
module avail qe
module avail espresso
```

강사 또는 클러스터 문서가 알려준 이름으로 module을 로드한 뒤, 실행 파일 위치를 확인합니다.

```bash
module purge
module load quantum-espresso/7.3   # 예시입니다. 실제 이름으로 바꾸세요.
command -v pw.x
```

예를 들어 다음처럼 나오면,

```text
/apps/qe/7.3/bin/pw.x
```

`env.sh`에서는 보통 module line만 제대로 고치면 됩니다. 수동으로 써야 한다면 다음처럼 적습니다.

```bash
export BIN_DIR=/apps/qe/7.3/bin
export QE_ROOT=/apps/qe/7.3
```

## `xspectra.x`가 없음

로드한 QE build에 XSpectra가 포함되어 있지 않을 수 있습니다. 먼저 확인하세요.

```bash
command -v xspectra.x
```

아무것도 출력되지 않으면 강사에게 XSpectra가 활성화된 QE module을 문의하세요.

## `upf2plotcore.sh`가 없음

`upf2plotcore.sh`는 실행 파일 `pw.x`와 달리 QE source tree의 `XSpectra/tools/` 아래에 있는 경우가 많습니다. cluster module이 실행 파일만 제공하면 이 파일이 없을 수 있습니다.

```bash
find "$QE_ROOT" -name upf2plotcore.sh
```

찾으면 `env.sh`에서 `TOOLS_DIR`를 해당 script가 들어 있는 디렉터리로 설정하세요. 새 계정이거나 찾지 못하면 QE source tree를 `$HOME/q-e`에 내려받아 `TOOLS_DIR`로 사용합니다.

```bash
cd ~
git clone --depth 1 --branch develop https://github.com/QEF/q-e.git q-e
export TOOLS_DIR=$HOME/q-e/XSpectra/tools
```

자세한 설명은 [QE source tree와 유사퍼텐셜 준비](00_qe_source_and_pseudopotentials.md)를 참고하세요.

## 유사퍼텐셜 파일을 열 수 없음

생성된 `scf.in`의 `pseudo_dir`를 확인하고, 파일이 실제로 있는지 확인하세요. Diamond 예제의 Carbon 유사퍼텐셜은 이제 `diamond/pseudo/`에 포함되어 있습니다.

```bash
ls diamond/pseudo/
ls SrTiO3/pseudo/
ls "$EXAMPLE_PSEUDO_DIR"
```

`EXAMPLE_PSEUDO_DIR`가 비어 있거나 잘못되었다면, 보통 다음처럼 저장소 안의 Diamond pseudo 폴더를 사용하면 됩니다.

```bash
export EXAMPLE_PSEUDO_DIR=$PWD/diamond/pseudo
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
