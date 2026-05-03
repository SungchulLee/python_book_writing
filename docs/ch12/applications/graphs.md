# Graph Algorithms

Sparse matrices for graph representation and analysis.

!!! tip "Mental Model"
    A graph's adjacency matrix is naturally sparse -- most nodes connect to only a few neighbors, so the matrix is almost entirely zeros. By storing this matrix in a sparse format, you can run graph algorithms like shortest paths and connected components at a fraction of the memory and time cost of dense representations.

## Adjacency Matrix

```python
import numpy as np
from scipy import sparse

def main():
    # Graph edges: (from, to)
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    n_nodes = 4
    
    row = [e[0] for e in edges]
    col = [e[1] for e in edges]
    data = np.ones(len(edges))
    
    # Undirected: symmetrize
    A = sparse.csr_matrix((data, (row, col)), shape=(n_nodes, n_nodes))
    A = A + A.T
    
    print("Adjacency matrix:")
    print(A.toarray())

if __name__ == "__main__":
    main()
```

## Graph Laplacian

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    A = sparse.csr_matrix([[0, 1, 1, 0],
                           [1, 0, 1, 0],
                           [1, 1, 0, 1],
                           [0, 0, 1, 0]])
    
    # Degree matrix
    D = sparse.diags(np.array(A.sum(axis=1)).flatten())
    
    # Laplacian
    L = D - A
    
    # Smallest eigenvalues (connectivity)
    vals, vecs = splinalg.eigsh(L.astype(float), k=2, which='SM')
    print(f"Smallest eigenvalues: {vals}")

if __name__ == "__main__":
    main()
```

Graph connected iff second smallest Laplacian eigenvalue > 0.

---

## Runnable Example: `delaunay_triangulation.py`

```python
"""
Delaunay Triangulation and Spatial Data Structures - A Practical Guide
Exploring scipy.spatial.Delaunay, ConvexHull, Voronoi concepts, and their
applications in computational geometry. Run this file to learn spatial structures!
"""

import numpy as np
from scipy import spatial

