from pathlib import Path
from typing import List, Iterator


class EntityLoader:
    @staticmethod
    def _find_entity_files(
        directory: Path, pattern: str = "*.entity.py"
    ) -> Iterator[Path]:
        """재귀적으로 엔티티 파일을 찾습니다."""
        for path in directory.rglob(pattern):
            if path.is_file():
                yield path

    @staticmethod
    def load(pattern: str = "**/*.entity.py") -> List[str]:
        """
        엔티티 파일들을 패턴에 맞게 검색하여 모듈 경로 리스트를 반환합니다.

        :param pattern: 검색할 패턴 (예: "**/*.entity.py")
        :return: 모듈 경로 리스트

        예시:
        >>> EntityLoader.load()
        ['users.user.entity', 'auth.token.entity']
        """
        base_path = Path(__file__).parent.parent.parent  # database 폴더의 상위 디렉토리
        pattern = pattern.lstrip("/")

        # pattern에서 파일 패턴과 디렉토리 패턴을 분리
        parts = pattern.split("/")
        file_pattern = parts[-1]
        dir_pattern = "/".join(parts[:-1]) if len(parts) > 1 else ""

        # 시작 디렉토리 설정
        start_dir = base_path
        if dir_pattern:
            start_dir = base_path / dir_pattern

        # 엔티티 파일 검색
        entities = []
        for file_path in EntityLoader._find_entity_files(start_dir, file_pattern):
            try:
                # base_path에 대한 상대 경로 계산
                relative_path = file_path.relative_to(base_path)
                # 모듈 경로 형식으로 변환 (예: auth.entities.user)
                module_path = str(relative_path.parent / relative_path.stem).replace(
                    "/", "."
                )
                entities.append(module_path)
            except ValueError:
                continue  # base_path 외부의 파일은 무시

        return sorted(entities)  # 일관된 순서를 위해 정렬
