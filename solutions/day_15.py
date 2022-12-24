import pathlib


class SetOfSegments:
    segments: set[(int, int)]

    def __init__(self):
        self.segments = set()

    @staticmethod
    def _are_touching(a: (int, int), b: (int, int)) -> bool:
        return b[0] <= a[1] and a[0] <= b[1]

    @staticmethod
    def _merge(a: (int, int), b: (int, int)) -> (int, int):
        assert SetOfSegments._are_touching(a, b)
        return min(a[0], b[0]), max(a[1], b[1])

    def _check_invariant(self):
        for a in self.segments:
            for b in self.segments:
                if a == b:
                    continue
                assert not SetOfSegments._are_touching(a, b)

    def add(self, segment: (int, int)):
        assert segment[0] <= segment[1]
        to_delete = []
        for some_segment in self.segments:
            if SetOfSegments._are_touching(some_segment, segment):
                segment = SetOfSegments._merge(some_segment, segment)
                to_delete.append(some_segment)
        for x in to_delete:
            self.segments.remove(x)
        self.segments.add(segment)


def parse(text: str) -> [(int, int), (int, int)]:
    detections = []
    for line in text.splitlines():
        parts = line.split()
        sensor = (
            int(parts[2][2:-1]),
            int(parts[3][2:-1]),
        )
        beacon = (
            int(parts[8][2:-1]),
            int(parts[9][2:]),
        )
        detections.append((sensor, beacon))
    return detections


def distance(a: (int, int), b: (int, int)) -> int:
    """Calculate manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part1(text: str, y: int = 2_000_000):
    detections = parse(text)
    segments = SetOfSegments()
    for sensor, beacon in detections:
        radius = distance(sensor, beacon) - abs(sensor[1] - y)
        left = sensor[0] - radius
        right = sensor[0] + radius + 1
        if left < right:
            segments.add((left, right))
    beacons = set(beacon for _, beacon in detections if beacon[1] == y)
    return sum(b - a for a, b in segments.segments) - len(beacons)


def part2(text: str, limit: int = 4_000_000):
    limit += 1
    detections = parse(text)
    result = None
    for y in range(0, limit):
        segments = SetOfSegments()
        for sensor, beacon in detections:
            radius = distance(sensor, beacon) - abs(sensor[1] - y)
            left = max(0, sensor[0] - radius)
            right = min(limit, sensor[0] + radius + 1)
            if left <= right:
                segments.add((left, right))
        if len(segments.segments) == 1:
            continue
        assert len(segments.segments) == 2
        segments = list(segments.segments)
        segments.sort(key=lambda x: x[0])
        result = (segments[0][1], y)
        break
    return result[0] * 4_000_000 + result[1]


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text, 10) == 26
    assert part1(real_text) == 5607466
    assert part2(test_text, 20) == 56000011
    assert part2(real_text) == 12543202766584