if __name__ == "__main__":

    print("=" * 70)
    print("DELAUNAY TRIANGULATION AND SPATIAL DATA STRUCTURES")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Basic Delaunay Triangulation in 2D
    # ============================================================================
    print("\n1. BASIC DELAUNAY TRIANGULATION IN 2D")
    print("-" * 70)

    # Create a set of 2D points
    np.random.seed(42)
    points_2d = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
        [0.5, 0.5],
    ])

    print("Points for triangulation:")
    for i, point in enumerate(points_2d):
        print(f"  Point {i}: {point}")

    # Compute Delaunay triangulation
    delaunay_2d = spatial.Delaunay(points_2d)

    print("\nDelaunay triangulation computed!")
    print(f"Number of simplices (triangles): {len(delaunay_2d.simplices)}")
    print(f"Each simplex is a triangle with 3 vertex indices\n")

    # Display triangles
    print("Triangles (simplices):")
    for i, triangle in enumerate(delaunay_2d.simplices):
        v0, v1, v2 = triangle
        p0, p1, p2 = points_2d[v0], points_2d[v1], points_2d[v2]
        print(f"  Triangle {i}: vertices {triangle}")
        print(f"    Coordinates: {p0}, {p1}, {p2}")

    # ============================================================================
    # EXAMPLE 2: Accessing Delaunay Data Structures
    # ============================================================================
    print("\n2. ACCESSING DELAUNAY STRUCTURE INFORMATION")
    print("-" * 70)

    # simplices: array of vertex indices for each triangle
    simplices = delaunay_2d.simplices
    print(f"Simplices shape: {simplices.shape}")
    print(f"(rows=triangles, cols=vertices per triangle)")
    print(f"Simplices:\n{simplices}")

    # points: the original input points
    print(f"\nInput points shape: {delaunay_2d.points.shape}")
    print(f"Points stored in triangulation:\n{delaunay_2d.points}")

    # neighbors: for each simplex, which neighboring simplices share edges
    neighbors = delaunay_2d.neighbors
    print(f"\nNeighbors array shape: {neighbors.shape}")
    print(f"neighbors[i, j] = simplex index sharing edge j of triangle i")
    print(f"(value -1 means no neighbor, edge is on convex hull)")
    print(f"Neighbors:\n{neighbors}")

    # vertices: same as simplices (alternative name)
    print(f"\nVertices shape: {delaunay_2d.vertices.shape}")

    # ============================================================================
    # EXAMPLE 3: Understanding the Empty Circumcircle Property
    # ============================================================================
    print("\n3. DELAUNAY PROPERTY: EMPTY CIRCUMCIRCLE")
    print("-" * 70)

    print("The Delaunay triangulation has a key property:")
    print("The circumcircle of each triangle contains no other points.\n")

    def circumcircle(p0, p1, p2):
        """
        Compute center and radius of circumcircle for triangle.

        Parameters
        ----------
        p0, p1, p2 : array-like
            Vertices of the triangle (2D points)

        Returns
        -------
        center : ndarray
            Center of circumcircle
        radius : float
            Radius of circumcircle
        """
        # Convert to homogeneous coordinates for calculation
        ax, ay = p0
        bx, by = p1
        cx, cy = p2

        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

        if abs(d) < 1e-10:
            # Degenerate case
            return np.array([0, 0]), 0

        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d

        center = np.array([ux, uy])
        radius = np.linalg.norm(p0 - center)

        return center, radius

    # Check circumcircle property for first triangle
    triangle_0 = delaunay_2d.simplices[0]
    v0, v1, v2 = triangle_0
    p0, p1, p2 = points_2d[v0], points_2d[v1], points_2d[v2]

    center, radius = circumcircle(p0, p1, p2)
    print(f"First triangle vertices: {triangle_0}")
    print(f"  Coordinates: {p0}, {p1}, {p2}")
    print(f"  Circumcircle center: {center}")
    print(f"  Circumcircle radius: {radius:.6f}\n")

    # Check distances of all points to this circumcircle
    print("Distances from other points to circumcircle:")
    for i, point in enumerate(points_2d):
        dist_to_center = np.linalg.norm(point - center)
        if i not in triangle_0:
            status = "OUTSIDE" if dist_to_center > radius + 1e-6 else "INSIDE/ON"
            print(f"  Point {i}: distance to center = {dist_to_center:.6f}, {status}")

    # ============================================================================
    # EXAMPLE 4: Convex Hull - Boundary of Point Set
    # ============================================================================
    print("\n4. CONVEX HULL: BOUNDARY OF POINT SET")
    print("-" * 70)

    print("The convex hull is the smallest convex polygon containing all points.\n")

    # Compute convex hull
    hull = spatial.ConvexHull(points_2d)

    print(f"Convex hull computed!")
    print(f"Number of vertices on hull: {len(hull.vertices)}")
    print(f"Vertex indices: {hull.vertices}")

    # Hull points
    print(f"\nHull vertices (coordinates):")
    for idx in hull.vertices:
        print(f"  Point {idx}: {points_2d[idx]}")

    # Hull simplices (in 2D, these are edges)
    print(f"\nHull simplices (edges in 2D):")
    for i, edge in enumerate(hull.simplices):
        v0, v1 = edge
        p0, p1 = points_2d[v0], points_2d[v1]
        print(f"  Edge {i}: points {v0} -- {v1}")

    # Area and volume
    print(f"\nHull properties:")
    print(f"  Area: {hull.volume:.6f}")  # In 2D, 'volume' is actually area

    # ============================================================================
    # EXAMPLE 5: Finding Hull Edges from Delaunay Triangulation
    # ============================================================================
    print("\n5. IDENTIFYING BOUNDARY EDGES IN DELAUNAY")
    print("-" * 70)

    print("In Delaunay, boundary edges have neighbors = -1\n")

    boundary_edges = []
    for i, neighbor_row in enumerate(delaunay_2d.neighbors):
        for edge_idx, neighbor_simplex in enumerate(neighbor_row):
            if neighbor_simplex == -1:  # No neighbor = boundary edge
                # Find vertices of this edge
                # Each edge is opposite to a vertex
                edge_vertices = np.delete(delaunay_2d.simplices[i], edge_idx)
                boundary_edges.append(edge_vertices)

    print(f"Found {len(boundary_edges)} boundary edges:")
    for i, edge in enumerate(boundary_edges):
        v0, v1 = edge
        print(f"  Edge {i}: points {v0} -- {v1}, coordinates {points_2d[v0]} -- {points_2d[v1]}")

    # ============================================================================
    # EXAMPLE 6: Point Location in Triangulation
    # ============================================================================
    print("\n6. POINT LOCATION: FINDING WHICH TRIANGLE CONTAINS A POINT")
    print("-" * 70)

    print("Query: Which triangle contains a given point?\n")

    test_points = np.array([
        [0.5, 0.5],     # Inside the triangulation
        [2.0, 2.0],     # Outside
        [0.1, 0.1],     # Inside
    ])

    print("Test points and their containing triangles:")
    for test_point in test_points:
        simplex_idx = delaunay_2d.find_simplex(test_point)
        if simplex_idx >= 0:
            triangle = delaunay_2d.simplices[simplex_idx]
            print(f"  Point {test_point}: in triangle {simplex_idx}, vertices {triangle}")
        else:
            print(f"  Point {test_point}: OUTSIDE triangulation")

    # ============================================================================
    # EXAMPLE 7: 3D Delaunay Triangulation with Random Data
    # ============================================================================
    print("\n7. DELAUNAY TRIANGULATION IN 3D")
    print("-" * 70)

    print("Extend to 3D: triangles become tetrahedra!\n")

    # Generate random 3D points
    np.random.seed(42)
    points_3d = np.random.rand(20, 3)  # 20 random points in unit cube

    # Compute 3D Delaunay
    delaunay_3d = spatial.Delaunay(points_3d)

    print(f"3D Delaunay triangulation:")
    print(f"  Number of points: {delaunay_3d.points.shape[0]}")
    print(f"  Number of tetrahedra: {len(delaunay_3d.simplices)}")
    print(f"  Tetrahedron size: {delaunay_3d.simplices.shape[1]} vertices")

    # Show first few tetrahedra
    print(f"\nFirst 3 tetrahedra:")
    for i in range(min(3, len(delaunay_3d.simplices))):
        tet = delaunay_3d.simplices[i]
        print(f"  Tetrahedron {i}: vertices {tet}")

    # ============================================================================
    # EXAMPLE 8: Volume Calculation in 3D Delaunay
    # ============================================================================
    print("\n8. COMPUTING TETRAHEDRON VOLUMES")
    print("-" * 70)

    def tetrahedron_volume(p0, p1, p2, p3):
        """
        Compute volume of tetrahedron with vertices p0, p1, p2, p3.

        Volume = |det([p1-p0, p2-p0, p3-p0])| / 6
        """
        matrix = np.array([
            p1 - p0,
            p2 - p0,
            p3 - p0
        ]).T
        volume = abs(np.linalg.det(matrix)) / 6.0
        return volume

    # Compute volumes of first 5 tetrahedra
    print("Volumes of first 5 tetrahedra:\n")
    total_volume = 0
    for i in range(min(5, len(delaunay_3d.simplices))):
        tet_vertices = delaunay_3d.simplices[i]
        pts = delaunay_3d.points[tet_vertices]
        vol = tetrahedron_volume(pts[0], pts[1], pts[2], pts[3])
        total_volume += vol
        print(f"  Tetrahedron {i}: volume = {vol:.8f}")

    print(f"\nTotal volume of first 5 tetrahedra: {total_volume:.8f}")

    # ============================================================================
    # EXAMPLE 9: Voronoi Diagram Concept
    # ============================================================================
    print("\n9. VORONOI DIAGRAM: DUAL OF DELAUNAY")
    print("-" * 70)

    print("Voronoi diagram is dual to Delaunay:")
    print("- Each Voronoi cell is the region closer to one point than any other")
    print("- Voronoi vertices are circumcenters of Delaunay triangles")
    print("- Voronoi edges connect these circumcenters\n")

    # Compute Voronoi diagram
    vor = spatial.Voronoi(points_2d)

    print(f"Voronoi diagram for 2D points:")
    print(f"  Number of Voronoi vertices: {vor.vertices.shape[0]}")
    print(f"  Number of Voronoi regions: {len(vor.regions)}")

    print(f"\nVoronoi vertices (first 3):")
    for i in range(min(3, vor.vertices.shape[0])):
        print(f"  Vertex {i}: {vor.vertices[i]}")

    print(f"\nFirst 3 Voronoi regions:")
    for i in range(min(3, len(vor.regions))):
        region = vor.regions[i]
        print(f"  Point {i} region: vertices {region}")

    # ============================================================================
    # EXAMPLE 10: Practical Application - Mesh Generation
    # ============================================================================
    print("\n10. PRACTICAL APPLICATION: MESH GENERATION")
    print("-" * 70)

    print("Delaunay triangulation is used for mesh generation in FEA/FEM.\n")

    # Create a grid of points
    x = np.linspace(-1, 1, 5)
    y = np.linspace(-1, 1, 5)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.column_stack([xx.ravel(), yy.ravel()])

    # Create Delaunay mesh
    mesh = spatial.Delaunay(grid_points)

    print(f"Mesh from 5x5 grid:")
    print(f"  Points: {mesh.points.shape[0]}")
    print(f"  Triangles: {len(mesh.simplices)}")

    # Show triangle quality metrics
    def triangle_aspect_ratio(p0, p1, p2):
        """Compute aspect ratio of triangle (1.0 = equilateral)"""
        side_lengths = [
            np.linalg.norm(p1 - p0),
            np.linalg.norm(p2 - p1),
            np.linalg.norm(p0 - p2)
        ]
        return max(side_lengths) / min(side_lengths)

    aspect_ratios = []
    for triangle in mesh.simplices:
        p0, p1, p2 = mesh.points[triangle]
        ar = triangle_aspect_ratio(p0, p1, p2)
        aspect_ratios.append(ar)

    aspect_ratios = np.array(aspect_ratios)
    print(f"\nTriangle aspect ratios:")
    print(f"  Min: {aspect_ratios.min():.4f} (most regular)")
    print(f"  Max: {aspect_ratios.max():.4f} (most irregular)")
    print(f"  Mean: {aspect_ratios.mean():.4f}")
    print(f"  (1.0 = perfect equilateral, higher = worse)")

    print("\n" + "=" * 70)
    print("Key takeaways:")
    print("- Delaunay triangulation: optimal triangulation maximizing angles")
    print("- Empty circumcircle property: no points inside triangle's circumcircle")
    print("- ConvexHull: boundary of point set, useful for collision detection")
    print("- 2D: simplices are triangles, 3D: simplices are tetrahedra")
    print("- find_simplex(): locate point within triangulation")
    print("- Voronoi: dual structure, useful for spatial analysis")
    print("- Applications: mesh generation, interpolation, spatial indexing")
    print("=" * 70)
