"""Small standard-library mesh helpers for Phase 3 placeholder geometry."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Mesh = Dict[str, List[List[float]]]


def sanitize_filename(name: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(name).strip()).strip("_")
    return clean or "unnamed"


def create_box(width: float, depth: float, height: float, origin: Tuple[float, float, float] = (0, 0, 0)) -> Mesh:
    x, y, z = origin
    w, d, h = float(width), float(depth), float(height)
    vertices = [
        [x, y, z], [x + w, y, z], [x + w, y + d, z], [x, y + d, z],
        [x, y, z + h], [x + w, y, z + h], [x + w, y + d, z + h], [x, y + d, z + h],
    ]
    faces = [
        [0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6],
        [0, 4, 5], [0, 5, 1], [1, 5, 6], [1, 6, 2],
        [2, 6, 7], [2, 7, 3], [3, 7, 4], [3, 4, 0],
    ]
    return {"vertices": vertices, "faces": faces}


def create_rectangular_frame(width: float, height: float, frame_width: float, depth: float) -> Mesh:
    fw = min(float(frame_width), float(width) / 3, float(height) / 3)
    w, h, d = float(width), float(height), float(depth)
    return merge_meshes([
        create_box(w + 2 * fw, d, fw, (-fw, 0, -fw)),
        create_box(w + 2 * fw, d, fw, (-fw, 0, h)),
        create_box(fw, d, h, (-fw, 0, 0)),
        create_box(fw, d, h, (w, 0, 0)),
    ])


def create_cylinder(radius: float, height: float, segments: int = 24) -> Mesh:
    r, h = float(radius), float(height)
    segments = max(8, int(segments))
    vertices: List[List[float]] = []
    for z in (0.0, h):
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            vertices.append([r * math.cos(angle), r * math.sin(angle), z])
    bottom_center = len(vertices); vertices.append([0, 0, 0])
    top_center = len(vertices); vertices.append([0, 0, h])
    faces: List[List[int]] = []
    for i in range(segments):
        j = (i + 1) % segments
        faces.append([i, j, segments + j]); faces.append([i, segments + j, segments + i])
        faces.append([bottom_center, j, i]); faces.append([top_center, segments + i, segments + j])
    return {"vertices": vertices, "faces": faces}


def create_pipe(outer_diameter: float, inner_diameter: float, length: float, segments: int = 24) -> Mesh:
    outer_r = float(outer_diameter) / 2
    inner_r = max(0.0, min(float(inner_diameter) / 2, outer_r * 0.95))
    if inner_r <= 0:
        return create_cylinder(outer_r, length, segments)
    segments = max(8, int(segments))
    vertices: List[List[float]] = []
    for z in (0.0, float(length)):
        for r in (outer_r, inner_r):
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                vertices.append([r * math.cos(angle), r * math.sin(angle), z])
    faces: List[List[int]] = []
    ob, ib, ot, it = 0, segments, 2 * segments, 3 * segments
    for i in range(segments):
        j = (i + 1) % segments
        faces += [[ob+i, ob+j, ot+j], [ob+i, ot+j, ot+i]]
        faces += [[ib+j, ib+i, it+i], [ib+j, it+i, it+j]]
        faces += [[ot+i, ot+j, it+j], [ot+i, it+j, it+i]]
        faces += [[ob+j, ob+i, ib+i], [ob+j, ib+i, ib+j]]
    return {"vertices": vertices, "faces": faces}


def create_rectangular_duct(width: float, height: float, length: float, wall_thickness: float) -> Mesh:
    # Phase 3 placeholder: use a solid bounding duct and record wall thickness in metadata upstream.
    return create_box(float(length), float(width), float(height), (0, 0, 0))


def merge_meshes(meshes: Iterable[Mesh]) -> Mesh:
    vertices: List[List[float]] = []
    faces: List[List[int]] = []
    offset = 0
    for mesh in meshes:
        mesh_vertices = mesh.get("vertices", [])
        vertices.extend(mesh_vertices)
        faces.extend([[int(index) + offset for index in face] for face in mesh.get("faces", [])])
        offset += len(mesh_vertices)
    return {"vertices": vertices, "faces": faces}


def compute_bounding_box(mesh: Mesh) -> Dict[str, List[float]]:
    vertices = mesh.get("vertices", [])
    if not vertices:
        return {"min": [0, 0, 0], "max": [0, 0, 0]}
    return {"min": [min(v[i] for v in vertices) for i in range(3)], "max": [max(v[i] for v in vertices) for i in range(3)]}


def _normal(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> List[float]:
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = c[0]-a[0], c[1]-a[1], c[2]-a[2]
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    length = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
    return [nx/length, ny/length, nz/length]


def write_obj(mesh: Mesh, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Phase 3 placeholder OBJ"]
    lines += [f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}" for v in mesh.get("vertices", [])]
    lines += ["f " + " ".join(str(i + 1) for i in face) for face in mesh.get("faces", [])]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ascii_stl(mesh: Mesh, path: Path, solid_name: str = "phase3_placeholder") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    vertices = mesh.get("vertices", [])
    lines = [f"solid {sanitize_filename(solid_name)}"]
    for face in mesh.get("faces", []):
        if len(face) < 3:
            continue
        a, b, c = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        n = _normal(a, b, c)
        lines.append(f"  facet normal {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}")
        lines.append("    outer loop")
        for vertex in (a, b, c):
            lines.append(f"      vertex {vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {sanitize_filename(solid_name)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_geometry_json(mesh: Mesh, metadata: Dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = dict(metadata)
    data["vertices"] = mesh.get("vertices", [])
    data["faces"] = mesh.get("faces", [])
    data.setdefault("metadata", {})["boundingBox"] = compute_bounding_box(mesh)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
