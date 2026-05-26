# Diamond C K-edge 실습

Diamond는 구조가 작고 계산이 빨리 끝나기 때문에 첫 번째 실습 예제로 사용합니다.

## 이 실습에서 배우는 것

- 기본 XSpectra 작업 흐름.
- `C_h`를 이용한 흡수 원자 레이블 지정.
- No-core-hole 스펙트럼과 full-core-hole 스펙트럼 비교.
- `xonly_plot`을 이용한 다시 그리기.
- `cut_occ_states`로 점유 상태 artifact 제거하기.

## 실행

계산 노드에서 또는 스케줄러를 통해 실행합니다.

```bash
bash run_all_examples.sh diamond-only
python3 plot_spectra.py
```

공개 튜토리얼 스크립트에서는 Diamond를 짧은 첫 실습으로 유지합니다. SrTiO3 예제는 뒤의 수업에서 따로 실행하거나 `bash run_all_examples.sh srtio3`로 실행합니다.

## 파일

`bash run_all_examples.sh diamond-only`를 실행하면 기본적으로 저장소에 포함된 `diamond/pseudo/`의 Carbon 유사퍼텐셜을 사용합니다. `env.sh`에서 `EXAMPLE_PSEUDO_DIR`를 따로 지정하면 그 값으로 `diamond/*.in` 파일의 `pseudo_dir`가 다시 작성됩니다. 따라서 학생이 `/path/to/q-e` 같은 경로를 직접 입력할 필요가 없습니다.

- `diamond/diamond.scf.in`
- `diamond/diamond.xspectra.in`
- `diamond/diamond.xspectra_replot.in`
- `diamond/diamondh.scf.in`
- `diamond/diamondh.xspectra.in`

## 출력 확인

```bash
ls diamond/*.dat
grep "WALL" diamond/*.out
```

예상 스펙트럼은 다음 위치에 있습니다.

```text
reference_output/diamond/
```
