import itertools
from dataclasses import dataclass, field
from itertools import permutations
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from z3 import Int, Solver

from utils import aoc_input
from utils.geo import Point3D
from utils.out import debug

TEST_DATA = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


@dataclass(eq=True, frozen=True)
class Beacon:
    location: Point3D
    name: str = field(default='', hash=False, compare=False)


@dataclass(eq=True, frozen=True)
class Scanner:
    beacons: Set[Beacon]
    name: str


def distance(a: Point3D, b: Point3D) -> int:
    return (a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    nb_total_beacons: int = 0

    current_scanner_num: str = ''
    current_beacon_id: int = 0
    scanners: List[Scanner] = []
    beacons: Set[Beacon] = set()
    for line in input_data.strip().split('\n'):
        if not line:
            continue

        if line.startswith('---'):
            if beacons:
                scanners.append(Scanner(beacons, name=current_scanner_num))

            _, _, current_scanner_num, _ = line.strip().split(' ')
            beacons = set()
            continue

        x, y, z = map(int, line.strip().split(','))
        beacons.add(Beacon(location=Point3D(x, y, z), name=f's{current_scanner_num}b{str(current_beacon_id)}'))
        nb_total_beacons += 1
        current_beacon_id += 1

    scanners.append(Scanner(beacons, name=current_scanner_num))

    scanner_located: Set[str] = set([scanners[0].name])

    scanner_0_locations: List[Optional[Point3D]] = [None] * len(scanners)
    scanner_0_locations[0] = Point3D(0, 0, 0)

    scanner_rel_locations: Dict[str, List[Optional[Tuple[int, int, int, int, int, int, int, int, int, int, int,
                                                         int]]]] = {}
    for scanner in scanners:
        scanner_rel_locations[scanner.name] = [None] * len(scanners)

    while len(scanner_located) != len(scanners):
        for from_idx, to_idx in itertools.permutations(range(0, len(scanners)), 2):
            from_scanner = scanners[from_idx]
            to_scanner = scanners[to_idx]

            if from_idx == 0 or from_scanner.name not in scanner_located:
                if to_scanner.name not in scanner_located:
                    consolidated, a, b, c, d, e, f, g, h, i, x, y, z = consolidate(from_scanner, to_scanner)
                    if consolidated:
                        scanner_located.add(to_scanner.name)
                        scanner_rel_locations[to_scanner.name][from_idx] = (a, b, c, d, e, f, g, h, i, x, y, z)

    print(len(scanners[0].beacons))

    # Part2
    while not all(scanner_0_locations):
        for idx, scanner in enumerate(scanners):
            if scanner_0_locations[idx]:
                continue

            for loc_idx, location in enumerate(scanner_rel_locations[scanner.name]):
                if location is None:
                    continue

                if loc_idx == 0:
                    if location:
                        break

                other_scanner_0_location = scanner_0_locations[loc_idx]
                other_scanner_transform = scanner_rel_locations[scanners[loc_idx].name][0]
                if other_scanner_0_location is not None:
                    scanner_rel_locations[scanner.name][0] = (
                        1,
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1,
                        location[-3] * other_scanner_transform[0] + location[-2] * other_scanner_transform[1] +
                        location[-1] * other_scanner_transform[2] + other_scanner_0_location.x,
                        location[-3] * other_scanner_transform[3] + location[-2] * other_scanner_transform[4] +
                        location[-1] * other_scanner_transform[5] + other_scanner_0_location.y,
                        location[-3] * other_scanner_transform[6] + location[-2] * other_scanner_transform[7] +
                        location[-1] * other_scanner_transform[8] + other_scanner_0_location.z,
                    )

            if scanner_rel_locations[scanner.name][0]:
                scanner_0_locations[idx] = Point3D(
                    scanner_rel_locations[scanner.name][0][-3],
                    scanner_rel_locations[scanner.name][0][-2],
                    scanner_rel_locations[scanner.name][0][-1],
                )

    # print(scanner_rel_locations)
    # for loc in scanner_0_locations:
    #     print(loc)

    print('')
    print(len(scanners))
    print(len(scanner_0_locations))

    i = 0
    max_manhattan = 0
    for from_idx, to_idx in itertools.combinations(range(0, len(scanners)), 2):
        loc1 = scanner_0_locations[from_idx]
        loc2 = scanner_0_locations[to_idx]
        manhattan = abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y) + abs(loc1.z - loc2.z)
        # print(from_idx, 'to', to_idx, '=', manhattan)
        if manhattan > max_manhattan:
            max_manhattan = manhattan

        i += 1

    print('13', scanner_rel_locations['13'])
    print('15', scanner_rel_locations['15'])
    print('13', scanner_0_locations[13])
    print('15', scanner_0_locations[15])

    print(i)
    print('should be more than 12178')
    print(max_manhattan)


