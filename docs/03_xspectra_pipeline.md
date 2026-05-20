# XSpectra 계산 흐름

모든 계산은 같은 3단계 흐름을 따릅니다.

## 1단계: 코어 파동함수 추출

```bash
$TOOLS_DIR/upf2plotcore.sh O.pbe-n-kjpaw_psl.0.1.UPF > O.wfc
```

이 명령은 XSpectra가 사용할 초기 코어 오비탈을 만듭니다.

중요: FCH/HCH 계산에서도 `filecore`는 원래의 non-core-hole 유사퍼텐셜에서 추출합니다.

## 2단계: `pw.x`로 SCF 계산 실행

```bash
pw.x < scf.in > scf.out
```

SCF 계산은 `outdir`에 전하 밀도와 파동함수 데이터를 만듭니다.

## 3단계: `xspectra.x` 실행

```bash
xspectra.x < xspectra.in > xspectra.out
```

출력 스펙트럼은 `xanes.dat`로 저장되고, 스크립트가 이를 더 설명적인 파일 이름으로 바꿉니다.

## 주요 XSpectra 변수

- `calculation='xanes_dipole'`: 전기 쌍극자 전이.
- `edge='K'`, `edge='L2'`, 또는 `edge='L3'`: 선택한 edge.
- `xepsilon(1:3)`: 편광 방향.
- `xiabs`: 흡수 원자의 species index.
- `filecore`: 추출한 코어 파동함수 파일.
- `xgamma`: eV 단위 Lorentzian broadening.
- `xemin`, `xemax`: 그림으로 볼 에너지 범위.
- `cut_occ_states`: edge 아래의 점유 상태 artifact를 제거합니다.
- `xonly_plot`: 비싼 계산을 다시 하지 않고 저장된 Lanczos 파일에서 다시 plot합니다.

## 흐름도

```text
UPF 유사퍼텐셜
   │
   ├── upf2plotcore.sh → O.wfc / Ti.wfc / C.wfc
   │
SCF 입력 → pw.x → tmp/ 안의 전하 밀도
   │
XSpectra 입력 + 코어 파동함수 → xspectra.x → xanes.dat
```
