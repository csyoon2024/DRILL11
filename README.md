# DRILL11

`pico2d` 기반 소년 캐릭터 컨트롤러입니다. `IDLE`에서 `A`를 누르면 5초 동안 빠르고 크게 좌우로 자동 이동하는 `AUTO_RUN` 상태가 시작됩니다.

## 실행

1. Python 3 환경을 준비하고 프로젝트 의존성을 설치합니다.

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. `pico2d`가 설치된 2DGP 수업 환경에서 저장소 루트에서 실행합니다.

   ```powershell
   python main.py
   ```

## 조작

- `A`: `IDLE` 상태에서 자동 무적 런 시작
- `←` / `→`: 수동 런. 자동 런 중 누르면 해당 방향의 일반 런으로 전환
- `Space`: 수면 상태에서 기상
- `Esc`: 종료

## 상태 동작

- `IDLE`에서 5초간 입력이 없으면 기존 동작대로 `SLEEP` 상태가 됩니다.
- `AUTO_RUN`은 입력 없이 좌우로 왕복하고, 5초 후 `IDLE`로 돌아갑니다.
- 자동 런은 화면 안쪽 경계에서 방향을 바꾸며, 일반 런보다 빠르고 큰 크기로 표시됩니다.
- 캐릭터 상태 로직은 `boy.py`에 있으며, 자동 런의 이동/시간 동작은 별도의 `AutoRun` 클래스가 담당합니다.

실행 이미지(`animation_sheet.png`, `grass.png`)는 저장소 루트에 포함되어 있습니다.

## 테스트

자동 런의 시작, 2배 이동 속도, 화면 경계 반전, 5초 종료, 방향키 취소 및 확대 렌더링을 확인하려면 다음 명령을 실행합니다.

```powershell
python -m unittest discover -s tests -v
```