def consolidate(from_scanner: Scanner,
                to_scanner: Scanner) -> Tuple[bool, int, int, int, int, int, int, int, int, int, int, int, int]:
    """
    Try to match from_scanner and to_scanner. If possible, will copy all the to_scanner beacons into from_scanner
    """
    a = None
    b = None
    c = None
    d = None
    e = None
    f = None
    g = None
    h = None
    i = None
    x = None
    y = None
    z = None
    found = False
    dist_per_scanner: Dict[str, Dict[Beacon, Set[int]]] = {}
    for scanner in [from_scanner, to_scanner]:
        dist_per_beacon: Dict[Beacon, Set[int]] = {}
        dist_per_scanner[scanner.name] = dist_per_beacon
        for beacon_a, beacon_b in itertools.combinations(scanner.beacons, 2):
            dist = distance(beacon_a.location, beacon_b.location)
            if dist_per_beacon.get(beacon_a) is None:
                dist_per_beacon[beacon_a] = set()
            if dist_per_beacon.get(beacon_b) is None:
                dist_per_beacon[beacon_b] = set()

            dist_per_beacon[beacon_a].add(dist)
            dist_per_beacon[beacon_b].add(dist)

    samesies: Set[Tuple[Beacon, Beacon]] = set()
    for from_beacon in from_scanner.beacons:
        for to_beacon in to_scanner.beacons:
            common_dist = dist_per_scanner[from_scanner.name][from_beacon] & dist_per_scanner[
                to_scanner.name][to_beacon]
            if len(common_dist) >= 11:
                samesies.add((from_beacon, to_beacon))

    list_samesies = list(samesies)
    if list_samesies:
        found = True

        a, b, c, d, e, f, g, h, i, x, y, z = find_scanner_coords(
            list_samesies[0][0].location,
            list_samesies[0][1].location,
            list_samesies[1][0].location,
            list_samesies[1][1].location,
            list_samesies[2][0].location,
            list_samesies[2][1].location,
            list_samesies[3][0].location,
            list_samesies[3][1].location,
            list_samesies[4][0].location,
            list_samesies[4][1].location,
            list_samesies[5][0].location,
            list_samesies[5][1].location,
        )
        # print(a, b, c, d, e, f, g, h, i, x, y, z)

        for beacon in to_scanner.beacons:
            from_scanner.beacons.add(
                Beacon(
                    Point3D(
                        a.as_long() * beacon.location.x + b.as_long() * beacon.location.y +
                        c.as_long() * beacon.location.z + x.as_long(),
                        d.as_long() * beacon.location.x + e.as_long() * beacon.location.y +
                        f.as_long() * beacon.location.z + y.as_long(),
                        g.as_long() * beacon.location.x + h.as_long() * beacon.location.y +
                        i.as_long() * beacon.location.z + z.as_long(),
                    ),
                    name=beacon.name,
                ))

    return (
        found,
        a.as_long() if a is not None else 0,
        b.as_long() if b is not None else 0,
        c.as_long() if c is not None else 0,
        d.as_long() if d is not None else 0,
        e.as_long() if e is not None else 0,
        f.as_long() if f is not None else 0,
        g.as_long() if g is not None else 0,
        h.as_long() if h is not None else 0,
        i.as_long() if i is not None else 0,
        x.as_long() if x is not None else 0,
        y.as_long() if y is not None else 0,
        z.as_long() if z is not None else 0,
    )


