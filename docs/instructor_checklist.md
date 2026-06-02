# 강사용 체크리스트

튜토리얼 세션 전 확인할 일:

- 모든 학생이 클러스터 계정을 가지고 있고 로그인할 수 있는지 확인합니다.
- QE module에 `pw.x`, `xspectra.x`, `ld1.x`가 포함되어 있는지 확인합니다.
- 새 계정에서 `$HOME/q-e`가 준비되는지 확인합니다. `git clone --depth 1 --branch develop https://github.com/QEF/q-e.git ~/q-e`로 받은 QE source tree의 `XSpectra/tools/` 경로를 `TOOLS_DIR`로 사용합니다.
- Diamond Carbon 유사퍼텐셜은 `diamond/pseudo/`에 포함되어 있으므로 별도 배포가 필요 없는지 확인합니다.
- 로컬 클러스터에 맞는 `env.sh`를 준비합니다.
- 새로 clone한 저장소에서 `./check_setup.sh`를 실행합니다.
- Diamond Slurm/PBS 테스트 작업을 제출해 봅니다.
- SrTiO3 테스트 작업을 최소 하나 제출해 봅니다.
- Python plotting이 작동하는지 확인하거나 미리 생성한 plot을 준비합니다.
- 학생들이 core-hole 및 supercell 작업을 실시간으로 실행할지, reference output을 볼지 결정합니다.
- 큐가 느릴 경우를 대비해 fallback output 파일을 준비합니다.
- 학생들에게 큰 MPI 작업을 로그인 노드에서 실행하지 말라고 안내합니다.
- 튜토리얼 소개를 위해 `docs/xspectra_tutorial_presentation.html`을 로컬 브라우저에서 열어 둡니다.

세션 중 진행 순서:

1. Diamond부터 시작합니다.
2. EELS와 가장 관련 있는 주요 예제로 SrTiO3 O K-edge를 사용합니다.
3. O K-edge에서 no-hole, FCH, HCH 차이를 비교합니다.
4. 작업이 아직 큐에 있으면 reference output을 보여 줍니다.
5. Supercell과 benchmarking은 고급 내용으로 남겨 둡니다.