```

---

## Exercises

**Exercise 1.**
Given the edge list `[(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]` for an undirected graph with 5 nodes, construct the adjacency matrix as a sparse CSR matrix, compute the graph Laplacian $L = D - A$, and verify that the row sums of $L$ are all zero.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
        n_nodes = 5
        row = [e[0] for e in edges]
        col = [e[1] for e in edges]
        data = np.ones(len(edges))

        A = sparse.csr_matrix((data, (row, col)), shape=(n_nodes, n_nodes))
        A = A + A.T  # symmetrize for undirected graph

        D = sparse.diags(np.array(A.sum(axis=1)).flatten())
        L = D - A

        row_sums = np.array(L.sum(axis=1)).flatten()
        print("Row sums of Laplacian:", row_sums)
        assert np.allclose(row_sums, 0), "Row sums should all be zero"

---

**Exercise 2.**
Create a 2D grid of 20 random points using `np.random.seed(0)`, compute their Delaunay triangulation with `scipy.spatial.Delaunay`, and determine how many triangles are in the triangulation. Then use `find_simplex` to check whether the point `[0.5, 0.5]` lies inside the triangulation.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import spatial

        np.random.seed(0)
        points = np.random.rand(20, 2)

        tri = spatial.Delaunay(points)
        print(f"Number of triangles: {len(tri.simplices)}")

        test_point = [0.5, 0.5]
        simplex_idx = tri.find_simplex(test_point)
        if simplex_idx >= 0:
            print(f"Point {test_point} is inside triangle {simplex_idx}")
        else:
            print(f"Point {test_point} is outside the triangulation")

---

**Exercise 3.**
Build the adjacency matrix of a complete graph $K_6$ (6 nodes, every pair connected) as a sparse matrix. Compute the graph Laplacian and find its two smallest eigenvalues using `scipy.sparse.linalg.eigsh`. Verify that the smallest eigenvalue is approximately zero and the second smallest (the algebraic connectivity) equals 6.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 6
        # Complete graph: all pairs connected
        A = sparse.csr_matrix(np.ones((n, n)) - np.eye(n))

        D = sparse.diags(np.array(A.sum(axis=1)).flatten())
        L = D - A

        vals, vecs = splinalg.eigsh(L.astype(float), k=2, which='SM')
        print(f"Two smallest eigenvalues: {vals}")
        print(f"Smallest eigenvalue ~ 0: {np.isclose(vals[0], 0, atol=1e-10)}")
        print(f"Second smallest (algebraic connectivity) ~ 6: {np.isclose(vals[1], 6, atol=1e-6)}")