def find_scanner_coords(point1_ref: Point3D, point1_scanner: Point3D, point2_ref: Point3D, point2_scanner: Point3D,
                        point3_ref: Point3D, point3_scanner: Point3D, point4_ref: Point3D, point4_scanner: Point3D,
                        point5_ref: Point3D, point5_scanner: Point3D, point6_ref: Point3D,
                        point6_scanner: Point3D) -> Tuple[int, int, int, int, int, int, int, int, int, int, int, int]:
    """
    Returns a, b, c, d, e, f, g, h, i, xs, ys, zs such that:

    - The scanner origin is at (xs, ys, zs)
    - To get the X reference coord of a beacon from its scanner coordinates (x,y,z), you do ax + by + cz
    - To get the Y reference coord of a beacon from its scanner coordinates (x,y,z), you do dx + ey + fz
    - To get the Z reference coord of a beacon from its scanner coordinates (x,y,z), you do gx + hy + iz
    """
    a = Int('a')
    b = Int('b')
    c = Int('c')
    d = Int('d')
    e = Int('e')
    f = Int('f')
    g = Int('g')
    h = Int('h')
    i = Int('i')
    xs = Int('xs')
    ys = Int('ys')
    zs = Int('zs')

    z3_solver = Solver()
    z3_solver.add(a >= -1)
    z3_solver.add(a <= 1)
    z3_solver.add(b >= -1)
    z3_solver.add(b <= 1)
    z3_solver.add(c >= -1)
    z3_solver.add(c <= 1)
    z3_solver.add(d >= -1)
    z3_solver.add(d <= 1)
    z3_solver.add(e >= -1)
    z3_solver.add(e <= 1)
    z3_solver.add(f >= -1)
    z3_solver.add(f <= 1)
    z3_solver.add(g >= -1)
    z3_solver.add(g <= 1)
    z3_solver.add(h >= -1)
    z3_solver.add(h <= 1)
    z3_solver.add(i >= -1)
    z3_solver.add(i <= 1)

    z3_solver.add(point1_scanner.x * a + point1_scanner.y * b + point1_scanner.z * c + xs == point1_ref.x)
    z3_solver.add(point2_scanner.x * a + point2_scanner.y * b + point2_scanner.z * c + xs == point2_ref.x)
    z3_solver.add(point3_scanner.x * a + point3_scanner.y * b + point3_scanner.z * c + xs == point3_ref.x)
    z3_solver.add(point4_scanner.x * a + point4_scanner.y * b + point4_scanner.z * c + xs == point4_ref.x)
    z3_solver.add(point5_scanner.x * a + point5_scanner.y * b + point5_scanner.z * c + xs == point5_ref.x)
    z3_solver.add(point6_scanner.x * a + point6_scanner.y * b + point6_scanner.z * c + xs == point6_ref.x)

    z3_solver.add(point1_scanner.x * d + point1_scanner.y * e + point1_scanner.z * f + ys == point1_ref.y)
    z3_solver.add(point2_scanner.x * d + point2_scanner.y * e + point2_scanner.z * f + ys == point2_ref.y)
    z3_solver.add(point3_scanner.x * d + point3_scanner.y * e + point3_scanner.z * f + ys == point3_ref.y)
    z3_solver.add(point4_scanner.x * d + point4_scanner.y * e + point4_scanner.z * f + ys == point4_ref.y)
    z3_solver.add(point5_scanner.x * d + point5_scanner.y * e + point5_scanner.z * f + ys == point5_ref.y)
    z3_solver.add(point6_scanner.x * d + point6_scanner.y * e + point6_scanner.z * f + ys == point6_ref.y)

    z3_solver.add(point1_scanner.x * g + point1_scanner.y * h + point1_scanner.z * i + zs == point1_ref.z)
    z3_solver.add(point2_scanner.x * g + point2_scanner.y * h + point2_scanner.z * i + zs == point2_ref.z)
    z3_solver.add(point3_scanner.x * g + point3_scanner.y * h + point3_scanner.z * i + zs == point3_ref.z)
    z3_solver.add(point4_scanner.x * g + point4_scanner.y * h + point4_scanner.z * i + zs == point4_ref.z)
    z3_solver.add(point5_scanner.x * g + point5_scanner.y * h + point5_scanner.z * i + zs == point5_ref.z)
    z3_solver.add(point6_scanner.x * g + point6_scanner.y * h + point6_scanner.z * i + zs == point6_ref.z)

    z3_solver.check()

    return (
        z3_solver.model()[a],
        z3_solver.model()[b],
        z3_solver.model()[c],
        z3_solver.model()[d],
        z3_solver.model()[e],
        z3_solver.model()[f],
        z3_solver.model()[g],
        z3_solver.model()[h],
        z3_solver.model()[i],
        z3_solver.model()[xs],
        z3_solver.model()[ys],
        z3_solver.model()[zs],
    )


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()


def main(day_num: int, part_num: int, with_test_data=True) -> None:
    input_file = None
    if not with_test_data:
        input_file = aoc_input.get_input(day_num)

    if part_num == 1:
        main_part_1(input_file)
    elif part_num == 2:
        main_part_2(input_file)
    else:
        raise ValueError(f"Invalid part number {part_num}")
