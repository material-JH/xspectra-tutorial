# QE source tree와 유사퍼텐셜 준비

이 튜토리얼에서 필요한 파일은 두 종류입니다.

1. **QE/XSpectra 실행 파일**: `pw.x`, `xspectra.x`, `ld1.x`
2. **QE source tree 안의 보조 파일**: 특히 `XSpectra/tools/upf2plotcore.sh`

초보자는 보통 QE 전체를 직접 빌드하지 않습니다. 실행 파일은 클러스터 module을 쓰고, source tree는 `upf2plotcore.sh` 같은 XSpectra 보조 파일을 얻기 위해 홈 디렉터리에 한 번 내려받습니다.

## 이 저장소에 이미 들어 있는 유사퍼텐셜

학생이 처음 실행하는 예제가 유사퍼텐셜 파일 때문에 멈추지 않도록, 작은 Diamond C K-edge 유사퍼텐셜은 저장소에 포함했습니다.

```text
diamond/pseudo/
  C_PBE_TM_2pj.UPF
  Ch_PBE_TM_2pj.UPF
```

SrTiO3 예제 유사퍼텐셜도 저장소에 포함되어 있습니다.

```text
SrTiO3/pseudo/
```

따라서 일반 학생은 유사퍼텐셜만 받기 위해 QE source tree를 찾을 필요는 없습니다. 그래도 새 계정에서는 `upf2plotcore.sh`를 안정적으로 쓰기 위해 QE source tree를 `$HOME/q-e`에 clone합니다. `env.sh.example`은 기본적으로 `diamond/pseudo/`를 `EXAMPLE_PSEUDO_DIR`로 사용합니다.

## QE source tree 내려받기

새 계정에서는 다음을 먼저 실행해서 QE source tree를 `$HOME/q-e`에 받으세요. 이미 `$HOME/q-e`가 있다면 다시 받을 필요는 없습니다.

```bash
cd "$HOME"
git clone --depth 1 --branch develop https://github.com/QEF/q-e.git q-e
```

브라우저 주소는 `https://github.com/QEF/q-e/tree/develop`이지만, 터미널에서 clone할 때는 위처럼 `.git` 주소를 사용합니다.

다운로드 뒤에는 다음 위치를 확인합니다.

```bash
[ -f "$HOME/q-e/XSpectra/tools/upf2plotcore.sh" ] && echo "PASS upf2plotcore.sh" || echo "WARN upf2plotcore.sh not found"
[ -f "$HOME/q-e/XSpectra/examples/pseudo/C_PBE_TM_2pj.UPF" ] && echo "PASS QE example pseudo" || echo "WARN QE example pseudo not found"
```

## `env.sh`에 적는 값

QE 실행 파일은 여전히 클러스터 module에서 찾는 것이 보통입니다.

```bash
module load quantum-espresso/7.3   # 예시입니다. 실제 module 이름으로 바꾸세요.
```

QE source tree를 `$HOME/q-e`에 받았다면 `env.sh`에는 보통 다음 한 줄만 추가하면 됩니다. 다른 위치에 clone했다면 `$HOME/q-e` 대신 본인이 선택한 경로를 적으세요.

```bash
export TOOLS_DIR=$HOME/q-e/XSpectra/tools
```

Diamond 유사퍼텐셜은 저장소에 포함되어 있으므로 보통 설정하지 않아도 됩니다. 그래도 QE source tree의 원본 예제 유사퍼텐셜을 쓰고 싶다면 다음을 추가하세요.

```bash
export EXAMPLE_PSEUDO_DIR=$HOME/q-e/XSpectra/examples/pseudo
```

설정 뒤에는 항상 확인합니다.

```bash
source env.sh
./check_setup.sh
```

## 주의: QE 전체 source를 이 튜토리얼 repo 안에 넣지 마세요

`q-e/` 전체 repository는 큽니다. 이 튜토리얼 저장소 안에 `q-e/`를 clone하거나 commit하지 마세요. 필요하면 홈 디렉터리(`~/q-e`)나 강사가 제공한 공용 경로를 사용하세요.
