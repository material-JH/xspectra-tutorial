# Quantum ESPRESSO 입력 파일 기초

QE 입력 파일은 일반 텍스트 파일입니다. 입력 파일은 namelist와 card로 구성됩니다.

## Namelist(네임리스트)

예시:

```fortran
&control
   calculation='scf',
   prefix='SrTiO3_OK',
   outdir='./tmp/',
   pseudo_dir='../pseudo/',
/
```

자주 보는 namelist는 다음과 같습니다.

- `&control`: 어떤 계산을 실행할지, 파일을 어디에 저장할지 정합니다.
- `&system`: 결정 구조, cutoff, band 수, occupation 등을 정합니다.
- `&electrons`: SCF 수렴 조건을 정합니다.

## Card(카드)

예시:

```fortran
ATOMIC_SPECIES
Sr  87.62   Sr.pbe-spn-kjpaw_psl.1.0.0.UPF
Ti  47.867  Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
Oh  15.999  O.pbe-n-kjpaw_psl.0.1.UPF
O   15.999  O.pbe-n-kjpaw_psl.0.1.UPF
```

중요한 card는 다음과 같습니다.

- `ATOMIC_SPECIES`: 원자 레이블, 질량, 유사퍼텐셜 파일을 지정합니다.
- `ATOMIC_POSITIONS`: 원자 레이블과 좌표를 지정합니다.
- `K_POINTS`: Brillouin zone sampling을 지정합니다.

## 학습자가 알아두어야 할 주요 변수

- `nat`: 원자 수.
- `ntyp`: 원자 종(species) 레이블 수.
- `ecutwfc`: 파동함수에 대한 plane-wave cutoff.
- `ecutrho`: 전하 밀도 cutoff. PAW/USPP에서 특히 중요합니다.
- `nbnd`: band 수. XSpectra 계산에는 충분한 비점유 상태가 필요합니다.
- `prefix`: QE가 저장 파일에 사용하는 이름.
- `outdir`: 임시 계산 파일이 저장되는 디렉터리.
- `pseudo_dir`: UPF 유사퍼텐셜이 들어 있는 디렉터리.

## 흡수 원자 레이블

XSpectra는 흡수 원자를 원자 번호가 아니라 species index로 구분합니다. 그래서 흡수 원자에는 `Oh`, `Tih`, `C_h`처럼 별도의 레이블을 주는 경우가 많습니다.

SrTiO3 O K-edge 예시:

```fortran
ATOMIC_SPECIES
Sr  ...
Ti  ...
Oh  ...   ! 흡수 원자, species 3
O   ...   ! 나머지 산소, species 4
```

그러면 XSpectra 입력에서는 다음처럼 씁니다.

```fortran
xiabs=3
```

이 부분은 XSpectra를 처음 실행할 때 가장 흔히 틀리는 지점 중 하나입니다.
